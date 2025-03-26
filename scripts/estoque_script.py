import streamlit as st
import pandas as pd
import psycopg2
from scripts.banco_de_dados import cadastrar_item, adicionar_item, retirar_item, excluir_item
from time import sleep

#tras as categorias e tipos de itens do estoque para inserção nos formulários
categorias =('Materia escritorio', 'manutencao', 'limpeza', 'material para salas') 
tipos = ('unidade', 'pacote 6', 'pacote 8', 'pacote 10', 'pacote 12', 'pacote 16')

#leitura e conexao do database para montagem da tabela de estoque
def carregar_dados():
    conn = psycopg2.connect("dbname=fac1l-governanca user=postgres password=Yasmin23@ host=localhost port=5432")
    df = pd.read_sql("SELECT * FROM estoque", conn)
    conn.close()  # Fechar a conexão após uso
    return df

#formulario para cadastro de item que executa a função de cadastro
def cadastrar_item_form ():
    with st.form('formulario_cadastrar_item', clear_on_submit=True):

        item = st.text_input('item que deseja cadastrar', 'item')

        col6, col7 = st.columns(2)
        with col6:
            categoria = st.selectbox('Selecione a categoria do item que deseja cadastrar:', categorias)
        with col7:
            tipo = st.selectbox('Selecione a categoria do item que deseja cadastrar:', tipos)
        quantidade = st.number_input('Insira a quantidade em que deseja cadastrar', value=0, step=1)
        preco = st.number_input('Insira o valor de compra do item', value=0, step=1)

        submitted = st.form_submit_button('Cadastrar')
        if submitted:
            cadastrar_item(item=item, categoria=categoria, tipo=tipo, quantidade=quantidade,preco_compra=preco)
            sleep(2)
            st.session_state.mostrar_formulario = None

#formulario para retirada de item que executa a função de retirada
def adicionar_item_form():
    with st.form("formulario_adicao_item", clear_on_submit=True):

        item = st.text_input('item que deseja adicionar', 'item')

        col6, col7 = st.columns(2)
        with col6:
            categoria = st.selectbox('Selecione a categoria do item que deseja adicionar:', categorias)
        with col7:
            tipo = st.selectbox('Selecione a categoria do item que deseja adicionar:', tipos)
        quantidade = st.number_input('Insira a quantidade em que deseja adicionar', value=0, step=1)

        submitted = st.form_submit_button("Adicionar")
        if submitted:
            adicionar_item(item=item, categoria=categoria, tipo=tipo, quantidade=quantidade)
            sleep(2)
            st.session_state.mostrar_formulario = None

#formulario para retirada de item que executa a função de retirada
def retirar_item_form():
    with st.form("formulario_retirada_item", clear_on_submit=True):

        item = st.text_input('item que deseja retirar', 'item')

        col6, col7 = st.columns(2)
        with col6:
            categoria = st.selectbox('Selecione a categoria do item que deseja retirar:', categorias)
        with col7:
            tipo = st.selectbox('Selecione a categoria do item que deseja retirar:', tipos)
        
        quantidade = st.number_input('Insira a quantidade em que deseja retirar', value=0, step=1)

        submitted = st.form_submit_button("Retirar")
        if submitted:
            retirar_item(item=item, categoria=categoria, tipo=tipo, quantidade=quantidade)
            sleep(2)
            st.session_state.mostrar_formulario = None

#formulario para exclusão de item que executa a função de exclusão
def excluir_item_form():
    with st.form("formulario_exclusao_item", clear_on_submit=True):

        item = st.text_input('item que deseja excluir', 'item')

        col6, col7 = st.columns(2)
        if col6:
            categoria = st.selectbox('Selecione a categoria do item que deseja excluir:', categorias)
        if col7:
            tipo = st.selectbox('Selecione a categoria do item que deseja excluir:', tipos)

        submitted = st.form_submit_button("Excluir")
        if submitted:
            excluir_item(item=item, categoria=categoria, tipo=tipo)
            sleep(2)
            st.session_state.mostrar_formulario = None
