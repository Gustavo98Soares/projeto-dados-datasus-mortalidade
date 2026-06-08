import pandas as pd

arquivo_2023 = 'dados/DATASUS23.csv'
arquivo_2024 = 'dados/DATASUS24.csv'

def ler_csv_forcado(caminho_arquivo):
    """Tenta ler o CSV com ponto e vírgula, se falhar ou ler pouca linha, tenta vírgula"""
    print(f"\nAnalisando arquivo: {caminho_arquivo}")
    
    
    df = pd.read_csv(caminho_arquivo, sep=';', low_memory=False, nrows=5)
    
    if len(df.columns) <= 1:
        separador = ','
    else:
        separador = ';'
        
    print(f"-> Separador detectado para este arquivo: '{separador}'")
    
    
    df_completo = pd.read_csv(caminho_arquivo, sep=separador, low_memory=False)
    print(f"-> Total de linhas lidas deste arquivo: {len(df_completo):,}".replace(',', '.'))
    return df_completo

# 1. Ler os dois arquivos garantindo a detecção do separador
df_2023 = ler_csv_forcado(arquivo_2023)
df_2024 = ler_csv_forcado(arquivo_2024)

# 2. Juntar as duas tabelas
print("\nUnificando as duas bases de dados...")
df_unificado = pd.concat([df_2023, df_2024], ignore_index=True)

# 3. Exibir diagnóstico final no terminal
print("\n=== DIAGNÓSTICO DO PYTHON ===")
total_2023 = len(df_2023)
total_2024 = len(df_2024)
total_esperado = total_2023 + total_2024
total_real = len(df_unificado)

print(f"Linhas em 2023: {total_2023:,}".replace(',', '.'))
print(f"Linhas em 2024: {total_2024:,}".replace(',', '.'))
print(f"Soma esperada : {total_esperado:,}".replace(',', '.'))
print(f"Soma real final: {total_real:,}".replace(',', '.'))

if total_real == total_esperado:
    print("\n[SUCESSO] O empilhamento funcionou perfeitamente agora!")
else:
    print("\n[ALERTA] Os números ainda não batem. Verifique se os arquivos possuem dados.")

# 4. Salvar a base bruta unificada corrigida
arquivo_final = 'datasus_2023_2024_completo_bruto.csv'
print(f"\nSalvando arquivo corrigido em '{arquivo_final}'... Por favor, aguarde.")
df_unificado.to_csv(arquivo_final, index=False, sep=';', encoding='utf-8')
print("Arquivo salvo com sucesso!")