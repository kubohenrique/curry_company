import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'home',
    page_icon = '📈')

#image_path = '/Users/henriquekubo/Documents/Repos/ftc_python/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=200 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.markdown('# Cury Company Dashboard')

st.markdown(
    """ 
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    ### Como utilizar o Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas Gerais de comportamento
        - Visão Tática: Indicadores Semanais de Crescimento
        - Visão Geográfica: Insights de Geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for Help
    - Henrique @kubohenrique
    
    """)