import streamlit as st
import pandas as pd
import plotly.express as px
from .banco_de_dados import conexao_db

def margem_bruta():
    # Estabelece conexão com o banco de dados
    conn = conexao_db()
    cursor = conn.cursor()
    
    # Consulta SQL para calcular a receita total agrupada por mês, considerando apenas janeiro a junho
    cursor.execute("""
        SELECT 
            TO_CHAR(data, 'YYYY-MM') AS mes,  
            SUM(valor) AS total_receita      
        FROM controle_receita_despesa
        WHERE tipo = 'receita'              
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  
        GROUP BY mes  
        ORDER BY mes  
    """)
    
    # Obtém os resultados da consulta
    resultados = cursor.fetchall()
    
    # Fecha a conexão com o banco de dados
    cursor.close()
    conn.close()
    
    # Converte os resultados em um DataFrame
    df = pd.DataFrame(resultados, columns=["Mês", "Receita Total"])
    
    # Cria um gráfico de linha
    fig = px.line(df, x="Mês", y="Receita Total", markers=True, title="Receita Total por Mês")
    
    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

def lucro_operacional():
    # Estabelece conexão com o banco de dados
    conn = conexao_db()
    cursor = conn.cursor()

    # Consulta SQL para calcular a receita total agrupada por mês (janeiro a junho)
    cursor.execute("""
        SELECT 
            TO_CHAR(data, 'YYYY-MM') AS mes,  
            SUM(valor) AS total_receita       
        FROM controle_receita_despesa
        WHERE tipo = 'receita'               
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  
        GROUP BY mes
        ORDER BY mes
    """)
    
    receitas = dict(cursor.fetchall())  # Converte para dicionário {mes: total_receita}

    # Consulta SQL para calcular as despesas operacionais (salário e manutenção) por mês (janeiro a junho)
    cursor.execute("""
        SELECT 
            TO_CHAR(data, 'YYYY-MM') AS mes,  
            SUM(valor) AS total_despesa       
        FROM controle_receita_despesa
        WHERE tipo = 'despesa'               
        AND categoria IN ('salario', 'manutenção')  
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  
        GROUP BY mes
        ORDER BY mes
    """)
    
    despesas = dict(cursor.fetchall())  # Converte para dicionário {mes: total_despesa}

    # Fecha a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Criando um DataFrame consolidado com lucro operacional (receita - despesa)
    meses = sorted(set(receitas.keys()) | set(despesas.keys()))  # Garante que todos os meses estejam na lista
    df = pd.DataFrame({
        "Mês": meses,
        "Receita Total": [receitas.get(mes, 0) for mes in meses],  # Usa 0 se o mês não estiver presente
        "Despesa Operacional": [despesas.get(mes, 0) for mes in meses]  # Usa 0 se o mês não estiver presente
    })

    # Calcula o lucro operacional (Receita - Despesa)
    df["Lucro Operacional"] = df["Receita Total"] - df["Despesa Operacional"]

    # Cria um gráfico de barras
    fig = px.bar(
        df, x="Mês", y="Lucro Operacional", 
        title="Lucro Operacional por Mês",
        text_auto=True  # Exibe os valores nas barras
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px
from .banco_de_dados import conexao_db

def lucro_liquido():
    # Estabelece conexão com o banco de dados
    conn = conexao_db()
    cursor = conn.cursor()

    # Consulta SQL para calcular a receita total por mês (janeiro a junho)
    cursor.execute("""
        SELECT 
            TO_CHAR(data, 'YYYY-MM') AS mes,  
            SUM(valor) AS total_receita       
        FROM controle_receita_despesa
        WHERE tipo = 'receita'               
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  
        GROUP BY mes
        ORDER BY mes
    """)
    
    receitas = dict(cursor.fetchall())  # Converte para {mes: total_receita}

    # Consulta SQL para calcular as despesas totais por mês (janeiro a junho)
    cursor.execute("""
        SELECT 
            TO_CHAR(data, 'YYYY-MM') AS mes,  
            SUM(valor) AS total_despesa       
        FROM controle_receita_despesa
        WHERE tipo = 'despesa'               
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  
        GROUP BY mes
        ORDER BY mes
    """)

    despesas = dict(cursor.fetchall())  # Converte para {mes: total_despesa}

    # Fecha a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Lista de meses esperados
    meses = ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06']

    # Criando DataFrame com valores de receita, despesa e lucro líquido
    df = pd.DataFrame({
        "Mês": meses,
        "Receita Total": [receitas.get(mes, 0) for mes in meses],  
        "Despesa Total": [despesas.get(mes, 0) for mes in meses]  
    })

    # Calcula o Lucro Líquido
    df["Lucro Líquido"] = df["Receita Total"] - df["Despesa Total"]

    # Cria um gráfico de barras
    fig = px.bar(
        df, x="Mês", y="Lucro Líquido", 
        title="Lucro Líquido por Mês",
        text_auto=True,  # Exibe os valores nas barras
        labels={"Lucro Líquido": "Valor (R$)"}
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

def alavancagem_endividamento():
    # Estabelece conexão com o banco de dados
    conn = conexao_db()
    cursor = conn.cursor()

    # Consulta SQL para calcular o total de receitas de janeiro a junho
    cursor.execute("""
        SELECT 
            SUM(valor) AS total_receita       
        FROM controle_receita_despesa
        WHERE tipo = 'receita'               
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  
    """)
    
    receita_total = cursor.fetchone()[0] or 0  

    # Consulta SQL para calcular o total de despesas de janeiro a junho
    cursor.execute("""
        SELECT 
            SUM(valor) AS total_despesa       
        FROM controle_receita_despesa
        WHERE tipo = 'despesa'               
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  
    """)
    
    despesa_total = cursor.fetchone()[0] or 0  

    # Fecha a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Evita divisão por zero e calcula a alavancagem percentual
    if receita_total == 0:
        alavancagem_percentual = 0  
    else:
        alavancagem_percentual = (despesa_total / receita_total) * 100  

    # Define os dados para o gráfico de pizza
    df = pd.DataFrame({
        "Categoria": ["Alavancagem (Endividamento)", "Capital Restante"],
        "Percentual": [alavancagem_percentual, 100 - alavancagem_percentual]
    })

    # Cria um gráfico de pizza
    fig = px.pie(
        df, 
        names="Categoria", 
        values="Percentual", 
        title="Índice de Alavancagem e Endividamento",
        hole=0.4  # Criando um efeito de "doughnut"
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

def liquidez_corrente():
    # Estabelece conexão com o banco de dados
    conn = conexao_db()
    cursor = conn.cursor()

    # Consulta SQL para calcular o total de receitas entre janeiro a junho de 2025
    cursor.execute("""
        SELECT SUM(valor) 
        FROM controle_receita_despesa 
        WHERE tipo = 'receita' 
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  -- Filtra de janeiro a junho
    """)
    receita = cursor.fetchone()[0] or 0  # Obtém o valor da receita, ou 0 se não houver dados

    # Consulta SQL para calcular o total de despesas entre janeiro a junho de 2025
    cursor.execute("""
        SELECT SUM(valor) 
        FROM controle_receita_despesa 
        WHERE tipo = 'despesa' 
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  -- Filtra de janeiro a junho
    """)
    despesa = cursor.fetchone()[0] or 0  # Obtém o valor da despesa, ou 0 se não houver dados

    # Fecha a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Define os dados para o gráfico de pizza
    df = pd.DataFrame({
        "Categoria": ["Receita Corrente", "Despesa Corrente"],
        "Valor": [receita, despesa]
    })

    # Cria o gráfico de pizza
    fig = px.pie(
        df, 
        names="Categoria", 
        values="Valor", 
        title="Receita vs Despesa",
        hole=0.4  # Efeito "doughnut"
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

def composicao_endividamento():
    # Estabelece conexão com o banco de dados
    conn = conexao_db()
    cursor = conn.cursor()

    # Consulta SQL para calcular o total de despesas circulantes entre janeiro a junho de 2025
    cursor.execute("""
        SELECT SUM(valor) 
        FROM controle_receita_despesa 
        WHERE tipo = 'despesa' 
        AND EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6)  -- Filtra de janeiro a junho
    """)
    despesa_circulante = cursor.fetchone()[0] or 0  # Obtém o valor da despesa circulante, ou 0 se não houver dados

    # Consulta SQL para calcular o total de todas as despesas
    cursor.execute("""
        SELECT SUM(valor) 
        FROM controle_receita_despesa 
        WHERE tipo = 'despesa'
    """)
    despesa_total = cursor.fetchone()[0] or 0  # Obtém o valor total das despesas, ou 0 se não houver dados

    # Fecha a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Evita divisão por zero e calcula o percentual de despesa circulante
    if despesa_total == 0:
        despesa_circulante_percentual = 0  # Evita divisão por zero
    else:
        despesa_circulante_percentual = (despesa_circulante / despesa_total) * 100  # Calcula o percentual

    # Define os dados para o gráfico de pizza
    df = pd.DataFrame({
        "Categoria": ["Despesa Circulante", "Despesa Não Circulante"],
        "Percentual": [despesa_circulante_percentual, 100 - despesa_circulante_percentual]
    })

    # Cria o gráfico de pizza
    fig = px.pie(
        df, 
        names="Categoria", 
        values="Percentual", 
        title="Composição das Despesas (Percentual)",
        hole=0.4  # Efeito "doughnut"
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

def relatorios ():
    margem_bruta()
    lucro_operacional()
    lucro_liquido()
    alavancagem_endividamento()
    liquidez_corrente()
    composicao_endividamento()

# Chamando a função dentro do script Streamlit
if __name__ == "__main__":
    margem_bruta()