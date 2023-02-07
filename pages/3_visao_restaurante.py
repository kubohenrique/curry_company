# ==============================================================================
# LIBRARY
# ==============================================================================

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import folium
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Restaurante', page_icon='🧑🏻‍🍳', layout='wide')

# ==============================================================================
#                                  FUNCTIONS
# ==============================================================================

def clean_code(df1):
    
    """ Esta função tem como propósito limpar o data frame
        
        Tipo de limpeza:
        1. Remoção dos NaN
        2. Conversão do formato de algumas variáveis
        3. Remoção dos espacos existentes
        
        input: DataFrame
        output: DataFrame
        
    """
    
    # Converter a coluna Age para numero
    df1 = df1.loc[df1['Delivery_person_Age'] != 'NaN ', :]
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # Convertendo a Coluna Rating para Floar
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # Convertendo a coluna multiple_deliveries para numero
    df1 = df1.loc[df1['multiple_deliveries'] != 'NaN ', :]
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # Convertendo a coluna order date para o tipo datetime
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # Removendo os espaços
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # Removendo NaN
    df1 = df1.loc[df1['Road_traffic_density'] != "NaN", :]
    df1 = df1.loc[df1['City'] != "NaN", :]
    df1 = df1.loc[df1['Delivery_person_Ratings'] != "NaN ", :]
    df1 = df1.loc[df1['Festival'] != "NaN", :]

    # Criando a coluna semana 
    df1['week_of_year'] = df1['Order_Date'].dt.strftime("%U")

    # Tratando a coluna Time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1
#------------------------------------- Início da Estrutura Lógica ---------------------------------------------

# ==============================================================================
# IMPORTING DATA SET
# ==============================================================================

#df = pd.read_csv('/Users/henriquekubo/Documents/Repos/ftc_python/dataset/train.csv')
df = pd.read_csv('pages/train.csv')

# ==============================================================================
# CLEANING DATA SET
# ==============================================================================

df1 = clean_code(df)


# =======================================
# Barra Lateral
# =======================================

st.header( 'Marketplace - Visão Restaurantes' )

#image_path = '/Users/henriquekubo/Documents/Repos/ftc_python/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Selecione uma data limite' )

date_slider = st.sidebar.slider( 
    'Até qual valor?',
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime(2022, 2, 11 ),
    max_value=pd.datetime( 2022, 4, 6 ),
    format='DD-MM-YYYY' )

st.sidebar.markdown( """---""" )


traffic_options = st.sidebar.multiselect( 
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'], 
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )

# Filtro de data
linhas_selecionadas = df1['Order_Date'] <  date_slider 
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]

# =======================================
# Layout no Streamlit
# =======================================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'] )

with tab1:
    with st.container():
        st.title( "Overal Metrics" )
        
        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        with col1:
            delivery_unique = len( df1.loc[:, 'Delivery_person_ID'].unique() )
            col1.metric( 'Entregadores', delivery_unique )
                
        with col2:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply( lambda x: 
                                        haversine(  (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 )

            avg_distance = np.round( df1['distance'].mean(), 2 )
            col2.metric( 'A distancia media', avg_distance )

            
        with col3:
            df_aux = ( df1.loc[:, ['Time_taken(min)', 'Festival']]
                          .groupby( 'Festival' )
                          .agg( {'Time_taken(min)': ['mean', 'std']} ) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'], 2 )
            col3.metric( 'Tempo Médio', df_aux )

        with col4:
            df_aux = ( df1.loc[:, ['Time_taken(min)', 'Festival']]
                          .groupby( 'Festival' )
                          .agg( {'Time_taken(min)': ['mean', 'std']} ) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'Yes', 'std_time'], 2 )
            col4.metric( 'STD Entrega', df_aux )
            
        with col5:
            df_aux = ( df1.loc[:, ['Time_taken(min)', 'Festival']]
                          .groupby( 'Festival' )
                          .agg( {'Time_taken(min)': ['mean', 'std']} ) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'No', 'avg_time'], 2 )
            col5.metric( 'Tempo Médio', df_aux )
            
        with col6:
            df_aux = ( df1.loc[:, ['Time_taken(min)', 'Festival']]
                          .groupby( 'Festival' )
                          .agg( {'Time_taken(min)': ['mean', 'std']} ) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            df_aux = np.round( df_aux.loc[df_aux['Festival'] == 'No', 'std_time'], 2 )
            col4.metric( 'STD Entrega', df_aux )
    
    with st.container():
        st.markdown( """---""" )
        col1, col2 = st.columns( 2 )
        
        with col1:
            df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby( 'City' ).agg( {'Time_taken(min)': ['mean', 'std']} )
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig = go.Figure() 
            fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time']))) 
            fig.update_layout(barmode='group') 

            st.plotly_chart( fig )
            
        with col2:
            df_aux = ( df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                          .groupby( ['City', 'Type_of_order'] )
                          .agg( {'Time_taken(min)': ['mean', 'std']} ) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            st.dataframe( df_aux )
    
    with st.container():
        st.markdown( """---""" )
        st.title( "Distribuição do Tempo" )
        
        col1, col2 = st.columns( 2 )
        with col1:
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply( lambda x: 
                                        haversine(  (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude']) ), axis=1 )

            avg_distance = df1.loc[:, ['City', 'distance']].groupby( 'City' ).mean().reset_index()
            fig = go.Figure( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
            st.plotly_chart( fig )

            
        with col2:
            df_aux = ( df1.loc[:, ['City', 'Time_taken(min)', 'Road_traffic_density']]
                          .groupby( ['City', 'Road_traffic_density'] )
                          .agg( {'Time_taken(min)': ['mean', 'std']} ) )

            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()

            fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                              color='std_time', color_continuous_scale='RdBu',
                              color_continuous_midpoint=np.average(df_aux['std_time'] ) )
            st.plotly_chart( fig )
        
