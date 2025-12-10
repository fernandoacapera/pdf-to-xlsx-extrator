from logica import trans_df
import streamlit as st
import pandas as pd
import io
st.set_page_config(page_title="Extrator de Extrato")

st.title("Extrator de Extrato")
arquivo = st.file_uploader("Coloque o arquivo CSV aqui", type=['csv'])
botao = st.button("Extrair")

if botao:
    df = trans_df(arquivo)
    st.dataframe(df)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    buffer.seek(0)

    st.download_button(
        label='Baixar Excel',
        data=buffer,
        file_name='arquivo_extraido.xlsx',
       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

