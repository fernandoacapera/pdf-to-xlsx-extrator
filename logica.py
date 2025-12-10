# %%
import pandas as pd
import numpy as np

# %%
pd.__version__

# %%

# %%
def trans_df(excel):
    df = pd.read_csv(excel, encoding='latin-1')
    try:
        df = df.drop("Unnamed: 6", axis=1)
    except:
        pass
# Definir as condições
# Passando uma tupla com todas as opções de início
    df = df[df['Histórico'].str.startswith(('Pix - Recebido', 'TED', 'Transferência recebida'))]
    condicao_pix = df['Histórico'].str.startswith('Pix - Recebido')
    condicao_ted = df['Histórico'].str.startswith('TED')

    df['Tipo'] = np.where(condicao_pix, 'Pix Recebido', 
               np.where(condicao_ted, 'TED Recebido', 'Transferência Recebida')
             )
    df['Dependencia Origem'] = df['Dependencia Origem'].fillna("Não Informado")
    df['Data do Balancete'] = df['Data do Balancete'].fillna("Não Informado")

    df.insert(2, 'Tipo', df.pop('Tipo'))

    df['Histórico'] = df['Histórico'].str.replace(
    # 1. Lista os prefixos (Pix, Transf, TED com ou sem texto extra)
    r'^(Pix\s*-\s*Recebido|Transferência recebida|TED-Crédito em Conta|TED)'
    # 2. Remove o separador e qualquer "sujeira" numérica (datas, horas ou códigos como 085 0101) que vier depois
    r'\s*-\s*[\d\s/:]*', 
    '', 
    regex=True
    )
    df['Histórico'] = df['Histórico'].str.strip()

    df['CPF/CNPJ'] = df['Histórico'].str.extract(r'(\d{14}|\d{11})')

    df['Histórico'] = df['Histórico'].str.replace(r'(\d{14}|\d{11})', '', regex=True)

    df.insert(3, 'CPF/CNPJ', df.pop('CPF/CNPJ'))

    df = df.fillna("Não Informado")

    df.rename(columns={"Histórico":"Nome"}, inplace=True)
    return df



