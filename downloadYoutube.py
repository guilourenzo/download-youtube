import streamlit as st
from pytube import YouTube
from PIL import Image
import requests
from io import BytesIO



url = st.text_input('Digite a url do site')
if len(url) < 1:
    url = 'https://www.youtube.com/watch?v=Yw6u6YkTgQ4'

yt = YouTube(url)
st.write('A url digitada é: ', url)

response = requests.get(yt.thumbnail_url)
thumb = Image.open(BytesIO(response.content))
st.image(thumb, caption=yt.title, use_column_width=True)

def getDetails(yt):
    st.write('Título: ', yt.title)
    st.write('Nº de Views: ', yt.views)
    st.write('Tamanho do Vídeo: ', yt.length)
    st.write('Classificação do Vídeo: ', yt.rating)
    ys = yt.streams.get_highest_resolution()

    return ys

if st.button('Download Vídeo'):
    with st.spinner('Baixando vídeo'):
        getDetails(yt).download()
        # ys.download()
    st.success('Vídeo baixado !')
else:
    st.warning('Clique para baixar')

