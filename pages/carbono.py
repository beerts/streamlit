import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# DANDO NOME E ÍCONE À PÁGINA
st.set_page_config(
    layout="wide", 
    page_icon='images/Araguaia Negativa sem escrita_250x160.png',
    page_title='ANÁLISE CARBOMAX'
    
)

# TÍTULO
st.title("CARBONO") 
st.logo('images/Araguaia Negativa sem escrita_250x160.png')


# VARIÁVEL DE COLUNAS    
LOTE_COLUMN = 'LOTE'
CARBONO_COLUMN = 'CARBONO'
MATERIAL_COLUMN = 'MATERIAL'
SILICIO_COLUMN = 'SILICIO'

# FUNÇÃO DE CARREGAR DADOS
def load_data(file_path, sheet_name=None, nrows=None):
    # Carregando dados do Excel
    data = pd.read_excel(file_path, sheet_name=sheet_name, nrows=nrows)

    # SIDEBAR COM SELEÇÃO
    with st.sidebar:
        # Selecionar mês
        mes_unico = data['MÊS'].unique().tolist()
        selecionar_mes = st.selectbox("MÊS", mes_unico)
        if selecionar_mes:
            data = data[data['MÊS'] == selecionar_mes]

        # Seleção dia
        dias_unicos = data['Dia'].unique().tolist()
        selecionar_dia = st.selectbox("DIA", dias_unicos)   
        if selecionar_dia:
            data = data[data['Dia'] == selecionar_dia]

        # Seleção material
        material_todos = ['Todos'] + data['Material'].unique().tolist() 
        selecionar_material = st.selectbox("MATERIAL", material_todos)   
        if selecionar_material and selecionar_material != 'Todos':
            data = data[data['Material'] == selecionar_material]

    # Removendo colunas desnecessárias
    data.drop(columns=['IP', 'Equipamento', 'Canal','Dt Início','Pico','tag1','tag2','tag3','tag4'], inplace=True)
    
    # RENOMEANDO COLUNAS PARA MAIÚSCULAS
    lowercase = lambda x: str(x).upper()
    data.rename(lowercase, axis='columns', inplace=True)

    return data, selecionar_dia, selecionar_mes, selecionar_material

# Carregando dados
file_path = 'C:/Users/ARA002980/Desktop/fusao/DADOS FUSÃO.xlsx'
sheet_name = 'Carbono'
data, selecionar_dia, selecionar_mes, selecionar_material = load_data(file_path, sheet_name=sheet_name, nrows=10000)

# Agrupando por 'lote' e 'material'
grouped_data = data.groupby([LOTE_COLUMN, MATERIAL_COLUMN])[CARBONO_COLUMN].mean().reset_index()
grouped_data1 = data.groupby([LOTE_COLUMN, MATERIAL_COLUMN])[SILICIO_COLUMN].mean().reset_index()

# Função para criar gráficos com rótulos de dados e cores específicas
def plot_bar_with_labels(data, x_column, y_column, title, color_map):
    # Configurando a cor de fundo da figura
    plt.figure(figsize=(12, 8))
    plt.gca().set_facecolor('#2b2b2b')  # Cor de fundo do gráfico
    plt.gcf().set_facecolor('#2b2b2b')  # Cor de fundo da área da figura

    # Criar barras e legenda
    for material, color in color_map.items():
        subset = data[data[MATERIAL_COLUMN] == material]
        plt.bar(subset[x_column], subset[y_column], color=color, label=material)

    # Adicionando rótulos de dados nas barras
    for i, row in data.iterrows():
        plt.text(row[x_column], row[y_column], f'{row[y_column]:.2f}', ha='center', va='bottom', fontsize=10, color='#f0f0f0')

    # Configurando cores de títulos e rótulos dos eixos
    plt.xlabel(x_column, color='#f0f0f0')
    plt.ylabel(y_column, color='#f0f0f0')
    plt.title(title, color='#f0f0f0')
    
    # Ajustando a cor dos rótulos dos ticks dos eixos
    plt.xticks(rotation=45, color='#f0f0f0')
    plt.yticks(color='#f0f0f0')
    
    # Adicionando legenda
    plt.legend(loc='upper left', frameon=False, fontsize=10, labelcolor='white')
    plt.ylim(0, data[y_column].max() * 1.2)

    plt.tight_layout()
    st.pyplot(plt)

# Mapeamento de cores para materiais
unique_materials = grouped_data[MATERIAL_COLUMN].unique()
colors = plt.cm.tab10(range(len(unique_materials)))  # Use uma colormap padrão
color_map = dict(zip(unique_materials, colors))

# Exibindo gráfico de barras com rótulos de dados e legenda
st.subheader(f'ANÁLISE CARBONO (% C)\n{selecionar_dia}/{selecionar_mes}\n')
plot_bar_with_labels(grouped_data, LOTE_COLUMN, CARBONO_COLUMN, f'Análise de Carbono (%) {selecionar_material}', color_map)

st.subheader(f'ANÁLISE SILÍCIO\n{selecionar_dia}/{selecionar_mes}\n')
plot_bar_with_labels(grouped_data1, LOTE_COLUMN, SILICIO_COLUMN, f'Análise de Silício (%) {selecionar_material}', color_map)
