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

    df = df[df['Histórico'].str.contains("Pix - Recebido|Transferência recebida", na=False)]


    df[df['Histórico'].str.contains("Transferência recebida", na=False)]

    condicao = df['Histórico'].str[:3] == 'Pix'

    df['Tipo'] = np.where(condicao, 'Pix Recebido', 'Transferência Recebida')
    df['Dependencia Origem'] = df['Dependencia Origem'].fillna("Não Informado")
    df['Data do Balancete'] = df['Data do Balancete'].fillna("Não Informado")

    df.insert(2, 'Tipo', df.pop('Tipo'))

    df['Histórico'] = df['Histórico'].str.replace(
        r'^(Pix\s*-\s*Recebido|Transferência recebida)\s*-\s*\d{2}/\d{2}\s*\d{2}:\d{2}\s*',
        '',
        regex=True
    )

    df['CPF/CNPJ'] = df['Histórico'].str.extract(r'(\d{14}|\d{11})')

    df['Histórico'] = df['Histórico'].str.replace(r'(\d{14}|\d{11})', '', regex=True)

    df.insert(3, 'CPF/CNPJ', df.pop('CPF/CNPJ'))

    df = df.fillna("Não Informado")

    df.rename(columns={"Histórico":"Nome"}, inplace=True)
    return df



