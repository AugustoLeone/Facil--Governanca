import streamlit as st
from .indices_operacionais import exibir_indices_operacionais, exibir_relatorios_financeiros

# Função principal para mostrar as abas
def indices_page():
    st.title("Análise Financeira e Operacional")

    # Criação das abas
    abas = st.tabs(["Índices Operacionais", "Relatórios Financeiros"])

    # Exibir conteúdo da aba de Índices Operacionais
    with abas[0]:
        exibir_indices_operacionais()

    # Exibir conteúdo da aba de Relatórios Financeiros
    with abas[1]:
        exibir_relatorios_financeiros()

    if st.button("Voltar para a tela inicial"):
        st.session_state.page = "home"

if __name__ == "__main__":
    indices_page()
