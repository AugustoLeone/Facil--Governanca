import streamlit as st
from scripts.auth import ensure_login
ensure_login()

from scripts.config import JSON_PATH
from scripts.discentes import cadastrar_aluno, emitir_certificado, consultar_aluno
from scripts.docentes import cadastrar_professor, cadastrar_curso, cadastrar_turma, visualizar_turmas
from scripts.agendamentos import agendamentos_app
from scripts.estoque import estoque
from scripts.funcionarios import funcionarios
from scripts.indices import indices_page

st.markdown(
    """
    <style>
    div.stButton > button {
        height: 100px;
        width: 250px;
        font-size: 24px;
        white-space: pre-line;
    }
    div.stButton {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def home_page():
    st.title("Bem-vindo ao Sistema Estação Tech")
    st.write("Selecione a funcionalidade desejada:")
    col1, col2, col3 = st.columns(3)
    if col1.button("🎓\nDiscentes"):
        st.session_state.page = "discentes"
    if col2.button("👩‍🏫\nDocentes"):
        st.session_state.page = "docentes"
    if col3.button("📅\nAgendamentos"):
        st.session_state.page = "agendamentos"
    
    col4, col5, col6 = st.columns(3)
    if col4.button("📦\nEstoque"):
        st.session_state.page = "estoque"
    if col5.button("👥\nFuncionarios"):
        st.session_state.page = "funcionarios"
    if col6.button("📊\nIndices"):
        st.session_state.page = "indices"

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

def render_discentes():
    st.header("Módulo Discentes")
    tab1, tab2, tab3 = st.tabs(["Cadastrar Alunos", "Emitir Certificado", "Consultar Aluno"])
    with tab1:
        cadastrar_aluno(JSON_PATH)
    with tab2:
        emitir_certificado(JSON_PATH)
    with tab3:
        consultar_aluno(JSON_PATH)
    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

def render_docentes():
    st.header("Módulo Docentes")
    tab1, tab2, tab3, tab4 = st.tabs(["Cadastrar Professor", "Cadastrar Curso", "Atribuir Aluno à Turma", "Visualizar Turmas"])
    with tab1:
        cadastrar_professor(JSON_PATH)
    with tab2:
        cadastrar_curso(JSON_PATH)
    with tab3:
        cadastrar_turma(JSON_PATH)
    with tab4:
        visualizar_turmas(JSON_PATH)
    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

def render_agendamentos():
    st.header("Módulo Agendamentos")
    agendamentos_app()
    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "discentes":
    render_discentes()
elif st.session_state.page == "docentes":
    render_docentes()
elif st.session_state.page == "agendamentos":
    render_agendamentos()
elif st.session_state.page == 'estoque':
    estoque()
elif st.session_state.page == 'funcionarios':
    funcionarios()
elif st.session_state.page == 'indices':
    indices_page()

