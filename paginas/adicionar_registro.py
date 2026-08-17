import streamlit as st
from funcoes import converter_valor
from datetime import date
from funcoes import inserir_registro




def adicionar_registro():
    st.subheader("Novo Registro")
        
    fonte_opcoes = "SELECIONE O TIPO DE REGISTRO"

    tipo = st.selectbox("Tipo", ["Receita", "Despesa", "Investimento"])

    if tipo == "Receita":
        fonte_opcoes = ["Trabalho", "Outros"]
    elif tipo == "Despesa":
        fonte_opcoes = ["Contas", "Supermercado", "Transporte", "Outros"]

    fonte = st.selectbox("Fonte", fonte_opcoes)
    valor_texto = st.text_input("Valor (R$)", placeholder="0,00")
    data_registro = st.date_input("Data", value=date.today())

    if st.button("Salvar"):
        valor = converter_valor(valor_texto)
        inserir_registro(tipo, fonte, valor, data_registro)
        st.success("Registro salvo com sucesso!")