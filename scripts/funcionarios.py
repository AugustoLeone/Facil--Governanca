import streamlit as st
from .funcionarios_script import cadastrar_funcionario_form, modificar_funcionario_form, excluir_funcionario_form
from .banco_de_dados import listar_funcionario, create_tb_funcionarios

# Inicializa a chave de estado para evitar erro na primeira execução
if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = None

create_tb_funcionarios()

#função para visualização da interface para administração dos fucnionarios
def funcionarios():
    st.title('Controle de funcionario')

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button('cadastrar', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'cadastrar_funcionario'

    with col2:
        if st.button('Modificar', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'modificar_funcionario'

    with col3:
        if st.button('Excluir', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'excluir_funcionario'

    #chamado dos formularios linkados com os botoes
    if st.session_state.mostrar_formulario == 'cadastrar_funcionario':
        cadastrar_funcionario_form()
    elif st.session_state.mostrar_formulario == 'modificar_funcionario':
        modificar_funcionario_form()
    elif st.session_state.mostrar_formulario == 'excluir_funcionario':
        excluir_funcionario_form()

    #visualização da tabela do db
    st.dataframe(listar_funcionario(), use_container_width=True)

    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

if __name__ == '__main__':
    funcionarios()
