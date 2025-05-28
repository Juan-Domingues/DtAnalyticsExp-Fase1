import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/Juan-Domingues/DtAnalyticsExp-Fase1/main/Arquivos%20Bases/Producao.csv', sep=';')

# Remove linhas com produtos em maiúsculo (categorias)
produtos_maiusculo = [
    'VINHO DE MESA',
    'VINHO FINO DE MESA (VINIFERA)',
    'SUCO',
    'DERIVADOS'
]
df = df[~df['produto'].isin(produtos_maiusculo)]

# Soma a produção total de cada registro (control) ao longo dos anos (2014 a 2023)
anos = [str(ano) for ano in range(2014, 2024)]
df['total_produzido'] = df[anos].sum(axis=1)

# Top 10 controls mais produzidos
top10 = df.nlargest(10, 'total_produzido').copy()

# Mapeamento dos prefixos para nomes completos
prefix_map = {
    'vm': 'Vinho de Mesa - ',
    'vv': 'Vinho Fino de Mesa - ',
    'su': 'Suco - ',
    'de': 'Derivado - '
}

def label_control_produto(row):
    prefix = row['control'][:2].lower()
    return prefix_map.get(prefix, '') + row['produto']

top10['control_label'] = top10.apply(label_control_produto, axis=1)

# Degradê escuro: do roxo escuro para um roxo ainda mais escuro (quase preto)
from matplotlib.colors import to_rgb

start_color = np.array(to_rgb("#3d003d"))  # Roxo bem escuro
end_color = np.array(to_rgb("#6f1d77"))    # Roxo escuro

degrade_colors = [
    tuple(start_color + (end_color - start_color) * (i / 9))
    for i in range(10)
]

plt.figure(figsize=(12,6))
bars = plt.bar(
    top10['control_label'],
    top10['total_produzido'] / 1_000_000_000,
    color=degrade_colors,
    edgecolor='none'
)
plt.title(
    'Ranking de Produção: Os 10 Principais Derivados da Uva (Período 2014-2023)',
    fontsize=15, weight='bold', color='#3d003d', pad=15
)
plt.xlabel('')
plt.ylabel('Bilhões de Litros', fontsize=12, color='#3d003d')
plt.xticks(rotation=20, ha='right', fontsize=11, color='#3d003d')
plt.yticks(fontsize=11, color='#3d003d')
plt.grid(axis='y', linestyle=':', alpha=0.12)
plt.gca().spines[['top', 'right', 'left']].set_visible(False)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.01,
        f'{bar.get_height():.2f}',
        ha='center', va='bottom', fontsize=10, color='#5a1846', fontweight='bold'
    )

plt.tight_layout()
plt.show()