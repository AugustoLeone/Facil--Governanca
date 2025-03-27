import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Função para carregar o banco de dados em JSON
def carregar_dados_json():
    with open("banco_de_dados.json", "r") as file:
        return json.load(file)

# Função para calcular a margem bruta
def margem_bruta():
    dados = carregar_dados_json()
    
    # Filtra as receitas e calcula a receita total por mês
    receitas = [
        (item["data"][:7], item["valor"]) for item in dados["controle_receita_despesa"]
        if item["tipo"] == "receita" and int(item["data"][5:7]) <= 6
    ]
    
    # Agrupa as receitas por mês
    df = pd.DataFrame(receitas, columns=["Mês", "Receita Total"])
    df = df.groupby("Mês").sum().reset_index()

    # Cria o gráfico de linha
    fig = px.line(df, x="Mês", y="Receita Total", markers=True, title="Receita Total por Mês")
    st.plotly_chart(fig)

# Função para calcular o lucro operacional
def lucro_operacional():
    dados = carregar_dados_json()

    # Filtra as receitas e despesas operacionais por mês
    receitas = {
        item["data"][:7]: item["valor"]
        for item in dados["controle_receita_despesa"]
        if item["tipo"] == "receita" and int(item["data"][5:7]) <= 6
    }

    despesas = {
        item["data"][:7]: item["valor"]
        for item in dados["controle_receita_despesa"]
        if item["tipo"] == "despesa" and item["categoria"] in ['salario', 'manutenção'] and int(item["data"][5:7]) <= 6
    }

    # Meses
    meses = sorted(set(receitas.keys()) | set(despesas.keys()))
    
    # Cria o DataFrame
    df = pd.DataFrame({
        "Mês": meses,
        "Receita Total": [receitas.get(mes, 0) for mes in meses],
        "Despesa Operacional": [despesas.get(mes, 0) for mes in meses]
    })
    
    df["Lucro Operacional"] = df["Receita Total"] - df["Despesa Operacional"]
    
    # Cria o gráfico de barras
    fig = px.bar(df, x="Mês", y="Lucro Operacional", title="Lucro Operacional por Mês", text_auto=True)
    st.plotly_chart(fig)

# Função para calcular o lucro líquido
def lucro_liquido():
    dados = carregar_dados_json()

    # Filtra as receitas e despesas totais por mês
    receitas = {
        item["data"][:7]: item["valor"]
        for item in dados["controle_receita_despesa"]
        if item["tipo"] == "receita" and int(item["data"][5:7]) <= 6
    }

    despesas = {
        item["data"][:7]: item["valor"]
        for item in dados["controle_receita_despesa"]
        if item["tipo"] == "despesa" and int(item["data"][5:7]) <= 6
    }

    # Meses
    meses = ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06']
    
    # Cria o DataFrame
    df = pd.DataFrame({
        "Mês": meses,
        "Receita Total": [receitas.get(mes, 0) for mes in meses],
        "Despesa Total": [despesas.get(mes, 0) for mes in meses]
    })
    
    df["Lucro Líquido"] = df["Receita Total"] - df["Despesa Total"]
    
    # Cria o gráfico de barras
    fig = px.bar(df, x="Mês", y="Lucro Líquido", title="Lucro Líquido por Mês", text_auto=True, labels={"Lucro Líquido": "Valor (R$)"})
    st.plotly_chart(fig)

# Função para calcular a alavancagem de endividamento
def alavancagem_endividamento():
    dados = carregar_dados_json()

    # Calcula a receita total de janeiro a junho
    receita_total = sum(
        item["valor"] for item in dados["controle_receita_despesa"]
        if item["tipo"] == "receita" and int(item["data"][5:7]) <= 6
    )

    # Calcula a despesa total de janeiro a junho
    despesa_total = sum(
        item["valor"] for item in dados["controle_receita_despesa"]
        if item["tipo"] == "despesa" and int(item["data"][5:7]) <= 6
    )

    # Calcula o índice de alavancagem
    if receita_total == 0:
        alavancagem_percentual = 0
    else:
        alavancagem_percentual = (despesa_total / receita_total) * 100

    # Cria o gráfico de pizza
    df = pd.DataFrame({
        "Categoria": ["Alavancagem (Endividamento)", "Capital Restante"],
        "Percentual": [alavancagem_percentual, 100 - alavancagem_percentual]
    })
    
    fig = px.pie(df, names="Categoria", values="Percentual", title="Índice de Alavancagem e Endividamento", hole=0.4)
    st.plotly_chart(fig)

# Função para calcular a liquidez corrente
def liquidez_corrente():
    dados = carregar_dados_json()

    # Calcula a receita total de janeiro a junho
    receita = sum(
        item["valor"] for item in dados["controle_receita_despesa"]
        if item["tipo"] == "receita" and int(item["data"][5:7]) <= 6
    )

    # Calcula a despesa total de janeiro a junho
    despesa = sum(
        item["valor"] for item in dados["controle_receita_despesa"]
        if item["tipo"] == "despesa" and int(item["data"][5:7]) <= 6
    )

    # Cria o gráfico de pizza
    df = pd.DataFrame({
        "Categoria": ["Receita Corrente", "Despesa Corrente"],
        "Valor": [receita, despesa]
    })

    fig = px.pie(df, names="Categoria", values="Valor", title="Receita vs Despesa", hole=0.4)
    st.plotly_chart(fig)

# Função para calcular a composição de endividamento
def composicao_endividamento():
    dados = carregar_dados_json()

    # Calcula a despesa circulante e total
    despesa_circulante = sum(
        item["valor"] for item in dados["controle_receita_despesa"]
        if item["tipo"] == "despesa" and item["categoria"] == "circulante" and int(item["data"][5:7]) <= 6
    )

    despesa_total = sum(
        item["valor"] for item in dados["controle_receita_despesa"]
        if item["tipo"] == "despesa"
    )

    # Calcula o percentual de despesa circulante
    if despesa_total == 0:
        despesa_circulante_percentual = 0
    else:
        despesa_circulante_percentual = (despesa_circulante / despesa_total) * 100

    # Cria o gráfico de pizza
    df = pd.DataFrame({
        "Categoria": ["Despesa Circulante", "Despesa Não Circulante"],
        "Percentual": [despesa_circulante_percentual, 100 - despesa_circulante_percentual]
    })

    fig = px.pie(df, names="Categoria", values="Percentual", title="Composição das Despesas (Percentual)", hole=0.4)
    st.plotly_chart(fig)

# Função que chama todas as funções de relatórios
def relatorios():
    margem_bruta()
    lucro_operacional()
    lucro_liquido()
    alavancagem_endividamento()
    liquidez_corrente()
    composicao_endividamento()

# Chamando a função dentro do script Streamlit
if __name__ == "__main__":
    relatorios()
