import streamlit as st
import pandas as pd
import re

from funcoes import carregar_dados
from database import conectar


def converter_valor(valor):
    if not valor:
        return 0.0

    valor = re.sub(r"[^\d,]", "", valor)
    valor = valor.replace(".", "").replace(",", ".")

    return float(valor)


def deletar_registro(id_registro):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM registros WHERE id = %s",
        (id_registro,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def atualizar_registro(id_registro, tipo, fonte, valor, data):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE registros
        SET tipo = %s,
            fonte = %s,
            valor = %s,
            data = %s
        WHERE id = %s
    """, (
        tipo,
        fonte,
        valor,
        data,
        id_registro
    ))

    conn.commit()

    cursor.close()
    conn.close()


def gerenciar_registros():

    if "confirmar_acao" not in st.session_state:
        st.session_state.confirmar_acao = None

    st.subheader("Gerenciar Registros")

    df = carregar_dados()

    if df.empty:

        st.info("Nenhum registro encontrado.")

    else:

        registro_id = st.selectbox(
            "Selecione um registro pelo ID:",
            df["id"]
        )

        registro = df[df["id"] == registro_id].iloc[0]

        tipo = st.selectbox(
            "Tipo",
            ["Receita", "Despesa", "Investimento"],
            index=[
                "Receita",
                "Despesa",
                "Investimento"
            ].index(registro["tipo"])
        )

        fonte = st.text_input(
            "Fonte",
            value=registro["fonte"]
        )

        valor = st.text_input(
            "Valor (R$)",
            value=str(registro["valor"]).replace(".", ",")
        )

        data_registro = st.date_input(
            "Data",
            value=pd.to_datetime(registro["data"])
        )

        col1, col2, _ = st.columns([1, 1, 12])

        with col1:

            if st.button("Atualizar"):
                st.session_state.confirmar_acao = "atualizar"

        with col2:

            if st.button("Apagar"):
                st.session_state.confirmar_acao = "apagar"

        # ---------------- ATUALIZAR ----------------

        if st.session_state.confirmar_acao == "atualizar":

            st.warning(
                "Tem certeza que deseja ATUALIZAR este registro?"
            )

            if st.button("Confirmar Atualização"):

                atualizar_registro(
                    registro_id,
                    tipo,
                    fonte,
                    converter_valor(valor),
                    data_registro
                )

                st.success("Registro atualizado!")

                st.session_state.confirmar_acao = None

                st.rerun()

        # ---------------- APAGAR ----------------

        if st.session_state.confirmar_acao == "apagar":

            st.error(
                "Tem certeza que deseja APAGAR este registro? "
                "Esta ação não pode ser desfeita."
            )

            if st.button("Confirmar Exclusão"):

                deletar_registro(registro_id)

                st.warning("Registro apagado!")

                st.session_state.confirmar_acao = None

                st.rerun()