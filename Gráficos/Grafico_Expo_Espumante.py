import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

df = pd.read_csv('https://raw.githubusercontent.com/Juan-Domingues/DtAnalyticsExp-Fase1/main/Arquivos%20Bases/ExpEspumantes.csv', sep='\t')

def rename_columns(col):
    if col.endswith('.1'):
        return f"{col[:-2]}_US$"
    elif col.isdigit():
        return f"{col}_Kg"
    else:
        return col

df = df.rename(columns=rename_columns)

cols_to_keep = [col for col in df.columns if not col[:4].isdigit() or int(col[:4]) >= 2015]
df = df[cols_to_keep]

pais_col = [col for col in df.columns if 'país' in col.lower() or 'pais' in col.lower()][0]

df[pais_col] = df[pais_col].replace('Alemanha, República Democrática', 'Alemanha')

anos = [str(ano) for ano in range(2015, 2024)]
kg_cols = [f"{ano}_Kg" for ano in anos if f"{ano}_Kg" in df.columns]
usd_cols = [f"{ano}_US$" for ano in anos if f"{ano}_US$" in df.columns]

df['Total_Kg'] = df[kg_cols].sum(axis=1)
df['Total_Ton'] = df['Total_Kg'] / 1000
df['Total_USD'] = df[usd_cols].sum(axis=1)

df_sorted = df.sort_values(by='Total_USD', ascending=False).head(10)

# Paleta viridis
colors = plt.cm.viridis([0.15 + 0.75*i/9 for i in range(10)])

plt.figure(figsize=(13,6))
bars = plt.bar(df_sorted[pais_col], df_sorted['Total_USD'], color=colors, edgecolor='none', zorder=3)
plt.xticks(rotation=30, ha='right', fontsize=11)
plt.title('Top 10 - Faturamento de Espumantes (US$) de 2015 a 2024', fontsize=16, weight='bold', color='#222')
plt.xlabel('País', fontsize=12, weight='bold')
plt.ylabel('Faturamento (US$ Mi)', fontsize=12, weight='bold')
plt.grid(axis='y', linestyle=':', alpha=0.25, zorder=0)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_linewidth(1)
plt.gca().spines['bottom'].set_linewidth(1)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1_000_000:.0f} Mi'))

for i, bar in enumerate(bars):
    valor = bar.get_height()
    volume = df_sorted['Total_Ton'].iloc[i]
    mi = valor / 1_000_000
    plt.text(
        bar.get_x() + bar.get_width()/2,
        valor + (plt.ylim()[1]*0.01),
        f"US$ {mi:,.2f} Mi\n{volume:,.1f} t",
        ha='center', va='bottom', fontsize=10, fontweight='bold', color='#222',
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.15')
    )

plt.tight_layout()
plt.show()