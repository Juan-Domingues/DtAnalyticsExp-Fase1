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
        return 'white' if luminance < 0.4 else 'black'
    except ValueError:
        return default_color

# Dados de produção de uva 2024
grape_production_states_2024 = {
    'Rio Grande do Sul': 703022,
    'São Paulo': 144836,
    'Santa Catarina': 39927,
    'Paraná': 54700,
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

label_adjustments_siglas = { # Ajustes apenas para as siglas
    'DF': (0.2, 0.05, 6), 'SE': (0, 0, 6), 'AL': (0, 0, 6),
    'PB': (0, 0, 6), 'RN': (0, 0, 6), 'ES': (0, 0.05, 7),
    'RJ': (0, 0.05, 7),
}

def create_grape_production_map_by_state(brazil_gdf):
    """
    Cria e exibe o mapa de produção de UVA por ESTADO no Brasil para 2024,
    com legenda de dados ao lado e SEM colorbar.
    """
    print("\nGerando mapa de produção de uva por ESTADO com legenda de texto (sem colorbar)...")
    brazil_states_map_data = brazil_gdf.copy()

    brazil_states_map_data['grape_production_2024'] = 0
    cmap_plot = plt.cm.get_cmap('Purples')  # Alterado para roxo
    relevant_prod_values = [p for p in grape_production_states_2024.values() if p > 0]
    min_prod_val = 0
    max_prod_val = max(relevant_prod_values) if relevant_prod_values else 1
    norm = mcolors.Normalize(vmin=min_prod_val, vmax=max_prod_val)

    state_colors = {}
    for state_name, production in grape_production_states_2024.items():
        brazil_states_map_data.loc[brazil_states_map_data['name'] == state_name, 'grape_production_2024'] = production
        if production > 0:
            state_colors[state_name] = mcolors.to_hex(cmap_plot(norm(production)))
        else:
             state_colors[state_name] = "#B0B0B0"  # Cinza para zero

    fig, ax = plt.subplots(1, 1, figsize=(13, 12)) # Ajustado figsize
    
    plot_column = 'grape_production_2024'
    brazil_states_map_data.plot(column=plot_column,
                                ax=ax,
                                cmap=cmap_plot,
                                missing_kwds={"color": "#B0B0B0", "edgecolor": "#C0C0C0"},
                                edgecolor='#BDBDBD',
                                linewidth=0.6,
                                vmin=min_prod_val,
                                vmax=max_prod_val)

    ax.set_axis_off()
    ax.set_title('Produção de Uva por Estado - Brasil (2024)', fontsize=20, fontweight='bold', pad=10)
    
    for idx, row in brazil_states_map_data.iterrows():
        centroid = row['geometry'].centroid
        state_initials = row['sigla']
        production_value = row[plot_column]
        
        current_bg_color_hex = "#B0B0B0"
        if state_initials in state_colors and row['name'] in state_colors : 
            current_bg_color_hex = state_colors.get(row['name'], "#B0B0B0")
        elif production_value > 0 : 
             current_bg_color_hex = mcolors.to_hex(cmap_plot(norm(production_value)))

        text_color = get_text_color_for_bg(current_bg_color_hex)
        
        adj = label_adjustments_siglas.get(state_initials, (0, 0, 8)) 
        x_offset_sigla, y_offset_sigla, fontsize_sigla = adj
        
        ax.text(centroid.x + x_offset_sigla, centroid.y + y_offset_sigla, state_initials,
                  horizontalalignment='center', verticalalignment='center',
                  fontsize=fontsize_sigla, color=text_color, fontweight='bold',
                  path_effects=[path_effects_module.Stroke(linewidth=0.8, foreground='#FFFFFF'),
                                path_effects_module.Stroke(linewidth=0.4, foreground='#333333'),
                                path_effects_module.Normal()])
                                
    legend_elements = []
    sorted_production_states = sorted(grape_production_states_2024.items(), key=lambda item: item[1], reverse=True)

    for state_name, production in sorted_production_states:
        if production > 0:
            color = state_colors.get(state_name, "#808080") 
            label = f"{state_name}: {int(production):,} t".replace(",",".")
            legend_elements.append(Patch(facecolor=color, edgecolor='#555555', label=label))

    if legend_elements:
        leg = ax.legend(handles=legend_elements,
                        title="Produtores (Uva 2024)",
                        loc='center left', 
                        bbox_to_anchor=(1.02, 0.5),
                        fontsize=9,
                        title_fontsize=11,
                        frameon=True,
                        facecolor='white',
                        edgecolor='grey',
                        framealpha=0.9)
        leg.get_title().set_fontweight('bold')

    plt.subplots_adjust(left=0.02, right=0.75, bottom=0.05, top=0.93)
    output_file = 'mapa_producao_uva_estados_sem_colorbar.png'
    try:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Mapa por ESTADO salvo como '{os.path.abspath(output_file)}'")
        plt.show()
    except Exception as e:
        print(f"Erro ao salvar ou mostrar o mapa por ESTADO: {e}")

def create_grape_production_map_by_region(brazil_gdf):
    """
    Cria e exibe o mapa de produção de UVA por REGIÃO no Brasil para 2024,
    SEM colorbar.
    """
    print("\nGerando mapa de produção de uva por REGIÃO (sem colorbar)...")
    brazil_regions_map_data = brazil_gdf.copy()
    
    brazil_regions_map_data['regiao'] = brazil_regions_map_data['name'].map(state_to_region_map)
    regions_gdf = brazil_regions_map_data.dissolve(by='regiao', aggfunc='sum')
    
    regions_gdf['grape_production_2024'] = 0
    for region_name, production in grape_production_regions_2024.items():
        if region_name in regions_gdf.index:
            regions_gdf.loc[region_name, 'grape_production_2024'] = production
    
    fig, ax = plt.subplots(1, 1, figsize=(13, 12))
    
    cmap_regions = plt.cm.get_cmap('Purples')  # Alterado para roxo
    relevant_prod_regions = regions_gdf[regions_gdf['grape_production_2024'] > 0]['grape_production_2024']
    min_prod_region_val = 0
    max_prod_region_val = relevant_prod_regions.max() if not relevant_prod_regions.empty else 1
    norm_regions = mcolors.Normalize(vmin=min_prod_region_val, vmax=max_prod_region_val)

    regions_gdf.plot(column='grape_production_2024',
                     ax=ax,
                     cmap=cmap_regions, 
                     missing_kwds={"color": "#B0B0B0", "edgecolor": "#C0C0C0"},
                     edgecolor='#777777',
                     linewidth=1.2,
                     vmin=min_prod_region_val,
                     vmax=max_prod_region_val)
    
    ax.set_axis_off()
    ax.set_title('Produção de Uva por Região - Brasil (2024)', fontsize=20, fontweight='bold', pad=10)

    for region_name, row in regions_gdf.iterrows():
        representative_point = row['geometry'].representative_point()
        production_value = row['grape_production_2024']
        
        current_bg_color_hex = "#B0B0B0"
        if pd.notna(production_value) and production_value > 0 :
            current_bg_color_rgba = cmap_regions(norm_regions(production_value))
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
                                
    plt.subplots_adjust(left=0.02, right=0.95, bottom=0.05, top=0.93)
    output_file = 'mapa_producao_uva_regioes_sem_colorbar.png'
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