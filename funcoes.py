import re
import pandas as pd

from database import conectar


def converter_valor(valor):
    if not valor:
        return 0.0

    valor = re.sub(r"[^\d,]", "", valor)
    valor = valor.replace(".", "").replace(",", ".")

    return float(valor)


def inserir_registro(tipo, fonte, valor, data):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO registros (tipo, fonte, valor, data)
        VALUES (%s, %s, %s, %s)
    """, (tipo, fonte, valor, data))

    conn.commit()

    cursor.close()
    conn.close()


def carregar_dados():

    conn = conectar()

    df = pd.read_sql(
        "SELECT * FROM registros",
        conn,
        parse_dates=["data"]
    )

    conn.close()

    return df


def calcular_saldo():

    df = carregar_dados()

    receitas = df[df["tipo"] == "Receita"]["valor"].sum()
    despesas = df[df["tipo"] == "Despesa"]["valor"].sum()
    investimentos = df[df["tipo"] == "Investimento"]["valor"].sum()

    return receitas - despesas - investimentos

# Importar planilhas


from funcoes import inserir_registro


def converter_valor(valor):
    """
    Converte valores como:
    '9,80' -> 9.80
    '1.234,56' -> 1234.56
    '- 50,00' -> -50.00
    """
    if pd.isna(valor):
        return 0.0

    valor = str(valor).strip()

    # Remove espaços
    valor = valor.replace(" ", "")

    # Mantém apenas números, ponto, vírgula e sinal
    valor = re.sub(r"[^\d,.\-]", "", valor)

    # Formato brasileiro: 1.234,56
    if "," in valor:
        valor = valor.replace(".", "").replace(",", ".")

    try:
        return float(valor)
    except ValueError:
        return 0.0


def categorizar_despesa(descricao):
    """
    Define automaticamente a categoria da despesa
    com base na descrição do Nubank.
    """
    descricao = str(descricao).lower()

    # Transporte
    palavras_transporte = [
        "uber",
        "99",
        "99food",
        "cabify",
        "taxi",
        "posto",
        "combustivel",
        "gasolina",
        "estacionamento",
        "pedagio"
    ]

    for palavra in palavras_transporte:
        if palavra in descricao:
            return "Transporte"

    # Contas
    palavras_contas = [
        "claro",
        "tim",
        "vivo",
        "oi ",
        "internet",
        "fatura",
        "energia",
        "cemig",
        "copasa",
        "aluguel",
        "telefone"
    ]

    for palavra in palavras_contas:
        if palavra in descricao:
            return "Contas"

    # Tudo que não foi identificado
    return "Outros"


def importar_nubank_excel(arquivo):

    df = pd.read_excel(arquivo)

    colunas_obrigatorias = {"date", "title", "amount"}

    if not colunas_obrigatorias.issubset(df.columns):
        raise ValueError(
            "O arquivo não possui as colunas esperadas: "
            "date, title e amount."
        )

    registros_importados = 0
    registros_ignorados = 0

    for _, linha in df.iterrows():

        descricao = str(linha["title"]).strip()

        if "pagamento recebido" in descricao.lower():
            registros_ignorados += 1
            continue

        valor = converter_valor(linha["amount"])

        if valor <= 0:
            registros_ignorados += 1
            continue

        data = pd.to_datetime(linha["date"]).date()

        categoria = categorizar_despesa(descricao)

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM registros
            WHERE tipo = %s
              AND fonte = %s
              AND valor = %s
              AND data = %s
        """, (
            "Despesa",
            categoria,
            valor,
            data
        ))

        existe = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        if existe:
            registros_ignorados += 1
            continue

        inserir_registro(
            "Despesa",
            categoria,
            valor,
            data
        )

        registros_importados += 1

    return registros_importados, registros_ignorados

def carregar_despesas():

    conn = conectar()

    df = pd.read_sql_query("""
        SELECT
            data,
            fonte,
            valor
        FROM registros
        WHERE tipo = 'Despesa'
        ORDER BY data
    """, conn)

    conn.close()

    return df