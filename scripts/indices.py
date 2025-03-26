import streamlit as st
from .indices_operacionais import permanencia_alunos, permanencia_alunos_curso, conclusao_curso, conclusao_curso_total, media_horas_curso
from .relatorios import margem_bruta, lucro_operacional, lucro_liquido, alavancagem_endividamento, liquidez_corrente, composicao_endividamento
from .banco_de_dados import criar_tabela_alunos, criar_tabela_professores, criar_tabela_cursos, criar_tabela_matriculas

criar_tabela_professores()
criar_tabela_cursos()
criar_tabela_alunos()
criar_tabela_matriculas()

# Inicializa a chave de estado para evitar erro na primeira execução
if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = None

# Função para exibir gráficos de índices operacionais
def exibir_indices_operacionais():
    st.header("Índices Operacionais")

    # Organizando os gráficos em colunas (2 por linha)
    col1, col2 = st.columns(2)

    with col1:
        permanencia_alunos()
    with col2:
        conclusao_curso_total()

    col3, col4 = st.columns(2)

    with col3:
        conclusao_curso()
    with col4:
        permanencia_alunos_curso()

    col5, col6 = st.columns(2)

    with col5:
        media_horas_curso()
    with col6:
        st.write("")

# Função para exibir gráficos de relatórios financeiros
def exibir_relatorios():
    st.header("Relatórios Financeiros")
    
    col1, col2 = st.columns(2)
    with col1:
        margem_bruta()
    with col2:
        lucro_operacional()

    col3, col4 = st.columns(2)
    with col3:
        lucro_liquido()
    with col4:
        alavancagem_endividamento()

    col5, col6 = st.columns(2)
    with col5:
        liquidez_corrente()
    with col6:
        composicao_endividamento()

# Exibindo os gráficos no Streamlit com abas
def indices_page():
    st.title("Análise Financeira e Operacional")

    # Criação das abas
    abas = st.tabs(["Índices Operacionais", "Relatórios Financeiros"])

    # Exibir conteúdo da aba de Índices Operacionais
    with abas[0]:
        exibir_indices_operacionais()

    # Exibir conteúdo da aba de Relatórios Financeiros
    with abas[1]:
        exibir_relatorios()

    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

if __name__ == "__main__":
    indices_page()
