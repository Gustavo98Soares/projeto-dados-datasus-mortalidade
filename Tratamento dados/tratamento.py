import pandas as pd
import numpy as np

# Carregar arquivos brutos
arquivo_bruto = 'datasus_2023_2024_completo_bruto.csv'
print("Carregando os ~3 milhões de registros... Isso pode levar alguns segundos.")
df = pd.read_csv(arquivo_bruto, sep=';', low_memory=False)


# DATA DO ÓBITO

if 'DTOBITO' in df.columns:
    df['DTOBITO'] = df['DTOBITO'].astype(str).str.split('.').str[0].str.zfill(8)
    df['Data_Obito'] = pd.to_datetime(df['DTOBITO'], format='%d%m%Y', errors='coerce')
else:
    df['Data_Obito'] = np.nan

# AC 01: ANALISE GEOGRAFICA (UF e Região)
# Os 2 primeiros dígitos do código do município representam o Estado (IBGE)
df['UF_Codigo'] = df['CODMUNOCOR'].astype(str).str[:2]

uf_mapping = {
    '11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO',
    '21': 'MA', '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL', '28': 'SE', '29': 'BA',
    '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP',
    '41': 'PR', '42': 'SC', '43': 'RS',
    '50': 'MS', '51': 'MT', '52': 'GO', '53': 'DF'
}
df['UF'] = df['UF_Codigo'].map(uf_mapping).fillna('Ignorado')

regiao_mapping = {
    'RO': 'Norte', 'AC': 'Norte', 'AM': 'Norte', 'RR': 'Norte', 'PA': 'Norte', 'AP': 'Norte', 'TO': 'Norte',
    'MA': 'Nordeste', 'PI': 'Nordeste', 'CE': 'Nordeste', 'RN': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'AL': 'Nordeste', 'SE': 'Nordeste', 'BA': 'Nordeste',
    'MG': 'Sudeste', 'ES': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'SC': 'Sul', 'RS': 'Sul',
    'MS': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'DF': 'Centro-Oeste'
}
df['Regiao'] = df['UF'].map(regiao_mapping).fillna('Ignorado')

# AC 02: RAÇA E SEXO

sex_mapping = {'1': 'Masculino', 'M': 'Masculino', '2': 'Feminino', 'F': 'Feminino'}
df['Sexo'] = df['SEXO'].astype(str).str.strip().map(sex_mapping).fillna('Ignorado')

raca_mapping = {
    '1': 'Branca', '2': 'Preta', '3': 'Amarela', 
    '4': 'Parda', '5': 'Indígena', '9': 'Ignorado'
}
df['Raca_Cor'] = df['RACACOR'].astype(str).str.split('.').str[0].str.strip().map(raca_mapping).fillna('Ignorado')

# AC 03: IDADE E ESCOLARIDADE
# O DATASUS usa códigos para a idade (ex: 420 significa 20 anos, 305 significa 5 meses). 
def converter_idade(val):
    try:
        val_str = str(val).split('.')[0].zfill(3)
        if len(val_str) == 3:
            prefixo = val_str[0]
            num = int(val_str[1:])
            if prefixo == '4': return num  # Anos de vida
            elif prefixo in ['1', '2', '3']: return 0  # Horas, Dias ou Meses (menor de 1 ano)
            elif prefixo == '5': return num + 100  # Centenários
        return np.nan
    except:
        return np.nan

df['Idade_Anos'] = df['IDADE'].apply(converter_idade)

# Escolaridade (Pode vir como 'ESC' ou 'ESC2010')
esc_col = 'ESC2010' if 'ESC2010' in df.columns else 'ESC'
esc_mapping = {
    '0': 'Sem Escolaridade', '1': 'Fundamental I (1ª a 4ª série)', '2': 'Fundamental II (5ª a 8ª série)',
    '3': 'Ensino Médio', '4': 'Ensino Superior incompleto', '5': 'Ensino Superior completo',
    '9': 'Ignorado'
}
df['Escolaridade'] = df[esc_col].astype(str).str.split('.').str[0].str.strip().map(esc_mapping).fillna('Ignorado')

# AC 04: CIRCUNSTÂNCIA DA MORTE
circ_mapping = {
    '1': 'Acidente', '2': 'Suicídio', '3': 'Homicídio', 
    '4': 'Outros','9': 'Ignorado'
}
# Se estiver vazio ou não listado na tabela de violência, considero Causa Natural (Doenças/Velhice)
df['Circunstancia_Obito'] = df['CIRCOBITO'].astype(str).str.split('.').str[0].str.strip().map(circ_mapping).fillna('Causa Natural')

# EXPORTAÇÃO 

colunas_finais = ['Data_Obito', 'UF', 'Regiao', 'Sexo', 'Raca_Cor', 'Idade_Anos', 'Escolaridade', 'Circunstancia_Obito']

df_clean = df[colunas_finais].dropna(subset=['Data_Obito'])

arquivo_saida = 'datasus_analise_final.csv'
df_clean.to_csv(arquivo_saida, index=False, sep=';', encoding='utf-8')
