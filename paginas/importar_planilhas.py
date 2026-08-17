import streamlit as st
from funcoes import carregar_dados
from funcoes import importar_nubank_excel, carregar_dados, calcular_saldo

def importar_planilhas():
    st.subheader("Importar gastos do Nubank")

    arquivo_nubank = st.file_uploader(
        "Selecione o arquivo Excel do Nubank",
        type=["xlsx"]
    )

    if arquivo_nubank is not None:

        if st.button("Importar gastos"):

            try:
                importados, ignorados = importar_nubank_excel(
                    arquivo_nubank
                )

                st.success(
                    f"{importados} gastos importados com sucesso!"
                )

                if ignorados > 0:
                    st.info(
                        f"{ignorados} lançamentos foram ignorados "
                        "(entradas ou registros já existentes)."
                    )

                st.rerun()

            except Exception as e:
                st.error(f"Erro ao importar arquivo: {e}")