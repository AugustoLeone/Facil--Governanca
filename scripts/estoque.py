import streamlit as st
from scripts.estoque_script import cadastrar_item_form, adicionar_item_form, retirar_item_form, excluir_item_form,carregar_dados
from .banco_de_dados import criar_tabela_estoque

# Inicializa a chave de estado para evitar erro na primeira execução
if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = None

criar_tabela_estoque()

#execução da aplicação completa
def estoque ():
    st.title('Controle de estoque')
    st.write('Escolha a opção que deseja realizar')

#separação dos botoes por coluna
    col1, col2, col3, col4 = st.columns(4)

#botao que executa a função de cadastro do formulario para o cadastro de item
    with col1:
        if st.button('cadastrar item', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'cadastrar'

#botao que executa a função de adição do formulario para o adição de item
    with col2:
        if st.button('Adicionar item', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'adicionar'

#botao que executa a função de retirada do formulario para o retirada de item
    with col3:
        if st.button('retirar item', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'retirar'

#botao que executa a função de exclusao do formulario para o exclusao de item            
    with col4:
        if st.button('excluir item', type='secondary',use_container_width=True):
            st.session_state.mostrar_formulario = 'excluir'

# Exibe o formulário correspondente
    if st.session_state.mostrar_formulario == 'cadastrar':
        cadastrar_item_form()
    elif st.session_state.mostrar_formulario == 'adicionar':
        adicionar_item_form()
    elif st.session_state.mostrar_formulario == 'retirar':
        retirar_item_form()
    elif st.session_state.mostrar_formulario == 'excluir':
        excluir_item_form()

#exibição do dataframe do estoque
    st.dataframe(carregar_dados(), use_container_width=True)

    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

if __name__ == "__main__":
    estoque()