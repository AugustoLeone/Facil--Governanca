import streamlit as st
from .scripts_financeiro import tabela_orcamentos
from .formularios import inserir_db_orcamento_formulario, excluir_db_orcamento_formulario
from .banco_de_dados import criar_db_orcamento

if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = None

criar_db_orcamento()

#interface gerenciamento orçamentário
def gerenciamento_orcamentario():

    if "mostrar_formulario" not in st.session_state:
        st.session_state.mostrar_formulario = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Inserir', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'inserir_orcamento'

    with col2:
        if st.button('Excluir', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'excluir_orcamento'

    if st.session_state.mostrar_formulario == 'inserir_orcamento':
        inserir_db_orcamento_formulario()
    elif st.session_state.mostrar_formulario == 'excluir_orcamento':
        excluir_db_orcamento_formulario()
    
    tabela_orcamentos()

    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

if __name__ == '__main__':
    gerenciamento_orcamentario()
    