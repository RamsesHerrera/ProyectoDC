import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.style as style
import geopandas as gpd
import matplotlib.colors as mcolors
from datetime import datetime
import os
import plotly.express as px




#Funcion para graficar barras
def graficar_barras(dataframe, titulo, columna_x,columna_y, nombre_x, nombre_y, tipo_grafica, limite):

    #colores = ['blue', 'green', 'red', 'purple', 'orange', 'yellow', 'cyan', 'magenta', 'brown', 'gray']
    colores = plt.cm.viridis(np.linspace(0, 1, len(dataframe)))


    grafica = dataframe.plot(kind=tipo_grafica, x=columna_x, y=columna_y,figsize=(10, 8),legend=False, color= colores)
    
    # Agregar título y etiquetas de los ejes
    grafica.set_title(titulo)
    grafica.set_xlabel(nombre_x)
    grafica.set_ylabel(nombre_y)

    # Establecer un límite en el eje x
    limite_x = limite  # El límite en el eje x (se agrega parametro para ajustar segun el requerimento de los datos)
    plt.xlim(-0.5, limite_x - 0.5)  # Ajustar los límites del eje x para crear espacio entre las barras
    
    plt.ticklabel_format(style='plain', axis='x')

    for index, value in enumerate(dataframe[columna_y]):
        grafica.text(value, index, str(value), ha='left', va='center')

    plt.tight_layout()  # Ajustar el diseño de la figura para que quepan todas las etiquetas


    plt.show()

# Fuente para el mapeo USA:https://catalog.data.gov/dataset/tiger-line-shapefile-current-nation-u-s-state-and-equivalent-entities



def print_map_usa(dataframe, name_state, count, title_map):
    
    #Importamos el shap descargado para mapear los estados 
    URL="C:/Users/20140/OneDrive/Documentos/GitHub/ciencia-datos-iec-RamsesHerrera/AD-ProyectoFinal/tl_2023_us_state/tl_2023_us_state.shp"
    usa = gpd.read_file(URL)
    #asignamos color al mapa
    color_map='GnBu'
    
    # Unimos los estados USA con los estados de mi data frame
    merged = usa.set_index('NAME').join(dataframe.set_index(name_state))
    
    # Calcula el tamaño
    minx, miny, maxx, maxy = merged.total_bounds
    
    # Crea el mapa 
    fig, ax = plt.subplots(figsize=(18, 17))
    merged.plot(column=count, cmap=color_map, linewidth=0.8, ax=ax, edgecolor='0.8', legend=False)
    
    # Limites de USA
    ax.set_xlim(minx +55, maxx - 245)
    ax.set_ylim(miny +12 , maxy - 20)
    
    # titulo
    ax.set_title(title_map, pad=0)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Ajusta estos valores según tus necesidades
    
    # Color 
    ax.axis('off')
    norm = mcolors.Normalize(vmin=merged[count].min(), vmax=merged[count].max())
    sm = plt.cm.ScalarMappable(cmap=color_map, norm=norm)
    cbar = fig.colorbar(sm,shrink=0.9,pad=0, aspect=25, location='left')
    cbar.ax.set_anchor((0.0, 1.2))
    plt.show()

#Realiza una union para graficar el dataframe guardado como .pickle
def graficar_modulo(dataframe_name,titulo1, columna_x1,columna_y1, nombre_x1, nombre_y1, tipo_grafica1, limite1):

    URL= 'Mi_modulo/'
    extencion = '.pickle'
    direccion_completa = os.path.join(URL,dataframe_name + extencion)

    dataframe_name = pd.read_pickle(direccion_completa)

    graficar_barras(dataframe_name, titulo1, columna_x1,columna_y1, nombre_x1, nombre_y1, tipo_grafica1, limite1)
    
#Realiza una union para graficar el dataframe guardado como .pickle
def graficar_modulo_mapa(dataframe_name, name_state, count, title_map):

    URL= 'Mi_modulo/'
    extencion = '.pickle'
    direccion_completa = os.path.join(URL,dataframe_name + extencion)

    dataframe_name = pd.read_pickle(direccion_completa)

    print_map_usa(dataframe_name, name_state, count, title_map)

    # Graficar con Plotly


def plotly_duble(dataframe, ejex, ejey, ejexlabel, ejeylabel, Title, color):

    dataframe = direcciones(dataframe)
        
    fig = px.bar(dataframe, x=ejex, y=ejey, title=Title)
        
     # Ajustar el ancho de las barras
    fig.update_traces(width=0.4, marker_color=color)  # Puedes ajustar el valor de width según tus necesidades
        # Ajustar el tamaño de la figura
    fig.update_layout(width=900, height=700)
        
    # Asignar nombres a las etiquetas de los ejes x y y
    fig.update_layout(
            xaxis_title=ejexlabel, yaxis_title=ejeylabel
        )
        
    fig.show()






def filtrar_df_por_estado(df_a_filtrar, abreviacion_state, columna_state, columna_grupo):
    #filtramos el dataframe por el estado de Texas, en esta parte ignore valores null
    
    df_edades = df_a_filtrar.loc[df_a_filtrar[columna_state] == abreviacion_state]
    

    #Procesamos el dataframe para California y poder graficarlo
    df_edades = df_edades[columna_grupo].value_counts()
        #Pasamos la serie a dataframe
    df_edades = pd.DataFrame(df_edades)
        #Reset index
    df_edades.reset_index(inplace=True)
    return df_edades


def pastel_1vs1():
    total_usuarios = 92432
    usuarios_registrados = 31773
    usuarios_no_registrados = total_usuarios - usuarios_registrados

    # Crear un DataFrame con los datos
    data = {
        'Tipo de Usuario': ['Identidad completada', 'No completada'],
        'Cantidad': [usuarios_registrados, usuarios_no_registrados]
    }

    df = pd.DataFrame(data)

    # Crear la gráfica de pastel
    fig = px.pie(df, names='Tipo de Usuario', values='Cantidad', title='Usuarios con identidad completada vs no completada - California')

    fig.update_layout(
        width=800,  # Ajusta el ancho
        height=600  # Ajusta la altura
    )
    # Mostrar la gráfica
    fig.show()

def pastel_genero(df,nombre_categoria, cantidades, Title, color1,color2):

    dataframe = direcciones(df)

    fig = px.pie(dataframe, names=nombre_categoria, values=cantidades, title=Title,color_discrete_sequence=[color1,color2])
    fig.update_layout(
        width=800,  # Ajusta el ancho
        height=600  # Ajusta la altura
    )
    # Mostrar la gráfica
    fig.show()

def direcciones(dataframe):

    URL= 'Mi_modulo/'
    extencion = '.pickle'
    direccion_completa = os.path.join(URL,dataframe + extencion)

    dataframe = pd.read_pickle(direccion_completa)
    return dataframe

def distribucion_male_female(dataframe, ejex,ejey, color_colum, title, ejey_label, ejex_label):

    dataframe = direcciones(dataframe)

    fig = px.bar(dataframe, x=ejex, y=ejey, color=color_colum, 
             title=title,
             labels={ejey: ejey_label, ejex: ejex_label},
             barmode='group',  # Para agrupar las barras por género dentro de cada rango de edad
             color_discrete_sequence=px.colors.qualitative.Pastel)

    fig.update_xaxes(categoryorder='total descending')
    # Mostrar la gráfica
    fig.show()

def multiples_barras_plotly(dataframe, ejex, ejey, color_colum, sub_colum, title, ejexlabel, ejeylabel):

    dataframe = direcciones(dataframe)

    fig = px.bar(dataframe, x=ejex, y=ejey, color=color_colum,
             facet_row=sub_colum,  # Crear subgráficas por estado civil
             title=title,
             labels={ejey: ejeylabel, ejex: ejexlabel},
             barmode='group',  # Para agrupar las barras por género dentro de cada rango de edad
             color_discrete_sequence=px.colors.qualitative.Pastel,height=1500)

    # Mostrar la gráfica
    fig.show()