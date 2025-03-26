from .banco_de_dados import buscar_db_receitas_despesas, buscar_db_dividas, buscar_db_orcamento
import streamlit as st
import pandas as pd

# Cache para evitar consultas desnecessárias ao banco
@st.cache_data
def carregar_dados():
    return buscar_db_receitas_despesas()

# Formata valores para exibição correta
def formatar_valor(tipo, valor):
    valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if tipo.lower() == "despesa": 
        return f"- {valor_formatado}"
    return valor_formatado

df_receitas_despesas = buscar_db_receitas_despesas()

#função que executa a tabela
def tabela_receita_despesa():
    df_receitas_despesas = buscar_db_receitas_despesas()
    
    if not df_receitas_despesas.empty:
        df_receitas_despesas["data"] = pd.to_datetime(df_receitas_despesas["data"], errors="coerce")  # Converte para datetime
        df_receitas_despesas["Data"] = df_receitas_despesas["data"].dt.strftime("%d/%m/%y")
        df_receitas_despesas["Valor"] = df_receitas_despesas.apply(
            lambda row: formatar_valor(row["tipo"], row["valor"]),
            axis=1
        )
        df_receitas_despesas = df_receitas_despesas.drop(columns=["data"])  # Remove a coluna original de data
        
        st.table(df_receitas_despesas)
    else:
        st.info("Nenhuma receita/despesa registrada ainda.")

#--------------------------------------------------Scripts Dividas----------------------------------------------------------

#função para visualização da tabela de dividas
def tabela_dividas():
    df_dividas = buscar_db_dividas()
    if not df_dividas.empty:
        df_dividas = pd.DataFrame(df_dividas)
        tabela_dividas = st.dataframe(df_dividas)
        return tabela_dividas
    else:
        st.info("Nenhuma divida registrada ainda.")
    
#--------------------------------------------------Scripts orcamento----------------------------------------------------------

#função para visualização da tabela de orçamentos
def tabela_orcamentos():
    df_orcamentos = buscar_db_orcamento()
    if not df_orcamentos.empty:
        df_orcamentos = pd.DataFrame(df_orcamentos)
        tabela_orcamento = st.dataframe(df_orcamentos)
        return tabela_orcamento
    else:
        st.info("Nenhum orçamento registrada ainda.")
