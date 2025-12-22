import pandas as pd
import numpy as np
import io

def trans_df(uploaded_file):
    try:
        # --- PARTE 1: Leitura Robusta (Resolve o erro da primeira imagem) ---
        conteudo_bytes = uploaded_file.getvalue()
        
        # Tenta decodificar latin-1 ou utf-8
        try:
            texto = conteudo_bytes.decode('latin-1')
        except:
            texto = conteudo_bytes.decode('utf-8', errors='ignore')

        # Remove aspas que causam confusão nas colunas
        texto_limpo = texto.replace('"', '')

        # engine='python' e on_bad_lines='skip' impedem que o app trave se uma linha estiver quebrada
        df = pd.read_csv(io.StringIO(texto_limpo), sep=',', on_bad_lines='skip', engine='python')

    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return None

    # --- PARTE 2: Limpeza e Tratamento ---
    try:
        df = df.drop("Unnamed: 6", axis=1, errors='ignore')
        
        if 'Histórico' not in df.columns:
            return None

        # Filtra apenas o que interessa
        termos_interesse = ('Pix - Recebido', 'TED', 'Transferência recebida')
        df = df[df['Histórico'].str.startswith(termos_interesse, na=False)].copy()

        if df.empty:
            return pd.DataFrame()

        # Define os tipos
        condicao_pix = df['Histórico'].str.startswith('Pix - Recebido')
        condicao_ted = df['Histórico'].str.startswith('TED')

        df['Tipo'] = np.where(condicao_pix, 'Pix Recebido', 
                     np.where(condicao_ted, 'TED Recebido', 'Transferência Recebida'))
        
        # Preenche nulos
        cols_fillna = ['Dependencia Origem', 'Data do Balancete']
        for col in cols_fillna:
            if col in df.columns:
                df[col] = df[col].fillna("Não Informado")

        if len(df.columns) > 2:
            df.insert(2, 'Tipo', df.pop('Tipo'))

        # --- PARTE 3: O REGEX ATUALIZADO (Resolve o erro da segunda imagem) ---
        # Adicionei "TED Transf.Eletr.Disponiv" na lista de remoção
        padrao_regex = (
            r'^(Pix\s*-\s*Recebido|Transferência recebida|TED-Crédito em Conta|TED Transf\.Eletr\.Disponiv|TED)' # Lista de prefixos
            r'[\s-]*'         # Qualquer traço ou espaço depois do prefixo
            r'[\d\s/:]*'      # Qualquer número, data ou código depois
        )
        
        df['Histórico'] = df['Histórico'].str.replace(padrao_regex, '', regex=True)
        df['Histórico'] = df['Histórico'].str.strip()

        # Extrai CPF/CNPJ e remove do nome
        df['CPF/CNPJ'] = df['Histórico'].str.extract(r'(\d{14}|\d{11})')
        df['Histórico'] = df['Histórico'].str.replace(r'(\d{14}|\d{11})', '', regex=True)
        
        # Limpeza final de sujeira (traços soltos no inicio do nome)
        df['Histórico'] = df['Histórico'].str.replace(r'^[\s-]*', '', regex=True).str.strip()

        if len(df.columns) > 3:
            df.insert(3, 'CPF/CNPJ', df.pop('CPF/CNPJ'))

        df = df.fillna("Não Informado")
        df.rename(columns={"Histórico": "Nome"}, inplace=True)
        
        return df
        
    except Exception as e:
        print(f"Erro no tratamento: {e}")
        return None