import streamlit as st
import pandas as pd

from dotenv import load_dotenv

from paginas.adicionar_registro import adicionar_registro
from paginas.dashboard import dashboard
from paginas.gerenciar_registros import gerenciar_registros
from paginas.importar_planilhas import importar_planilhas
from paginas.ver_despesas import ver_despesas


load_dotenv()

# ---------------- CONFIGURAÇÃO ----------------

st.set_page_config("Finanças Familiar", layout="wide")

st.markdown("""
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="Content-Language" content="pt-BR">
    </head>
    </html>
""", unsafe_allow_html=True)




# ---------------- INTERFACE ----------------

st.title("Controle Financeiro Familiar")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Ver por categoria",
        "Adicionar Registro",
        "Gerenciar Registros",
        "Importar planilha"
    ]
)


# ---------------- PÁGINAS ----------------

if menu == "Adicionar Registro":
    adicionar_registro()

elif menu == "Dashboard":
    dashboard()

elif menu == "Gerenciar Registros":
    gerenciar_registros()

elif menu == "Importar planilha":
    importar_planilhas()

elif menu == "Ver por categoria":
    ver_despesas()