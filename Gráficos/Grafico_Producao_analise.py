import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import matplotlib.patheffects as path_effects_module
import os
import requests
import pandas as pd

def download_geojson():
    """
    Baixa o arquivo GeoJSON do Brasil se não existir localmente.
    """
    filename = 'brazil_states.geojson'
    if not os.path.exists(filename):
        print(f"Baixando arquivo GeoJSON do Brasil para: {os.path.abspath(filename)}")
        url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Arquivo {filename} baixado com sucesso!")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar o arquivo GeoJSON: {e}")
            return None
    else:
        print(f"Arquivo {filename} já existe localmente em: {os.path.abspath(filename)}")
    return filename

def get_text_color_for_bg(bg_color_hex, default_color='black'):
    """
    Determina se o texto deve ser preto ou branco com base na luminosidade da cor de fundo.
    """
    try:
        rgb = mcolors.hex2color(bg_color_hex)
        luminance = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
        return 'white' if luminance < 0.4 else 'black' # Ajustado threshold
    except ValueError:
        return default_color

# Dados de produção de uva 2024
grape_production_states_2024 = {
    'Rio Grande do Sul': 703022,
    'São Paulo': 144836,
    'Santa Catarina': 39927,
    'Paraná': 54700,
    # Adicione outros estados se tiver os dados e quiser destacá-los
}

grape_production_regions_2024 = {
    'Sul': 798649,
    'Sudeste': 144836,
    'Nordeste': 703022,
    'Centro-Oeste': 3862,
    'Norte': 0
}

state_to_region_map = {
    'Acre': 'Norte', 'Alagoas': 'Nordeste', 'Amapá': 'Norte', 'Amazonas': 'Norte',
    'Bahia': 'Nordeste', 'Ceará': 'Nordeste', 'Distrito Federal': 'Centro-Oeste',
    'Espírito Santo': 'Sudeste', 'Goiás': 'Centro-Oeste', 'Maranhão': 'Nordeste',
    'Mato Grosso': 'Centro-Oeste', 'Mato Grosso do Sul': 'Centro-Oeste',
    'Minas Gerais': 'Sudeste', 'Pará': 'Norte', 'Paraíba': 'Nordeste',
    'Paraná': 'Sul', 'Pernambuco': 'Nordeste', 'Piauí': 'Nordeste',
    'Rio de Janeiro': 'Sudeste', 'Rio Grande do Norte': 'Nordeste',
    'Rio Grande do Sul': 'Sul', 'Rondônia': 'Norte', 'Roraima': 'Norte',
    'Santa Catarina': 'Sul', 'São Paulo': 'Sudeste', 'Sergipe': 'Nordeste',
    'Tocantins': 'Norte'
}

# Mapeamento nome do estado -> sigla
state_name_to_sigla = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM',
    'Bahia': 'BA', 'Ceará': 'CE', 'Distrito Federal': 'DF', 'Espírito Santo': 'ES',
    'Goiás': 'GO', 'Maranhão': 'MA', 'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG', 'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR',
    'Pernambuco': 'PE', 'Piauí': 'PI', 'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS', 'Rondônia': 'RO', 'Roraima': 'RR', 'Santa Catarina': 'SC',
    'São Paulo': 'SP', 'Sergipe': 'SE', 'Tocantins': 'TO'
}

# Posições externas para rótulos (fora do mapa, ajuste conforme necessário)
external_label_positions = {
    'RS': (-52, -31),   # Ajuste para próximo do estado, mas fora do polígono
    'SC': (-52, -28),
    'PR': (-52, -23),
    'SP': (-44, -20),
    # Adicione outros estados conforme necessário
}

def create_grape_production_map_by_state(brazil_gdf):
    """
    Cria e exibe o mapa de produção de UVA por ESTADO no Brasil para 2024,
    com rótulos fora do mapa e setas ligando ao estado.
    """
    print("\nGerando mapa de produção de uva por ESTADO...")
    brazil_states_map_data = brazil_gdf.copy()
    # Sempre cria a coluna 'sigla' a partir do nome do estado
    brazil_states_map_data['sigla'] = brazil_states_map_data['name'].map(state_name_to_sigla)
    brazil_states_map_data['grape_production_2024'] = 0
    for state_name, production in grape_production_states_2024.items():
        brazil_states_map_data.loc[brazil_states_map_data['name'] == state_name, 'grape_production_2024'] = production

    fig, ax = plt.subplots(1, 1, figsize=(15, 13))
    min_prod_val = 0
    relevant_prod_values = brazil_states_map_data[brazil_states_map_data['grape_production_2024'] > 0]['grape_production_2024']
    max_prod_val = relevant_prod_values.max() if not relevant_prod_values.empty else 1

    brazil_states_map_data.plot(
        column='grape_production_2024',
        ax=ax,
        legend=True,
        legend_kwds={'label': "Produção de Uva em Toneladas (2024)",
                     'orientation': "horizontal",
                     'shrink': 0.55, 'pad':0.02, 'aspect': 30},
        cmap='YlOrRd',
        missing_kwds={"color": "#F5F5F5", "edgecolor": "#C0C0C0", "label": "Sem dados/Baixa prod."},
        edgecolor='#BDBDBD',
        linewidth=0.6,
        vmin=min_prod_val,
        vmax=max_prod_val
    )

    ax.set_axis_off()
    plt.title('Produção de Uva por Estado - Brasil (2024)', fontsize=20, fontweight='bold', pad=15)

    for idx, row in brazil_states_map_data.iterrows():
        centroid = row['geometry'].centroid
        state_initials = row['sigla']
        production_value = row['grape_production_2024']

        # Mostra o centroide do RS para ajudar no ajuste
        if state_initials == 'RS':
            print(f"RS centroide: {centroid.x}, {centroid.y}")

        # Use posição externa se disponível, senão pule o rótulo
        if state_initials not in external_label_positions:
            continue
        label_x, label_y = external_label_positions[state_initials]

        current_bg_color_hex = "#F5F5F5"
        if production_value > 0:
            norm = mcolors.Normalize(vmin=min_prod_val, vmax=max_prod_val)
            cmap_plot = plt.cm.get_cmap('YlOrRd')
            current_bg_color_rgba = cmap_plot(norm(production_value))
            current_bg_color_hex = mcolors.to_hex(current_bg_color_rgba)
        text_color = get_text_color_for_bg(current_bg_color_hex)

        # Texto do rótulo
        label_text = f"{state_initials}\n{int(production_value):,} t".replace(",", ".") if production_value > 0 else state_initials

        # Anotação com seta
        ax.annotate(
            label_text,
            xy=(centroid.x, centroid.y), xycoords='data',
            xytext=(label_x, label_y), textcoords='data',
            fontsize=10, color=text_color, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=0.8, alpha=0.85),
            arrowprops=dict(arrowstyle="->", color='gray', lw=1.5, connectionstyle="arc3,rad=0.2"),
            path_effects=[path_effects_module.Stroke(linewidth=1.2, foreground='#FFFFFF'),
                          path_effects_module.Normal()]
        )

    plt.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.93)
    output_file = 'mapa_producao_uva_estados_2024_rotulos_externos_seta.png'
    try:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Mapa por ESTADO salvo como '{os.path.abspath(output_file)}'")
        plt.show()
    except Exception as e:
        print(f"Erro ao salvar ou mostrar o mapa por ESTADO: {e}")

def create_grape_production_map_by_region(brazil_gdf):
    """
    Cria e exibe o mapa de produção de UVA por REGIÃO no Brasil para 2024.
    """
    print("\nGerando mapa de produção de uva por REGIÃO...")
    brazil_regions_map_data = brazil_gdf.copy()
    
    brazil_regions_map_data['regiao'] = brazil_regions_map_data['name'].map(state_to_region_map)
    regions_gdf = brazil_regions_map_data.dissolve(by='regiao', aggfunc='sum')
    
    regions_gdf['grape_production_2024'] = 0
    for region_name, production in grape_production_regions_2024.items():
        if region_name in regions_gdf.index:
            regions_gdf.loc[region_name, 'grape_production_2024'] = production
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    
    relevant_prod_regions = regions_gdf[regions_gdf['grape_production_2024'] > 0]['grape_production_2024']
    max_prod_region = relevant_prod_regions.max() if not relevant_prod_regions.empty else 1

    regions_gdf.plot(column='grape_production_2024',
                     ax=ax,
                     legend=True,
                     legend_kwds={'label': "Produção de Uva em Toneladas (2024)",
                                  'orientation': "horizontal",
                                  'shrink': 0.55, 'pad':0.02, 'aspect': 30},
                     cmap='Greens', 
                     missing_kwds={"color": "#F5F5F5", "edgecolor": "#C0C0C0", "label": "Sem dados/Baixa prod."},
                     edgecolor='#777777',
                     linewidth=1.2,
                     vmin=0,
                     vmax=max_prod_region)
    
    ax.set_axis_off()
    plt.title('Produção de Uva por Região - Brasil (2024)', fontsize=20, fontweight='bold', pad=15)

    for region_name, row in regions_gdf.iterrows():
        representative_point = row['geometry'].representative_point()
        production_value = row['grape_production_2024']
        
        current_bg_color_hex = "#F5F5F5"
        if pd.notna(production_value) and production_value > 0 :
            norm = mcolors.Normalize(vmin=0, vmax=max_prod_region)
            cmap_plot = plt.cm.get_cmap('Greens')
            current_bg_color_rgba = cmap_plot(norm(production_value))
            current_bg_color_hex = mcolors.to_hex(current_bg_color_rgba)

        text_color = get_text_color_for_bg(current_bg_color_hex)
        
        label_text = f"{region_name}\n({int(production_value):,} t)".replace(",",".") if pd.notna(production_value) and production_value > 0 else region_name
        if region_name == "Norte" and production_value == 0:
             label_text = region_name

        ax.text(representative_point.x, representative_point.y, label_text,
                  horizontalalignment='center', verticalalignment='center',
                  fontsize=11, color=text_color, fontweight='bold',
                  linespacing=1.3,
                  path_effects=[path_effects_module.Stroke(linewidth=1.2, foreground='#FFFFFF'),
                                path_effects_module.Stroke(linewidth=0.6, foreground='#333333'),
                                path_effects_module.Normal()])
                                
    plt.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.93)
    output_file = 'mapa_producao_uva_regioes_2024_rotulos_ajustados.png'
    try:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Mapa por REGIÃO salvo como '{os.path.abspath(output_file)}'")
        plt.show()
    except Exception as e:
        print(f"Erro ao salvar ou mostrar o mapa por REGIÃO: {e}")

if __name__ == "__main__":
    geojson_file_path = download_geojson()
    if geojson_file_path:
        try:
            brazil_data = gpd.read_file(geojson_file_path)
            create_grape_production_map_by_state(brazil_data)
            create_grape_production_map_by_region(brazil_data)
        except Exception as e:
            print(f"Erro ao processar o arquivo GeoJSON ou gerar mapas: {e}")
    else:
        print("Download do GeoJSON falhou. Não é possível gerar os mapas.")