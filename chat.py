# Titulo
# Input do chat (campo de mensagem)
# a cada mensagem que o usuario enviar: 
    # mostrar a mensagem que o usuario enviou no chat
    # pegar a pergunta e enviar para uma IA responder
    # exibir a resposta da IA na tela

# Streamlit - apenas com o Python criar o frontend e o backend do site
# a IA que vamos usar: OpenIA ou Gemini
# pip install openai streamlit

from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

modelo_ia = genai.GenerativeModel('models/gemini-2.5-flash')

st.write('# Chatbot do Lázin!') # markdown

# Cabeçalho
st.header('*Tire as suas Dúvidas aqui!*')
st.sidebar.header('Opções de aplicação')
nome = st.sidebar.text_input(label='Digite o seu nome: ')
st.sidebar.write('Olá, {}!\nTudo bem?? Seja Bem-Vindo ao Chatbot'.format(nome))


def reset_chat():
    st.session_state.chat = modelo_ia.start_chat(history=[])
    # Se você mantiver a lista_mensagens, também precisaria limpá-la:
    # st.session_state['lista_mensagens'] = []
    st.experimental_rerun() # Para recarregar a página e mostrar o chat limpo

st.sidebar.button('Reiniciar Chat', on_click=reset_chat)

if not 'lista_mensagens' in st.session_state:
    st.session_state['lista_mensagens'] = [] # são os cookies do site

if 'chat' not  in st.session_state:
    st.session_state.chat = modelo_ia.start_chat(history=[]) 

texto_usuario = st.chat_input('Digite sua mensagem')

for mensagem in st.session_state['lista_mensagens']:
    role = mensagem['role']
    content = mensagem['parts'][0]
    if role == 'model':
        role = 'assistant'

    st.chat_message(role).write(content)

if texto_usuario:
    st.chat_message('user').write(texto_usuario)
    mensagem_usuario = {'role': 'user', 'parts': [texto_usuario]}
    st.session_state['lista_mensagens'].append(mensagem_usuario)

    # ia respondeu
    with st.spinner("A IA está pensando..."):
        resposta_ia = st.session_state.chat.send_message(texto_usuario)
    texto_resposta_ia = resposta_ia.text
    st.chat_message('assistant').write(texto_resposta_ia)
    mensagem_ia = {'role': 'assistant', 'parts': [texto_resposta_ia]}
    st.session_state['lista_mensagens'].append(mensagem_ia)
