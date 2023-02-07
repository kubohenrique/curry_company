# =======================================
# LIBRARY
# =======================================

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from PIL import Image

from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Empresa', page_icon='👁️', layout='wide')

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
#-------------------------------------------------------------------------------------------------------------    
def order_day(fig):
    # Quantidade de pedidos por dia
    aux1 = df1[['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    aux1.columns = ['data_pedido', 'qtde_pedido']

    # Grafico
    fig = px.bar(aux1, x='data_pedido', y='qtde_pedido')

    return fig
#-------------------------------------------------------------------------------------------------------------

def order_trafic(df1):
    # Quantidade de pedidos por trafego
    aux3 = df1[['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    aux3 = aux3.loc[aux3['Road_traffic_density'] != 'NaN', :]

    # Achar a porcentagem para fazer o grafico de pizza
    aux3['porcentagem'] = 100 * (aux3['ID'] / aux3['ID'].sum())

    # O Grafico de Pizza
    fig = px.pie( aux3, values='porcentagem', names='Road_traffic_density')

    return fig
#-------------------------------------------------------------------------------------------------------------

def mapas_(df1):
    aux6 = df1[['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()

    map = folium.Map()

    for i, location in aux6.iterrows():
        folium.Marker([location['Delivery_location_latitude'], location['Delivery_location_longitude']], popup = location[['City', 'Road_traffic_density']]).add_to(map)

        folium_static(map, width=1024, height=600) 

    return None
    
#------------------------------------- Início da Estrutura Lógica ---------------------------------------------

# ==============================================================================
# IMPORTING DATA SET
# ==============================================================================

#df = pd.read_csv('/Users/henriquekubo/Documents/Repos/ftc_python/dataset/train.csv'
# /Users/henriquekubo/Documents/Repos/ftc_python/dataset)
df = pd.read_csv('pages/train.csv')

# ==============================================================================
# CLEANING DATA SET
# ==============================================================================

df1 = clean_code(df)

# ==============================================================================
# Barra Lateral
# ==============================================================================
st.header( 'Marketplace - Visão Empresa' )

#image_path = '/Users/henriquekubo/Documents/Repos/ftc_python/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=200 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Selecione uma data limite' )

date_slider = st.sidebar.slider( 
    'Até qual valor?',
    value=pd.datetime( 2022, 3, 13 ),
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


# =====================================================================================================================
# Layout no Streamlit
# =====================================================================================================================
tab1, tab2, tab3 = st.tabs( ['Visão de Planejamento', 'Visão estratégica', 'Visão geográfica'] )

with tab1:
    
    with st.container():
        st.header('Orders by Day')
        
        fig = order_day(df1)
        st.plotly_chart(fig, user_container_width=True)
        
       
    # Criando duas colunas na linha 2 da visulização
    
    with st.container():
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('Orders by Traffic') 
            fig = order_trafic(df1)
            st.plotly_chart(fig, user_container_width=True)
            
            

        with col2:
            st.markdown('Volum by City') 
            aux4 = df1[['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()

            fig = px.scatter(aux4, 'City', 'Road_traffic_density', size='ID', color = 'City')
            st.plotly_chart(fig, user_container_width=True)
    
with tab3:
    
    st.header('Mapa')
    
    mapas_(df1)
    
    