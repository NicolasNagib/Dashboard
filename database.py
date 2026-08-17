import os
import psycopg2
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def conectar():

    # Quando estiver no Streamlit Cloud
    if "DB_HOST" in st.secrets:

        return psycopg2.connect(
            host=st.secrets["DB_HOST"],
            port=st.secrets["DB_PORT"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            connect_timeout=10
        )

    # Quando estiver rodando localmente
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=10
    )