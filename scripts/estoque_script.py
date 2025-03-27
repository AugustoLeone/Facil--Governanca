import json
import os

DB_FILE = "banco_de_dados.json"

def carregar_dados():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(DB_FILE, "w") as f:
        json.dump(dados, f, indent=4)

def cadastrar_item(item, categoria, tipo, quantidade, preco_compra):
    dados = carregar_dados()
    if "estoque" not in dados:
        dados["estoque"] = []
    novo_item = {
        "id": len(dados["estoque"]) + 1,
        "item": item,
        "categoria": categoria,
        "tipo": tipo,
        "quantidade": quantidade,
        "preco_compra": preco_compra
    }
    dados["estoque"].append(novo_item)
    salvar_dados(dados)
    return novo_item

def quantidade_estoque(item, categoria):
    dados = carregar_dados()
    if "estoque" not in dados:
        return 0
    for produto in dados["estoque"]:
        if produto["item"] == item and produto["categoria"] == categoria:
            return produto["quantidade"]
    return 0

def adicionar_item(item, categoria, tipo, quantidade):
    dados = carregar_dados()
    if "estoque" not in dados:
        return "Estoque não encontrado."
    for produto in dados["estoque"]:
        if produto["item"] == item and produto["categoria"] == categoria:
            produto["quantidade"] += quantidade
            salvar_dados(dados)
            return produto
    return "Item não encontrado."

def retirar_item(item, categoria, tipo, quantidade):
    dados = carregar_dados()
    if "estoque" not in dados:
        return "Estoque não encontrado."
    for produto in dados["estoque"]:
        if produto["item"] == item and produto["categoria"] == categoria:
            if produto["quantidade"] >= quantidade:
                produto["quantidade"] -= quantidade
                salvar_dados(dados)
                return produto
            else:
                return "Quantidade insuficiente."
    return "Item não encontrado."

def excluir_item(item, categoria, tipo):
    dados = carregar_dados()
    if "estoque" not in dados:
        return "Estoque não encontrado."
    dados["estoque"] = [p for p in dados["estoque"] if not (p["item"] == item and p["categoria"] == categoria)]
    salvar_dados(dados)
    return "Item removido com sucesso."
