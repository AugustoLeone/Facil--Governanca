import streamlit as st
from datetime import date
from .banco_de_dados import inserir_db_receita_despesa, excluir_db_receitas_despesas, inserir_db_dividas,excluir_db_dividas, excluir_db_orcamento, inserir_db_orcamento
from .scripts_financeiro import carregar_dados

#categorias de receitas e despesas
categorias = ('Transporte', 'Alimentação', 'Lazer', 'Saúde', 'Educação', 'Outros')

#função de inserção de receita e despesa
def inserir_db_receita_despesa_formulario():

    st.subheader('Inserir Receita ou Despesa')

    if "tipo" not in st.session_state:
        st.session_state.tipo = "receita"

    col1, col2 =st.columns(2)
    with col1:
        data = st.date_input("Data", value=date.today())
    with col2:
        categoria = st.selectbox("Categoria", categorias)
    
    descricao = st.text_input("Descrição")

    tipo = st.radio("Tipo", ["receita", "despesa"], horizontal=True, key="tipo")

    data_pagamento, n_parcelas, forma_pagamento = None, None, None
    if tipo == 'despesa':
        data_pagamento = data
        n_parcelas = st.number_input('Insira o número de parcelas', value=1, step=1, min_value=1)
        forma_pagamento = st.radio('Forma de Pagamento', ['a vista', 'parcelado'], horizontal=True)

    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", key="inserir_valor")

    if st.button('Inserir'):
        inserir_db_receita_despesa(data=data, categoria=categoria, descricao=descricao, tipo=tipo, valor=valor)
        
        if tipo == 'despesa':
            inserir_db_dividas(data_compra=data, data_pagamento=data_pagamento, forma_pagamento=forma_pagamento, n_parcelas=n_parcelas, categoria=categoria, descricao=descricao, valor=valor)
        
        st.success(f'{tipo.capitalize()} inserida com sucesso!')
        carregar_dados.clear()

#função de formulario de exclusão de receitas e despesas
def excluir_db_receitas_despesas_formulario():
    
    st.subheader('Excluir Receita ou Despesa')

    if "tipo" not in st.session_state:
        st.session_state.tipo = "receita"

    col1, col2 =st.columns(2)
    with col1:
        data = st.date_input("Data", value=date.today())
    with col2:
        categoria = st.selectbox("Categoria", categorias)
    
    tipo = st.radio("Tipo", ["receita", "despesa"], horizontal=True, key="tipo")

    n_parcelas, forma_pagamento = None, None
    if tipo == 'despesa':
        n_parcelas = st.number_input('Número de parcelas', min_value=1, value=1, step=1)
        forma_pagamento = st.radio('Forma de Pagamento', ['a vista', 'parcelado'], horizontal=True)

    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", key="excluir_valor")

    if st.button('Excluir'):

        sucesso = excluir_db_receitas_despesas(data=data, categoria=categoria, tipo=tipo, valor=valor)
        excluir_db_dividas(data_compra=data, forma_pagamento=forma_pagamento, n_parcelas=n_parcelas, categoria=categoria, valor=valor)
        
        if sucesso:
            st.rerun()  # Atualiza a página imediatamente após a exclusão

#--------------------------------------------------Scripts Dividas----------------------------------------------------------

#função de inserção de dividas
def inserir_db_dividas_formulario():

    st.subheader('Inserir Receita ou Despesa')

    if "tipo" not in st.session_state:
        st.session_state.tipo = "receita"

    col1, col2 =st.columns(2)
    with col1:
        data = st.date_input("Data", value=date.today())
    with col2:
        categoria = st.selectbox("Categoria", categorias)
    
    descricao = st.text_input("Descrição")

    tipo = 'despesa'

    data_pagamento, n_parcelas, forma_pagamento = None, None, None
    if tipo == 'despesa':
        data_pagamento = data
        n_parcelas = st.number_input('Insira o número de parcelas', value=1, step=1, min_value=1)
        forma_pagamento = st.radio('Forma de Pagamento', ['a vista', 'parcelado'], horizontal=True)

    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", key="inserir_divida")

    if st.button('Inserir'):
        inserir_db_receita_despesa(data=data, categoria=categoria, descricao=descricao, tipo=tipo, valor=valor)
        
        if tipo == 'despesa':
            inserir_db_dividas(data_compra=data, data_pagamento=data_pagamento, forma_pagamento=forma_pagamento, n_parcelas=n_parcelas, categoria=categoria, descricao=descricao, valor=valor)
        
        st.success(f'{tipo.capitalize()} inserida com sucesso!')
        carregar_dados.clear()

#função de exclusão de dividas
def excluir_db_dividas_formulario():
    
    st.subheader('Excluir Receita ou Despesa')

    if "tipo" not in st.session_state:
        st.session_state.tipo = "receita"

    col1, col2 =st.columns(2)
    with col1:
        data = st.date_input("Data", value=date.today())
    with col2:
        categoria = st.selectbox("Categoria", categorias)
    
    tipo = "despesa"

    n_parcelas, forma_pagamento = None, None
    if tipo == 'despesa':
        n_parcelas = st.number_input('Número de parcelas', min_value=1, value=1, step=1)
        forma_pagamento = st.radio('Forma de Pagamento', ['a vista', 'parcelado'], horizontal=True)

    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", key="excluir_divida")

    if st.button('Excluir'):

        sucesso = excluir_db_receitas_despesas(data=data, categoria=categoria, tipo=tipo, valor=valor)
        excluir_db_dividas(data_compra=data, forma_pagamento=forma_pagamento, n_parcelas=n_parcelas, categoria=categoria, valor=valor)
        
        if sucesso:
            st.rerun()

#--------------------------------------------------Scripts orcamento----------------------------------------------------------

#função de inserção de orcamentos
def inserir_db_orcamento_formulario():

    st.subheader('Inserir Receita ou Despesa')

    col1, col2 =st.columns(2)
    with col1:
        data_inicio = st.date_input("Data de inicio", value=date.today())
    with col2:
        data_termino_previsto = st.date_input("Data prevista para o termino", value=date.today())
    
    atraso_dias = st.number_input('Numero de dias de atraso', min_value=0)

    descricao = st.text_input("Descrição")

    data_pagamento, n_parcelas, forma_pagamento = None, None, None

    valor_orcado = st.number_input("Valor Orçado (R$)", min_value=0.0, format="%.2f", key="inserir_valor_orcado")
    valor_gasto = st.number_input("Valor Gasto (R$)", min_value=0.0, format="%.2f", key="inserir_valor_gasto")

    if st.button('Inserir'):
        
        inserir_db_orcamento(
            data_inicio=data_inicio,
            data_termino_previsto=data_termino_previsto,
            atraso_dias=atraso_dias,
            descricao=descricao,
            valor_orcado=valor_orcado,
            valor_gasto=valor_gasto
        )

        st.success('Orçamento inserido com sucesso!')
        carregar_dados.clear()

#função de exclusão de orcamento
def excluir_db_orcamento_formulario():
    
    st.subheader('Excluir Receita ou Despesa')

    if "tipo" not in st.session_state:
        st.session_state.tipo = "receita"

    col1, col2 =st.columns(2)
    with col1:
        data_inicio = st.date_input("Data de inicio", value=date.today())
    with col2:
        data_termino_previsto = st.date_input("Data prevista para o termino", value=date.today())

    descricao = st.text_input("Descrição")

    valor_orcado = st.number_input("Valor Orçado (R$)", min_value=0.0, format="%.2f", key="excluir_valor_orcado")

    if st.button('Excluir'):

        sucesso = excluir_db_orcamento(
            data_inicio= data_inicio,
            data_termino_previsto=data_termino_previsto,
            descricao=descricao,
            valor_orcado=valor_orcado
        )
        
        if sucesso:
            st.rerun()
