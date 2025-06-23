#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib

# Ensure 'DejaVu Sans' font is available or comment this out if it causes issues
# and matplotlib will use a default font.
try:
    matplotlib.rcParams['font.family'] = 'DejaVu Sans'
except RuntimeError:
    print("DejaVu Sans font not found, using Matplotlib default.")

# Define the directory for saving the graph
DIRETORIO_GRAFICOS = 'graficos_isolados'
os.makedirs(DIRETORIO_GRAFICOS, exist_ok=True)

# Data for world wine consumption (as defined in your script's criar_dados_exemplo)
data_consumo_mundial = {
    'pais': [
        'Países Baixos', 'Brasil', 'África do Sul', 'Canadá', 'Austrália',
        'Portugal', 'China', 'Argentina', 'Rússia', 'Espanha',
        'Reino Unido', 'Alemanha', 'Itália', 'França', 'Estados Unidos'
    ],
     'consumo_milhoes_hectolitros': [
        3.3, 4.0, 4.5, 4.8, 5.4,
        6.6, 6.8, 7.8, 8.6, 9.8,
        12.8, 19.1, 21.8, 24.4, 33.3
    ]
}

df_consumo_mundial = pd.DataFrame(data_consumo_mundial)

# Sort data for better visualization (optional, but often good for bar charts)
df_consumo_mundial = df_consumo_mundial.sort_values(by='consumo_milhoes_hectolitros', ascending=True)

# Generate the world consumption chart
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['axes.formatter.use_locale'] = True # For number formatting if applicable

fig, ax = plt.subplots(figsize=(12, 8)) # Adjusted figsize for potentially better label display

# Define the custom color palette
custom_colors = ['#78143E', '#C30D61']
num_bars = len(df_consumo_mundial)
bar_colors = [custom_colors[i % len(custom_colors)] for i in range(num_bars)]

bars = ax.barh(df_consumo_mundial['pais'], df_consumo_mundial['consumo_milhoes_hectolitros'],
              color=bar_colors)

ax.set_xlabel('Consumo (Milhões de Hectolitros)', fontsize=12)
ax.set_ylabel('País', fontsize=12)
ax.set_title('Consumo Mundial de Vinho por País (2023)', fontsize=16, fontweight='bold')

# Add values at the end of the bars
for i, v in enumerate(df_consumo_mundial['consumo_milhoes_hectolitros']):
    ax.text(v + 0.2, i, f'{v}', va='center', fontsize=10) # Adjusted offset and fontsize

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
fig.tight_layout() # Use fig.tight_layout() for better spacing

output_filename = f'{DIRETORIO_GRAFICOS}/consumo_mundial_modificado.png'
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.close()

print(f"Gráfico 'Consumo Mundial de Vinho por País (2023)' gerado com sucesso!")
print(f"Arquivo salvo como: {output_filename}")