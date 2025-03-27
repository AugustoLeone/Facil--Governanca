import streamlit as st
import json
import os
from time import sleep
import bcrypt

# Caminho do arquivo JSON
FUNCIONARIOS_DB = "funcionarios.json"

# Lista de cargos possíveis
todos_cargos = ('Desenvolvedor', 'Diretor', 'Financeiro', 'RH', 'Coordenador', 'Administrativo', 'Pelador', 'Professor', 'Monitor')

# Inicializar estado da página
if "funcionarios_view" not in st.session_state:
    st.session_state.funcionarios_view = None

# Função para carregar os dados do JSON
def carregar_dados():
    if not os.path.exists(FUNCIONARIOS_DB):
        return []
    with open(FUNCIONARIOS_DB, "r", encoding="utf-8") as f:
        return json.load(f)

# Função para salvar os dados no JSON
def salvar_dados(dados):
    with open(FUNCIONARIOS_DB, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

# Função para criptografar a senha
def criptografar_senha(senha):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Validação de e-mail
def verifica_email(email):
    if email.count("@") != 1 or " " in email or not email.split("@")[1].count("."):
        return None
    return email

# Validação de CPF
def verifica_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
    if not cpf.isdigit() or len(cpf) != 11 or cpf == cpf[0] * 11:
        return None
    return cpf

# Formulário para cadastrar funcionário
def cadastrar_funcionario_form():
    with st.form("Cadastro de Funcionário", clear_on_submit=True):
        nome = st.text_input("Nome")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        email = st.text_input("E-mail")
        cpf = st.text_input("CPF")
        cargo = st.selectbox("Cargo", todos_cargos)
        salario = st.number_input("Salário", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Cadastrar")
        
        if submitted:
            if not verifica_email(email):
                st.error("E-mail inválido!")
                return
            if not verifica_cpf(cpf):
                st.error("CPF inválido!")
                return
            
            senha_criptografada = criptografar_senha(senha)
            dados = carregar_dados()
            dados.append({"nome": nome, "usuario": usuario, "senha": senha_criptografada, "email": email, "cpf": cpf, "cargo": cargo, "salario": salario})
            salvar_dados(dados)
            st.success("Funcionário cadastrado com sucesso!")
            sleep(2)
            st.session_state.funcionarios_view = None

# Formulário para modificar funcionário
def modificar_funcionario_form():
    dados = carregar_dados()
    nomes = [func["nome"] for func in dados]
    
    if not nomes:
        st.warning("Nenhum funcionário cadastrado.")
        return
    
    nome = st.selectbox("Selecione o funcionário", nomes)
    usuario = st.text_input("Novo usuário")
    senha = st.text_input("Nova senha", type="password")
    email = st.text_input("Novo e-mail")
    cpf = st.text_input("Novo CPF")
    cargo = st.selectbox("Novo Cargo", todos_cargos)
    salario = st.number_input("Novo Salário", min_value=0.0, format="%.2f")
    
    if st.button("Modificar", key=f"modificar_{nome}"):
        for func in dados:
            if func["nome"] == nome:
                func.update({
                    "usuario": usuario,
                    "senha": criptografar_senha(senha) if senha else func["senha"],
                    "email": email,
                    "cpf": cpf,
                    "cargo": cargo,
                    "salario": salario
                })
                salvar_dados(dados)
                st.success("Funcionário atualizado!")
                sleep(2)
                st.session_state.funcionarios_view = None
                return
        st.error("Funcionário não encontrado!")

# Formulário para excluir funcionário
def excluir_funcionario_form():
    dados = carregar_dados()
    nomes = [func["nome"] for func in dados]

    if not nomes:
        st.warning("Nenhum funcionário cadastrado.")
        return

    nome = st.selectbox("Selecione o funcionário para excluir", nomes)
    
    if st.button("Excluir", key=f"excluir_{nome}"):
        dados = [func for func in dados if func["nome"] != nome]
        salvar_dados(dados)
        st.success("Funcionário excluído!")
        sleep(2)
        st.session_state.funcionarios_view = None

# Interface principal
def funcionarios():
    st.title("Controle de Funcionários")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Cadastrar", key="btn_cadastrar"):
            st.session_state.funcionarios_view = "cadastrar"
    
    with col2:
        if st.button("Modificar", key="btn_modificar"):
            st.session_state.funcionarios_view = "modificar"

    with col3:
        if st.button("Excluir", key="btn_excluir"):
            st.session_state.funcionarios_view = "excluir"

    # Exibir o formulário correspondente
    if st.session_state.funcionarios_view == "cadastrar":
        cadastrar_funcionario_form()
    elif st.session_state.funcionarios_view == "modificar":
        modificar_funcionario_form()
    elif st.session_state.funcionarios_view == "excluir":
        excluir_funcionario_form()
    
    st.dataframe(carregar_dados(), use_container_width=True)

    if st.button("Voltar", key="btn_voltar"):
        st.session_state.page = "home"
        st.session_state.funcionarios_view = None
