import matplotlib.pyplot as plt
import numpy as np

# Dados de consumo de vinho per capita em 2024 (litros por habitante)
paises = [
    'Portugal', 'Itália', 'França', 'Suíça', 'Áustria', 
    'Austrália', 'Alemanha', 'Hungria', 'Eslovênia', 
    'Reino Unido', 'Argentina', 'Holanda'
]

consumo = [61.1, 42.7, 41.5, 29.7, 28.6, 24.5, 24.5, 24.4, 23.8, 22.3, 21.6, 20.7]

# Configuração do gráfico vertical
plt.figure(figsize=(8, 4))

# Cor roxo escuro para todas as barras
cor_roxo_escuro = '#78143E'
cores = [cor_roxo_escuro] * len(paises)

# Gráfico de barras verticais
barras = plt.bar(paises, consumo, color=cores, edgecolor='black', linewidth=0.8)

# Personalização do gráfico
plt.ylabel('Consumo per capita (litros por habitante)', fontsize=12, fontweight='bold')
plt.xlabel('Países', fontsize=12, fontweight='bold')
plt.title('Consumo de Vinho per Capita por País em 2024\n(Dados da Organização Internacional da Vinha e do Vinho - OIV)', 
          fontsize=14, fontweight='bold', pad=20)

# Adicionando valores nas barras
for barra, valor in zip(barras, consumo):
    plt.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.5, 
             f'{valor:.1f}L', ha='center', va='bottom', fontweight='bold', fontsize=10)

# Configurações adicionais
plt.ylim(0, max(consumo) * 1.15)  # Espaço extra para os rótulos
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Adicionando uma nota explicativa
plt.figtext(0.5, 0.02, 
           'Fonte: Organização Internacional da Vinha e do Vinho (OIV) - 2024\n'
           'Portugal lidera o ranking mundial com 61,1 litros per capita, seguido por Itália (42,7L) e França (41,5L)',
           ha='center', fontsize=9, style='italic')

# Salvando o gráfico
plt.savefig('consumo_vinho_per_capita_2024_vertical.png', dpi=300, bbox_inches='tight')
plt.show()

print("Gráfico vertical salvo como 'consumo_vinho_per_capita_2024_vertical.png'")
print("\nAnálise dos dados:")
print("="*60)
print(f"País líder: {paises[0]} com {consumo[0]:.1f} litros per capita")
print(f"Diferença para o 2º lugar: {consumo[0] - consumo[1]:.1f} litros ({((consumo[0] - consumo[1])/consumo[1]*100):.1f}% a mais)")
print(f"Média dos top 3: {np.mean(consumo[:3]):.1f} litros per capita")
print(f"Média geral: {np.mean(consumo):.1f} litros per capita")
print("="*60)