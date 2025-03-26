import streamlit as st
import pandas as pd
import plotly.express as px
from .banco_de_dados import conexao_db

def permanencia_alunos():
    conn = conexao_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            TO_CHAR(a.data_matricula, 'YYYY-MM') AS mes,  
            COUNT(a.id_aluno) AS total_alunos      
        FROM alunos a
        WHERE EXTRACT(MONTH FROM a.data_matricula) IN (1, 2, 3, 4, 5, 6)  
        GROUP BY mes  
        ORDER BY mes  
    """)
    
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not resultados:
        st.warning("Nenhum dado encontrado para os alunos matriculados.")
        return
    
    df = pd.DataFrame(resultados, columns=["Mês", "Total de Alunos Matriculados"])
    fig = px.line(df, x="Mês", y="Total de Alunos Matriculados", markers=True, title="Permanência de Alunos por Mês")
    st.plotly_chart(fig)

def permanencia_alunos_curso():
    with conexao_db() as conn:
        with conn.cursor() as cursor:
            # Obtendo cursos disponíveis
            cursor.execute("SELECT DISTINCT nome FROM cursos ORDER BY nome")
            cursos_disponiveis = [row[0] for row in cursor.fetchall()]
            
            if not cursos_disponiveis:
                st.error("Nenhum curso disponível para exibição.")
                return

            # Seleção de curso pelo usuário
            curso_selecionado = st.selectbox("Selecione um curso", cursos_disponiveis, key="curso_selecionado_curso")
            
            # Consultando dados de alunos matriculados no curso selecionado
            cursor.execute("""
                SELECT 
                    TO_CHAR(a.data_matricula, 'YYYY-MM') AS mes,  
                    COUNT(a.id_aluno) AS total_alunos      
                FROM matriculas m
                JOIN alunos a ON m.aluno_id = a.id_aluno
                JOIN cursos c ON m.curso_id = c.id_curso
                WHERE EXTRACT(MONTH FROM a.data_matricula) IN (1, 2, 3, 4, 5, 6)  
                AND c.nome = %s
                GROUP BY mes  
                ORDER BY mes  
            """, (curso_selecionado,))
            
            resultados = cursor.fetchall()
            
            if not resultados:
                st.warning(f"Nenhum dado encontrado para o curso {curso_selecionado}.")
                return

    df = pd.DataFrame(resultados, columns=["Mês", "Total de Alunos Matriculados"])
    fig = px.line(df, x="Mês", y="Total de Alunos Matriculados", markers=True, title=f"Permanência de Alunos - {curso_selecionado}")
    st.plotly_chart(fig)

def conclusao_curso():
    conn = conexao_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT nome FROM cursos ORDER BY nome")
    cursos = [row[0] for row in cursor.fetchall()]
    
    curso_selecionado = st.selectbox("Selecione um curso", cursos, key="curso_selecionado_conclusao")
    
    cursor.execute("""
        SELECT COUNT(*) AS total_concluintes
        FROM alunos
        JOIN cursos ON alunos.curso_id = cursos.id_curso
        WHERE alunos.status = 'concluido' AND cursos.nome = %s
    """, (curso_selecionado,))
    
    total_concluintes = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    df = pd.DataFrame({"Curso": [curso_selecionado], "Total de Concluintes": [total_concluintes]})
    fig = px.bar(df, x="Curso", y="Total de Concluintes", text="Total de Concluintes", title=f"Total de Concluintes - {curso_selecionado}")
    st.plotly_chart(fig)

def conclusao_curso_total():
    conn = conexao_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT c.nome, COUNT(*) AS total_concluintes
        FROM alunos a
        JOIN cursos c ON a.curso_id = c.id_curso
        WHERE a.status = 'concluido'
        GROUP BY c.nome
        ORDER BY total_concluintes DESC
    """)
    
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    
    df = pd.DataFrame(resultados, columns=["Curso", "Total de Concluintes"])
    fig = px.bar(df, x="Curso", y="Total de Concluintes", text="Total de Concluintes", title="Índice de Concluintes por Curso")
    st.plotly_chart(fig)

def media_horas_curso():
    # Conectando ao banco de dados
    conn = conexao_db()
    cursor = conn.cursor()

    # Buscando os dados necessários (horários de início e conclusão dos cursos)
    cursor.execute("""
        SELECT c.nome, m.data_inicio, m.data_conclusao
        FROM matriculas m
        JOIN cursos c ON m.curso_id = c.id_curso
        WHERE m.status = 'concluido'
        AND m.data_conclusao IS NOT NULL
        AND m.data_inicio IS NOT NULL
    """)
    
    # Obtendo os resultados da consulta
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convertendo os dados para um DataFrame
    df = pd.DataFrame(resultados, columns=["Curso", "Data Início", "Data Conclusão"])
    
    # Convertendo as colunas para o tipo datetime
    df["Data Início"] = pd.to_datetime(df["Data Início"])
    df["Data Conclusão"] = pd.to_datetime(df["Data Conclusão"])

    # Calculando a diferença entre as datas em horas
    df["Duração (Horas)"] = (df["Data Conclusão"] - df["Data Início"]).dt.total_seconds() / 3600
    
    # Calculando a média de horas por curso
    media_horas = df.groupby("Curso")["Duração (Horas)"].mean().reset_index()

    # Gerando o gráfico
    fig = px.bar(media_horas, x="Curso", y="Duração (Horas)", text="Duração (Horas)", title="Média Total de Horas por Curso")
    st.plotly_chart(fig)
