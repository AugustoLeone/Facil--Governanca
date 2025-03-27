import streamlit as st
from .estoque_script import cadastrar_item, adicionar_item, retirar_item, excluir_item, carregar_dados

# Inicializa a chave de estado para evitar erro na primeira execução
if "mostrar_formulario" not in st.session_state:
    st.session_state.mostrar_formulario = None

def estoque():
    st.title('Controle de Estoque')
    st.write('Escolha a opção que deseja realizar')

    # Separação dos botões por coluna
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button('Cadastrar Item', type='secondary', use_container_width=True):
            st.session_state.mostrar_formulario = 'cadastrar'

    with col2:
        if st.button('Adicionar Item', type='secondary', use_container_width=True):
            st.session_state.mostrar_formulario = 'adicionar'

    with col3:
        if st.button('Retirar Item', type='secondary', use_container_width=True):
            st.session_state.mostrar_formulario = 'retirar'

    with col4:
        if st.button('Excluir Item', type='secondary', use_container_width=True):
            st.session_state.mostrar_formulario = 'excluir'

    # Exibe o formulário correspondente
    if st.session_state.mostrar_formulario == 'cadastrar':
        cadastrar_formulario()
    elif st.session_state.mostrar_formulario == 'adicionar':
        adicionar_formulario()
    elif st.session_state.mostrar_formulario == 'retirar':
        retirar_formulario()
    elif st.session_state.mostrar_formulario == 'excluir':
        excluir_formulario()

    # Exibição do DataFrame do estoque
    st.dataframe(carregar_dados(), use_container_width=True)

    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

def cadastrar_formulario():
    st.subheader("Cadastrar Novo Item")
    with st.form("cadastrar_item"):
        item = st.text_input("Nome do Item")
        categoria = st.text_input("Categoria")
        tipo = st.text_input("Tipo")
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        preco_compra = st.number_input("Preço de Compra", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Cadastrar Item")

        if submitted:
            if item and categoria and tipo and quantidade and preco_compra:
                novo_item = cadastrar_item(item, categoria, tipo, quantidade, preco_compra)
                st.success(f"Item {novo_item['item']} cadastrado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

def adicionar_formulario():
    st.subheader("Adicionar Quantidade ao Estoque")
    with st.form("adicionar_item"):
        item = st.text_input("Nome do Item")
        categoria = st.text_input("Categoria")
        tipo = st.text_input("Tipo")
        quantidade = st.number_input("Quantidade a Adicionar", min_value=1, step=1)
        submitted = st.form_submit_button("Adicionar Item")

        if submitted:
            if item and categoria and tipo and quantidade:
                item_adicionado = adicionar_item(item, categoria, tipo, quantidade)
                if isinstance(item_adicionado, dict):
                    st.success(f"{quantidade} unidades de {item_adicionado['item']} adicionadas ao estoque!")
                else:
                    st.error(item_adicionado)
            else:
                st.error("Por favor, preencha todos os campos.")

def retirar_formulario():
    st.subheader("Retirar Quantidade do Estoque")
    with st.form("retirar_item"):
        item = st.text_input("Nome do Item")
        categoria = st.text_input("Categoria")
        tipo = st.text_input("Tipo")
        quantidade = st.number_input("Quantidade a Retirar", min_value=1, step=1)
        submitted = st.form_submit_button("Retirar Item")

        if submitted:
            if item and categoria and tipo and quantidade:
                item_retirado = retirar_item(item, categoria, tipo, quantidade)
                if isinstance(item_retirado, dict):
                    st.success(f"{quantidade} unidades de {item_retirado['item']} retiradas do estoque!")
                else:
                    st.error(item_retirado)
            else:
                st.error("Por favor, preencha todos os campos.")

def excluir_formulario():
    st.subheader("Excluir Item do Estoque")
    with st.form("excluir_item"):
        item = st.text_input("Nome do Item")
        categoria = st.text_input("Categoria")
        tipo = st.text_input("Tipo")
        submitted = st.form_submit_button("Excluir Item")

        if submitted:
            if item and categoria and tipo:
                resultado = excluir_item(item, categoria, tipo)
                st.success(resultado)
            else:
                st.error("Por favor, preencha todos os campos.")
