import streamlit as st
from .scripts_financeiro import tabela_dividas
from .formularios import inserir_db_dividas_formulario, excluir_db_dividas_formulario
from .banco_de_dados import criar_db_dividas

if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = None

criar_db_dividas()

#interface aba de gerenciamento de dividas
def gerenciamento_dividas():

    if "mostrar_formulario" not in st.session_state:
        st.session_state.mostrar_formulario = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Inserir', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'inserir_divida'

    with col2:
        if st.button('Excluir', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'excluir_divida'

    if st.session_state.mostrar_formulario == 'inserir_divida':
        inserir_db_dividas_formulario()
    elif st.session_state.mostrar_formulario == 'excluir_divida':
        excluir_db_dividas_formulario()
    
    tabela_dividas()

    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

if __name__ == '__main__':
    gerenciamento_dividas()
    