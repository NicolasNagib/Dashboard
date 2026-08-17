import streamlit as st
import plotly.express as px
import pandas as pd
from funcoes import carregar_dados

cores = {
    "Receita": "#0e864e",
    "Despesa": "#9e1212",
    "Investimento": "#063c72"
}


def dashboard():
    df = carregar_dados()

    df["mes_num"] = df["data"].dt.month
    df["mes_nome"] = df["data"].dt.month_name(locale="pt_BR")

    mapa_meses = dict(zip(df["mes_nome"], df["mes_num"]))
    lista_meses = sorted(df["mes_nome"].unique(), key=lambda x: mapa_meses[x])
    menu = st.sidebar.selectbox("Mês", ["Todos"] + lista_meses)
    if menu != "Todos":
        mes_escolhido = mapa_meses[menu]
        df = df[df["mes_num"] == mes_escolhido]


    if df.empty:
        st.info("Nenhum dado cadastrado ainda.")
    else:
        receitas = df[df["tipo"] == "Receita"]["valor"].sum()
        despesas = df[df["tipo"] == "Despesa"]["valor"].sum()
        investimentos = df[df["tipo"] == "Investimento"]["valor"].sum()
        saldo = receitas - despesas 

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Receitas", f"R$ {receitas:,.2f}")
        col2.metric("Despesas", f"R$ {despesas:,.2f}")
        col3.metric("Investimentos", f"R$ {investimentos:,.2f}")
        col4.metric("Saldo", f"R$ {saldo:,.2f}")

        fig_pizza = px.pie(
            df,
            values="valor",
            names="tipo",
            title="Distribuição Financeira",
            color="tipo",
            color_discrete_map=cores
        )

        st.plotly_chart(fig_pizza, width='stretch')

        st.subheader("Histórico")
        
        df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m/%Y")
        
        df_exibicao = df.drop(columns=["id"]).reset_index(drop=True)
        st.dataframe(df_exibicao.sort_values("data", ascending=False), width='stretch', hide_index=True)
