import streamlit as st
from scripts.banco_de_dados import cadastrar_funcionario_db, modificar_funcionario_db, excluir_funcionario_db
from time import sleep
import bcrypt

# Lista de cargos possíveis de funcionarios
cargos = ('Desenvolvedor', 'Diretor', 'Financeiro', 'RH', 'Coordenador', 'Administrativo', 'Pelador', 'Professor', 'Monitor')

# Variáveis para armazenar os dados confirmados
email_confirmado = None
cpf_confirmado = None

#função para criptografar a senha
def criptografar_senha(senha):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


# Verifica se um e-mail está válido
def verifica_email(email):

    #verifica se tem somente 1 '@'
    if email.count("@") != 1:
        return None 
    
    #separa o lacal do dominio dividindo o email pelo '@'
    local, dominio = email.split("@")

    #define caracteres invalidos
    invalid_chars = "(),:;<>[] "

    #verifica se tem algo antes e depois do '@'
    if not local or not dominio:
        return None

    #verifica se tem . no dominio
    if "." not in dominio:
        return None

    #vereifica se possui caracteres invalidos
    for i in invalid_chars:
        if i in email:
            return None

    return email  

# Validação se o CPF é valido
def verifica_cpf(cpf):

    # Remove caracteres especiais
    cpf = cpf.replace(".", "").replace("-", "")  

    # Retorna None se a quantidade de digitos numéricos for diferente de 11
    if not cpf.isdigit() or len(cpf) != 11:
        return None  

    # Evita CPFs com todos os dígitos iguais
    if cpf == cpf[0] * 11:
        return None  

    #calculo dos digitos verificadores
    def calcula_digito(cpf, peso):
        soma = sum(int(cpf[i]) * (peso - i) for i in range(peso - 1))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    primeiro_digito = calcula_digito(cpf, 10)
    segundo_digito = calcula_digito(cpf, 11)

    # Retorna o CPF se for válido
    if cpf[-2:] == primeiro_digito + segundo_digito:
        return cpf  
    
    return None

#formulario de cadastro do funcionario
def cadastrar_funcionario_form():
    with st.form("Formulario de cadastro de funcionario", clear_on_submit=True):
        nome = st.text_input('Insira o nome do funcionario que deseja cadastrar:', placeholder='Nome')
        usuario = st.text_input('Insira o nome de usuario do novo funcionario', placeholder='Usuario')
        senha = st.text_input('Insira a senha para o funcionario que deseja cadastrar', placeholder='Senha')
        email = st.text_input('Insira o email do novo funcionario', placeholder='email')
        cpf = st.text_input('Insira os digitos do CPF do novo funcionario', placeholder='CPF')
        col1, col2 = st.columns(2)
        with col1:
            cargo = st.selectbox('Selecione o cargo do novo funcionario', cargos)
        with col2:
            salario =  st.number_input('Insira o salario do novo funcionario', value=0.0, min_value=0.0, format="%.2f")

        submitted = st.form_submit_button('Cadastrar funcionario')
        if submitted:

            # Validação dos dados e declaração das variáveis SOMENTE se forem válidos
            if verifica_email(email=email):
                email_confirmado = verifica_email(email=email)
            else:
                st.error("❌ E-mail inválido!")
        
            if verifica_cpf(cpf=cpf):
                cpf_confirmado = verifica_cpf(cpf=cpf)
            else:
                st.error("❌ CPF inválido! Verifique os números inseridos.")
    
            #criptografando a senha
            senha_criptografada = criptografar_senha(senha=senha)

            #execução da função de cadastrono db
            try:
                cadastrar_funcionario_db(nome=nome, usuario=usuario, senha_criptografada=senha_criptografada, email_confirmado=email_confirmado, cpf_confirmado=cpf_confirmado, cargo=cargo, salario=salario)
                sleep(2)
            except:
                st.error("❌campo preenchido incorretamente!")

#formulario que modifica todos os campos do funcionario
def modificar_funcionario_form():
    with st.form("Formulario de modificação de funcionario", clear_on_submit=True):
        nome = st.text_input('Insira o nome do funcionario que deseja cadastrar:', placeholder='Nome')
        usuario = st.text_input('Insira o nome de usuario do novo funcionario', placeholder='Usuario')
        senha = st.text_input('Insira a senha para o funcionario que deseja cadastrar', placeholder='Senha')
        email = st.text_input('Insira o email do novo funcionario', placeholder='email')
        cpf = st.text_input('Insira os digitos do CPF do novo funcionario', placeholder='CPF')
        col1, col2 = st.columns(2)
        with col1:
            cargo = st.selectbox('Selecione o cargo do novo funcionario', cargos)
        with col2:
            salario =  st.number_input('Insira o salario do novo funcionario', value=0.0, min_value=0.0, format="%.2f")
        
        submitted = st.form_submit_button('Modificar dados do funcionario funcionario')
        if submitted:

            # Validação dos dados e declaração das variáveis SOMENTE se forem válidos
            if verifica_email(email=email):
                email_confirmado = verifica_email(email=email)
            else:
                st.error("❌ E-mail inválido!")
        
            if verifica_cpf(cpf=cpf):
                cpf_confirmado = verifica_cpf(cpf=cpf)
            else:
                st.error("❌ CPF inválido! Verifique os números inseridos.")

            if senha:
                senha_criptografada = criptografar_senha(senha=senha)
            else:
                senha_criptografada = None

            modificar_funcionario_db(nome=nome,usuario=usuario,senha_criptografada=senha_criptografada,email_confirmado=email_confirmado,cpf_confirmado=cpf_confirmado,cargo=cargo,salario=salario)
            sleep(2)

#formulario para exclusão do funcionario
def excluir_funcionario_form():
    with st.form("Formulario de exclusão de funcionario", clear_on_submit=True):
        nome = st.text_input('Insira o nome do funcionario que deseja cadastrar:', placeholder='Nome')
        email = st.text_input('Insira o email do novo funcionario', placeholder='email')
        cpf = st.text_input('Insira os digitos do CPF do novo funcionario', placeholder='CPF')
        cargo = st.selectbox('Selecione o cargo do novo funcionario', cargos)

        submitted = st.form_submit_button('excluir funcionario')
        if submitted:
            excluir_funcionario_db(nome=nome, email=email, cpf=cpf, cargo=cargo)
            sleep(2)

# Função para verificar a senha
def verificar_senha(senha, senha_armazenada):
    return bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8'))