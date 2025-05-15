import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:\\Users\\jp291\\Downloads\\ExpVinho.csv', sep='\t')

# Função para renomear as colunas
def rename_columns(col):
    if col.endswith('.1'):
        return f"{col[:-2]}_US$"
    elif col.isdigit():
        return f"{col}_Kg"
    else:
        return col

df = df.rename(columns=rename_columns)

# Seleciona apenas colunas de 2014 em diante (Kg e US$), além das não relacionadas a anos
cols_to_keep = [col for col in df.columns if not col[:4].isdigit() or int(col[:4]) >= 2014]
df = df[cols_to_keep]

# Supondo que a coluna do país se chama 'País' ou similar, ajuste conforme necessário
pais_col = [col for col in df.columns if 'país' in col.lower() or 'pais' in col.lower()][0]

# Seleciona colunas de volume e valor de 2014 a 2024
anos = [str(ano) for ano in range(2014, 2024)]
kg_cols = [f"{ano}_Kg" for ano in anos if f"{ano}_Kg" in df.columns]
usd_cols = [f"{ano}_US$" for ano in anos if f"{ano}_US$" in df.columns]

# Soma o volume e valor exportado no período para cada país
df['Total_Kg'] = df[kg_cols].sum(axis=1)
df['Total_USD'] = df[usd_cols].sum(axis=1)

# Ordena pelo total de volume exportado e pega o top 10
df_sorted_1 = df.sort_values(by='Total_Kg', ascending=False).head(10)
df_sorted_2 = df.sort_values(by='Total_USD', ascending=False).head(10)

# Gráfico de volume exportado (2014-2024) - Top 10
plt.figure(figsize=(10,5))
bars = plt.bar(df_sorted_1[pais_col], df_sorted_1['Total_Kg'])
plt.xticks(rotation=90)
plt.title('Top 10 - Volume Exportado (Kg) de 2014 a 2024')
plt.xlabel('País')
plt.ylabel('Volume (Kg)')
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{int(bar.get_height()):,}',
             ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.show()

# Gráfico de valor exportado (2014-2024) - Top 10
plt.figure(figsize=(10,5))
bars = plt.bar(df_sorted_2[pais_col], df_sorted_2['Total_USD'])
plt.xticks(rotation=90)
plt.title('Top 10 - Valor Exportado (US$) de 2014 a 2024')
plt.xlabel('País')
plt.ylabel('Valor (US$)')
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{int(bar.get_height()):,}',
             ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.show()