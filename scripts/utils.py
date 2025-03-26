import json
import streamlit as st

def load_data(json_path: str):
    """Carrega os dados do JSON especificado."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar o JSON: {e}")
        return None

def save_data(json_path: str, data):
    """Salva os dados atualizados no JSON."""
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        st.success("Dados salvos com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar o JSON: {e}")

def get_estacao_tech_project(data):
    """Retorna o projeto 'Estação Tech' presente em 'projetos_ativos'."""
    for projeto in data.get("projetos_ativos", []):
        if projeto.get("nome_projeto") == "Estação Tech":
            return projeto
    st.error("Projeto 'Estação Tech' não encontrado.")
    return None
