# scripts/auth.py
import json
import streamlit as st
import os

def load_server_credentials():
    credentials_path = os.path.join("data", "credentials.json")
    try:
        with open(credentials_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar as credenciais do servidor: {e}")
        return None

def login_screen():
    st.title("Login")
    server_creds = load_server_credentials()
    if server_creds is None:
        st.error("Credenciais do servidor não configuradas. Contate o administrador.")
        st.stop()
    
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")
    
    if submit:
        if username == server_creds.get("username") and password == server_creds.get("password"):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login realizado com sucesso!")
            st.rerun()  # Atualiza a página para remover a tela de login
        else:
            st.error("Credenciais inválidas!")

def ensure_login():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login_screen()
        if "logged_in" not in st.session_state or not st.session_state.logged_in:
            st.stop()
