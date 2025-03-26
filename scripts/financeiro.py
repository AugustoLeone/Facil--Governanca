import streamlit as st
from .receita_despesa import controle_receitas_despesas
from .gerenciamento_dividas import gerenciamento_dividas
from .gerenciamento_orcamentario import gerenciamento_orcamentario
from .relatorios import relatorios

#visual principal do app
def financeiro():
    st.sidebar.title('Menu Financeiro')
    opcao = st.sidebar.radio('Navegação',
    [
    'Controle de receitas e despesas',
    'Gerenciamento de dividas',
    'Gerenciamento Orçamentário',
    ])
    
    #redirecionamento pages
    if opcao == "Controle de receitas e despesas":
        controle_receitas_despesas()
    elif opcao == "Gerenciamento de dividas":
        gerenciamento_dividas()
    elif opcao == "Gerenciamento Orçamentário":
        gerenciamento_orcamentario()

    
if __name__ == "__main__":
    financeiro()
    