import streamlit as st
import plotly.express as px
import pandas as pd
from funcoes import carregar_despesas

cores = {
    "Transporte": "#d4c10e",
    "Contas": "#9e1212",
    "Outros": "#063c72"
}

def ver_despesas():
        df_despesas = carregar_despesas()

        df_despesas["data"] = pd.to_datetime(df_despesas["data"])

        # Cria coluna mês
        df_despesas["mes"] = df_despesas["data"].dt.to_period("M")

   
        # Lista de meses disponíveis
         # Mapeamento meses
        meses = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro"
            }
        
        df_despesas["mes_num"] = df_despesas["data"].dt.month
        df_despesas["mes_nome"] = df_despesas["data"].dt.month.map(meses)
    
        mapa_meses = dict(zip(df_despesas["mes_nome"], df_despesas["mes_num"]))
        lista_meses = sorted(df_despesas["mes_nome"].unique(), key=lambda x: mapa_meses[x])
        menu = st.sidebar.selectbox("Mês", ["Todos"] + lista_meses)
        if menu != "Todos":
                mes_escolhido = mapa_meses[menu]
                df_despesas = df_despesas[df_despesas["mes_num"] == mes_escolhido]
        else:
            mes_escolhido = "todos os meses"

        

        st.subheader(
            f"Gastos de {mes_escolhido}"
        )


        st.metric(
            "Total gasto",
            f"R$ {df_despesas["valor"].sum():,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        # Gastos por categoria
        gastos_categoria = (
        df_despesas
        .groupby("fonte", as_index=False)["valor"]
        .sum()
        .sort_values("valor", ascending=False)
        )

        st.subheader("Gastos por categoria")

        fig_pizza = px.pie(
            gastos_categoria,
            values="valor",
            names="fonte",
            title="Distribuição dos gastos",
            color="fonte",
            color_discrete_map=cores
        )

        fig_pizza.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig_pizza,
            use_container_width=True
        )
        
        gastos_categoria = (
            df_despesas
            .groupby("fonte", as_index=False)["valor"]
            .sum()
            .sort_values("valor", ascending=False)
        )
        
        col1, col2, col3 = st.columns(3)

        transporte = gastos_categoria.loc[
            gastos_categoria["fonte"] == "Transporte",
            "valor"
        ].sum()

        contas = gastos_categoria.loc[
            gastos_categoria["fonte"] == "Contas",
            "valor"
        ].sum()

        outros = gastos_categoria.loc[
            gastos_categoria["fonte"] == "Outros",
            "valor"
        ].sum()

        col1.metric(
            "Transporte",
            f"R$ {transporte:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        col2.metric(
            "Contas",
            f"R$ {contas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

        col3.metric(
            "Outros",
            f"R$ {outros:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        # Tabela
        st.subheader("Lançamentos")

        st.dataframe(
            df_despesas[
                ["data", "fonte", "valor"]
            ].sort_values("data", ascending=False),
            use_container_width=True
        )