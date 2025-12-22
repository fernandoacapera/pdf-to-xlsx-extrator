from logica import trans_df
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Extrator de Extrato", layout="wide")

st.title("Extrator de Extrato")
st.markdown("Faça upload do CSV para limpar e padronizar os dados.")

arquivo = st.file_uploader("Coloque o arquivo CSV aqui", type=['csv'])
botao = st.button("Extrair e Processar")

if botao and arquivo:
    with st.spinner('Lendo e processando arquivo...'):
        df = trans_df(arquivo)
        
        if df is None:
            st.error("Erro ao ler o arquivo. Verifique se é um CSV válido.")
        elif df.empty:
            st.warning("O arquivo foi lido, mas nenhuma linha de Pix ou TED foi encontrada.")
        else:
            st.success("Arquivo processado com sucesso!")
            st.dataframe(df)
            
            # Preparar Download
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Dados')
                
                # Ajuste automático de largura das colunas (Bônus estético)
                worksheet = writer.sheets['Dados']
                for i, col in enumerate(df.columns):
                    largura = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, largura)
            
            buffer.seek(0)

            st.download_button(
                label='📥 Baixar Excel Pronto',
                data=buffer,
                file_name='extrato_tratado.xlsx',
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )