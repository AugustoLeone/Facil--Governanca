import streamlit as st
import pandas as pd
import plotly.express as px

# Função para exibir os gráficos de índices operacionais
def exibir_indices_operacionais():
    st.header("Índices Operacionais")

    # Organizando os gráficos em colunas (2 por linha)
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de Permanência de Alunos por Mês
        dados_permanencia = [
            {"mes": "2023-01", "total_alunos": 120},
            {"mes": "2023-02", "total_alunos": 130},
            {"mes": "2023-03", "total_alunos": 125},
            {"mes": "2023-04", "total_alunos": 140},
            {"mes": "2023-05", "total_alunos": 135},
            {"mes": "2023-06", "total_alunos": 145}
        ]
        df = pd.DataFrame(dados_permanencia)
        fig = px.line(df, x="mes", y="total_alunos", markers=True, title="Permanência de Alunos por Mês")
        st.plotly_chart(fig)

    with col2:
        # Gráfico de Conclusão de Curso
        alunos_concluintes = [
            {"curso": "Matemática", "status": "concluido", "total_concluintes": 50},
            {"curso": "Física", "status": "concluido", "total_concluintes": 30},
        ]
        df_concluicao = pd.DataFrame(alunos_concluintes)
        fig_concluicao = px.bar(df_concluicao, x="curso", y="total_concluintes", text="total_concluintes", title="Conclusão de Curso")
        st.plotly_chart(fig_concluicao)

    col3, col4 = st.columns(2)

    with col3:
        # Gráfico de Média de Horas por Curso
        cursos_horas = [
            {"curso": "Matemática", "duracao_horas": 40},
            {"curso": "Física", "duracao_horas": 35},
            {"curso": "Química", "duracao_horas": 45},
        ]
        df_horas = pd.DataFrame(cursos_horas)
        fig_horas = px.bar(df_horas, x="curso", y="duracao_horas", text="duracao_horas", title="Média de Horas por Curso")
        st.plotly_chart(fig_horas)

    with col4:
        st.write("Conteúdo do gráfico da coluna 4.")

# Função para exibir relatórios financeiros (opcional para complementar)
def exibir_relatorios_financeiros():
    st.header("Relatórios Financeiros")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Gráfico ou conteúdo do primeiro relatório financeiro.")
    with col2:
        st.write("Gráfico ou conteúdo do segundo relatório financeiro.")
    
    col3, col4 = st.columns(2)
    with col3:
        st.write("Gráfico ou conteúdo do terceiro relatório financeiro.")
    with col4:
        st.write('')
