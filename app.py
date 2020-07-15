# Importação das bibliotecas
import streamlit as st
from pytube import YouTube, Stream
from PIL import Image
import requests
from io import BytesIO
from hurry.filesize import size

@st.cache()
def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%d:%02d:%02d" % (hour, min, sec) 

# Função para exibição dos detalhes e download do vídeo
def getDetails(yt):
    st.write('**Título:** ', yt.title)
    st.write('**Autor:** ', yt.author)
    st.write('**Descrição do vídeo:**')
    st.write(yt.description)
    st.write('**Nº de Views:** {:,}'.format(yt.views).replace(',','.'))
    st.write('**Tempo de Vídeo:** ', convert(yt.length))
    st.write('**Classificação do Vídeo:** {:.2f}'.format(yt.rating))
    
    ys = yt.streams

    # st.write('**Tamanho aprox.:** ', size(ys.filesize_approx))
    
    versoes = {}
    for versao in yt.streams.filter(file_extension='mp4', progressive=True):
        if versao.resolution is not None:
            versoes[versao.itag] = versao.resolution

    return ys, versoes

# Função para baixar o vídeo na qualidade selecionada
@st.cache()
def downloadVersoes(detail, versao):
    dwn = detail.get_by_itag(versao)
    dwn.download()

def listaVersoes(versoes):
    tmp = []
    for chave, valor in opcoes.items():
        tmp.append(valor)

    opcao = st.selectbox('Selecione uma Qualidade de Vídeo:', tmp)
    selecao = [key for (key,value) in opcoes.items() if value in opcao]

    return selecao[0]

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

# Exibe os detalhes do vídeo e as opções de qualidade
with st.spinner('Buscando detalhes do vídeo'):
    details, opcoes = getDetails(yt)
    
    versao = listaVersoes(opcoes)


# Função do botão de Download
if st.button('Download Vídeo'):
    with st.spinner('Baixando vídeo'):
        downloadVersoes(details, versao)

    st.success('Vídeo baixado !')
    st.balloons()
else:
    st.warning('Clique para baixar')

