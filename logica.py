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
    condicoes = [
    df['Histórico'].str.startswith('Pix'),
    df['Histórico'].str.startswith('TED')
    ]

# Definir os resultados respectivos
    escolhas = [
    'Pix Recebido',
    'TED Recebido'
    ]

# Aplicar (o que sobrar vira 'Transferência Recebida')
    df['Tipo'] = np.select(condicoes, escolhas, default='Transferência Recebida')
    df['Dependencia Origem'] = df['Dependencia Origem'].fillna("Não Informado")
    df['Data do Balancete'] = df['Data do Balancete'].fillna("Não Informado")

    df.insert(2, 'Tipo', df.pop('Tipo'))

    df['Histórico'] = df['Histórico'].str.replace(
        r'^(Pix\s*-\s*Recebido|Transferência recebida|TED-Crédito em Conta)\s*-\s*\d{2}/\d{2}\s*\d{2}:\d{2}\s*',
        '',
        regex=True
    )

    df['CPF/CNPJ'] = df['Histórico'].str.extract(r'(\d{14}|\d{11})')

    df['Histórico'] = df['Histórico'].str.replace(r'(\d{14}|\d{11})', '', regex=True)

    df.insert(3, 'CPF/CNPJ', df.pop('CPF/CNPJ'))

    df = df.fillna("Não Informado")

    df.rename(columns={"Histórico":"Nome"}, inplace=True)
    return df



