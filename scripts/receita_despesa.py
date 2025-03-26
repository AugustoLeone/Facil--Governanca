import streamlit as st
from .scripts_financeiro import tabela_receita_despesa
from .formularios import inserir_db_receita_despesa_formulario, excluir_db_receitas_despesas_formulario
from .banco_de_dados import criar_db_receitas_despesas

if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = None

criar_db_receitas_despesas()

#interface de inserção de receitas e despesas
def controle_receitas_despesas():
    st.title('Controle de receitas e despesas')
    
    if "mostrar_formulario" not in st.session_state:
        st.session_state.mostrar_formulario = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Inserir', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'inserir_receita_despesa'

    with col2:
        if st.button('Excluir', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'excluir_receita_despesa'

    if st.session_state.mostrar_formulario == 'inserir_receita_despesa':
        inserir_db_receita_despesa_formulario()
    elif st.session_state.mostrar_formulario == 'excluir_receita_despesa':
        excluir_db_receitas_despesas_formulario()

    tabela_receita_despesa()

    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"
    
if __name__ == '__main__':
    controle_receitas_despesas()