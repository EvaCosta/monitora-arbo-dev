import streamlit as st
import streamlit.components.v1 as components
from process_data import processar_arquivos
import pyrebase
import pandas as pd
import base64
import os
import plotly.express as px
import shutil
firebaseConfig = {
    "apiKey": "AIzaSyDjeRvV8yHAUmzDbiv2laM5tVM5iFXBByw",
    "authDomain": "monitora-arbo.firebaseapp.com",
    "projectId": "monitora-arbo",
    "storageBucket": "monitora-arbo.appspot.com",
    "messagingSenderId": "401575058454",
    "appId": "1:401575058454:web:52475e9a1be4acfe4fa937",
    "measurementId": "G-2CBGBT9JHG",
    "databaseURL": "https://monitora-arbo.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Definindo diretamente o email do usuário (substitua pelo e-mail desejado)
user_email = "seu_email@exemplo.com"  # Substitua com o e-mail que deseja utilizar

# def login():
    # st.title("🔐 Login - Monitora Arboviroses")
    # email = st.text_input("Email")
    # password = st.text_input("Senha", type="password")
    # login_button = st.button("Entrar")

    # if login_button:
    #     try:
    #         user = auth.sign_in_with_email_and_password(email, password)
    #         st.session_state['user'] = user
    #         st.session_state['email'] = email
    #         st.session_state['refreshToken'] = user['refreshToken']
    #         st.success(f"Bem-vindo, {email}!")
    #         st.experimental_rerun()
    #     except Exception as e:
    #         st.error("Email ou senha inválidos.")

# Função para download estilizado
def download_dataframe(df, filename, label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'''
    <a href="data:file/csv;base64,{b64}" download="{filename}">
        <button style="
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 12px;
            cursor: pointer;">
            ⬇️ {label}
        </button>
    </a>
    '''
    st.markdown(href, unsafe_allow_html=True)
def apagar_dados():
    try:
        shutil.rmtree("dados_salvos")
        shutil.rmtree("temp_upload")
        os.makedirs("dados_salvos", exist_ok=True)
        os.makedirs("temp_upload", exist_ok=True)
        st.success("✅ Todos os dados foram apagados com sucesso.")
    except Exception as e:
        st.error(f"❌ Erro ao apagar os dados: {e}")

def processamento(user_email):
    st.title("📊 Painel de Dados")

    if user_email == "vigilanciaepidemiologicadsvii@gmail.com":
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("🗑️ Apagar dados"):
                apagar_dados()
    
    pasta_dados = "dados_salvos"
    os.makedirs(pasta_dados, exist_ok=True)
    
    # Sempre mostra o upload
    if user_email != "vigilanciaambientalds7@gmail.com":
        uploaded_files = st.file_uploader("📂 Envie um ou mais arquivos .xls ou .ods", type=["xls", "ods"], accept_multiple_files=True)
    else:
        st.info("Você tem acesso apenas para visualização dos dados.")
        uploaded_files = None
   
    pasta_temp = "temp_upload"
    os.makedirs(pasta_temp, exist_ok=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            caminho = os.path.join(pasta_temp, uploaded_file.name)
            with open(caminho, "wb") as f:
                f.write(uploaded_file.getbuffer())

        try:
            df_ve, df_va, df_casos_sem_encerramento = processar_arquivos(pasta_temp)

            if user_email == "vigilanciaepidemiologicadsvii@gmail.com":
                df_ve.to_excel(os.path.join(pasta_dados, "chico_filtrado_ve.xlsx"), index=False, engine='openpyxl')
                df_va.to_excel(os.path.join(pasta_dados, "chico_filtrado_va.xlsx"), index=False, engine='openpyxl')
                df_casos_sem_encerramento.to_excel(os.path.join(pasta_dados, "casos_sem_encerramento.xlsx"), index=False, engine='openpyxl')
                st.success("Arquivos processados e salvos com sucesso!")
            else:
                st.info("Arquivos processados apenas para visualização. Nenhum dado foi salvo permanentemente.")

            st.subheader("🦠 Casos dos Últimos 60 Dias (VE)")
            st.dataframe(df_ve)
            download_dataframe(df_ve, "chico_filtrado_ve.csv", "Download VE")

            st.subheader("🦠 Casos dos Últimos 30 Dias (VA)")
            st.dataframe(df_va)
            download_dataframe(df_va, "chico_filtrado_va.csv", "Download VA")

            st.subheader("🦠 Casos sem encerramento")
            st.dataframe(df_casos_sem_encerramento)
            download_dataframe(df_casos_sem_encerramento, "casos_sem_encerramento.csv", "Casos sem encerramento")

        except Exception as e:
            st.error(f"Erro ao processar os arquivos: {e}")

    # Se não houver upload, exibe os dados salvos para os usuários que podem ver
    elif user_email in ["vigilanciaambientalds7@gmail.com", "vigilanciaepidemiologicadsvii@gmail.com"]:
        try:
            if user_email == "vigilanciaambientalds7@gmail.com":
                df_va = pd.read_excel(os.path.join(pasta_dados, "chico_filtrado_va.xlsx"))
                st.subheader("🦠 Casos dos Últimos 30 Dias (VA)")
                st.dataframe(df_va)
                download_dataframe(df_va, "chico_filtrado_va.csv", "Download VA")
            elif user_email == "vigilanciaepidemiologicadsvii@gmail.com":
                df_ve = pd.read_excel(os.path.join(pasta_dados, "chico_filtrado_ve.xlsx"))
                st.subheader("🦠 Casos dos Últimos 60 Dias (VE)")
                st.dataframe(df_ve)
                download_dataframe(df_ve, "chico_filtrado_ve.csv", "Download VE")

            
            st.subheader("🦠 Casos sem encerramento")
            df_casos_sem_encerramento = pd.read_excel(os.path.join(pasta_dados, "casos_sem_encerramento.xlsx"))
            st.dataframe(df_casos_sem_encerramento)
            download_dataframe(df_casos_sem_encerramento, "casos_sem_encerramento.csv", "Casos sem encerramento")
        except Exception:
            st.warning("Nenhum dado salvo foi encontrado.")

# Função de painel admin (se precisar de um painel de admin)
def admin_panel():
    if st.button("Cadastrar Novo Usuário ➕"):
        st.session_state.show_register = True

    if st.session_state.show_register:
        st.subheader("👤 Cadastro de Novo Usuário")
        new_email = st.text_input("Novo email")
        new_password = st.text_input("Nova senha", type="password")

        if st.button("Cadastrar novo usuário"):
            try:
                auth.create_user_with_email_and_password(new_email, new_password)
                st.success(f"Usuário {new_email} criado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao criar usuário: {e}")


def logout():
    if st.sidebar.button("🔒 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

if 'user' not in st.session_state and 'refreshToken' in st.session_state:
    try:
        user = auth.refresh(st.session_state['refreshToken'])
        st.session_state['user'] = user
        if 'email' not in st.session_state:
            # Tenta recuperar o email a partir do idToken
            user_info = auth.get_account_info(user['idToken'])
            st.session_state['email'] = user_info['users'][0]['email']
    except Exception:
        st.warning("Sessão expirada. Faça login novamente.")
        # login()
        st.stop()



if 'user' not in st.session_state:
    processamento(user_email);
    # login()
else:
    logout()
    processamento(st.session_state['email'])
# Chamando a função de processamento com o e-mail diretamente
# processamento(user_email)
