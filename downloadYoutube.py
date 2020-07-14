# Importação das bibliotecas
import streamlit as st
from pytube import YouTube
from PIL import Image
import requests
from io import BytesIO

# Captura da URL digitada
url = st.text_input('Digite a url do site')

# Caso não tenha sido digitada uma URL um link padrão é carregado
if len(url) < 1:
    url = 'https://www.youtube.com/watch?v=Yw6u6YkTgQ4'

# Realiza a leitura do link
yt = YouTube(url)
st.write('A url digitada é: ', url)

# Exibe o Thumbnail do Vídeo
response = requests.get(yt.thumbnail_url)
thumb = Image.open(BytesIO(response.content))
st.image(thumb, caption=yt.title, use_column_width=True)

# Função para exibição dos detalhes e download do vídeo
def getDetails(yt):
    st.write('Título: ', yt.title)
    st.write('Nº de Views: ', yt.views)
    st.write('Tamanho do Vídeo: ', yt.length)
    st.write('Classificação do Vídeo: ', yt.rating)
    ys = yt.streams.get_highest_resolution()

    return ys

# Função do botão de Download
if st.button('Download Vídeo'):
    with st.spinner('Baixando vídeo'):
        getDetails(yt).download()
        # ys.download()
    st.success('Vídeo baixado !')
else:
    st.warning('Clique para baixar')

