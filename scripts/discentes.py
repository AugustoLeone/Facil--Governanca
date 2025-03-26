import streamlit as st
from scripts.utils import load_data, save_data, get_estacao_tech_project

def cadastrar_aluno(json_path: str):
    """
    Cadastra um novo aluno na Estação Tech, incluindo campos adicionais:
    Etnia, Endereço, CPF, Telefone 1 e 2, Escolaridade, Escola (caso estude),
    e nomes completos do pai e da mãe.
    """
    data = load_data(json_path)
    if data is None:
        st.error("Erro ao carregar os dados do JSON.")
        return

    projeto = get_estacao_tech_project(data)
    if projeto is None:
        st.error("Projeto 'Estação Tech' não encontrado.")
        return

    st.header("Cadastrar Aluno")
    alunos = projeto.get("alunos", [])
    st.write(f"Número de alunos cadastrados: {len(alunos)}")

    opcoes_escolaridade = [
        "Analfabeto",
        "Ensino Fundamental 1",
        "Ensino Fundamental 2",
        "Ensino Médio",
        "Ensino Superior"
    ]

    with st.form("form_cadastrar_aluno", clear_on_submit=True):
        nome = st.text_input("Nome do Aluno")
        idade = st.number_input("Idade", min_value=0, step=1)
        email = st.text_input("E-mail")
        
        st.markdown("### Dados Adicionais:")
        etnia = st.text_input("Etnia")
        rua = st.text_input("Rua")
        numero = st.text_input("Numero")
        bairro = st.text_input("Bairro")
        municipio = st.text_input("Muncipio")
        cpf = st.text_input("CPF")
        telefone1 = st.text_input("Telefone 1")
        telefone2 = st.text_input("Telefone 2")
        escolaridade = st.selectbox("Escolaridade", opcoes_escolaridade)
        escola_atual = st.text_input("Escola em que estuda (deixe em branco se não se aplica)")
        nome_pai = st.text_input("Nome completo do pai")
        nome_mae = st.text_input("Nome completo da mãe")

        submitted = st.form_submit_button("Cadastrar")
    
    if submitted:
        if not nome or not email:
            st.error("Nome e E-mail são obrigatórios!")
            return
        
        novo_aluno = {
            "id": len(alunos) + 1,
            "nome": nome,
            "idade": idade,
            "email": email,
            "modulos_concluidos": [],
            "certificacoes_obtidas": [],
            "informacoes_extra": {
                "etnia": etnia,
                "rua": rua,
                "numero":numero,
                "bairro":bairro,
                "municipio":municipio,
                "cpf": cpf,
                "telefone1": telefone1,
                "telefone2": telefone2,
                "escolaridade": escolaridade,
                "escola_atual": escola_atual,
                "nome_pai": nome_pai,
                "nome_mae": nome_mae
            }
        }

        if "alunos" not in projeto:
            projeto["alunos"] = []
        projeto["alunos"].append(novo_aluno)
        
        if "indicadores" in projeto:
            projeto["indicadores"]["total_inscritos"] = len(projeto["alunos"])
        
        save_data(json_path, data)
        st.success(f"Aluno '{nome}' cadastrado com sucesso!")

def emitir_certificado(json_path: str):
    """Emite um certificado para um aluno e atualiza o histórico."""
    data = load_data(json_path)
    if data is None:
        return

    projeto = get_estacao_tech_project(data)
    if projeto is None:
        return

    st.header("Emitir Certificado")
    alunos = projeto.get("alunos", [])
    if not alunos:
        st.info("Nenhum aluno cadastrado.")
        return

    opcoes_alunos = {f"{aluno['id']} - {aluno['nome']}": aluno for aluno in alunos}
    aluno_selecionado = st.selectbox("Selecione o aluno", list(opcoes_alunos.keys()), key="emitir_certificado_selectbox")
    aluno = opcoes_alunos[aluno_selecionado]
    
    with st.form("form_emitir_certificado", clear_on_submit=True):
        nome_certificado = st.text_input("Nome do Curso/Certificado")
        submitted = st.form_submit_button("Emitir Certificado")
    
    if submitted:
        if not nome_certificado:
            st.error("O nome do certificado é obrigatório!")
            return
        
        if "certificacoes_obtidas" not in aluno:
            aluno["certificacoes_obtidas"] = []
        aluno["certificacoes_obtidas"].append(nome_certificado)
        
        if "indicadores" in projeto:
            if "numero_certificados_emitidos" in projeto["indicadores"]:
                projeto["indicadores"]["numero_certificados_emitidos"] += 1
            else:
                projeto["indicadores"]["numero_certificados_emitidos"] = 1
        
        save_data(json_path, data)
        st.success(f"Certificado '{nome_certificado}' emitido para {aluno['nome']}!")

def consultar_aluno(json_path: str):
    """
    Consulta e exibe os dados de um aluno, incluindo campos adicionais:
    etnia, endereço, CPF, telefones, escolaridade, escola, nomes do pai e mãe.
    """
    data = load_data(json_path)
    if data is None:
        st.error("Erro ao carregar o JSON.")
        return

    projeto = get_estacao_tech_project(data)
    if projeto is None:
        st.error("Projeto 'Estação Tech' não encontrado.")
        return

    st.header("Consultar Aluno")
    alunos = projeto.get("alunos", [])
    if not alunos:
        st.info("Nenhum aluno cadastrado.")
        return

    # Cria um dicionário de alunos por ID e nome
    opcoes_alunos = {f"{aluno['id']} - {aluno['nome']}": aluno for aluno in alunos}
    aluno_selecionado = st.selectbox(
        "Selecione o aluno",
        list(opcoes_alunos.keys()),
        key="consultar_aluno_selectbox"
    )
    aluno = opcoes_alunos[aluno_selecionado]

    st.subheader(f"Dados do Aluno: {aluno['nome']}")
    st.write(f"**ID:** {aluno['id']}")
    st.write(f"**Nome:** {aluno['nome']}")
    st.write(f"**Idade:** {aluno['idade']}")
    st.write(f"**E-mail:** {aluno['email']}")

    # Campos adicionais ficam em informacoes_extra
    info_extra = aluno.get("informacoes_extra", {})
    if info_extra:
        st.markdown("### Informações Extras:")
        etnia = info_extra.get("etnia", "N/D")
        rua = info_extra.get("rua", "N/D")
        numero = info_extra.get("numero", "N/D")
        bairro = info_extra.get("bairro", "N/D")
        municipio = info_extra.get("municipio", "N/D")
        cpf = info_extra.get("cpf", "N/D")
        telefone1 = info_extra.get("telefone1", "N/D")
        telefone2 = info_extra.get("telefone2", "N/D")
        escolaridade = info_extra.get("escolaridade", "N/D")
        escola_atual = info_extra.get("escola_atual", "N/D")
        nome_pai = info_extra.get("nome_pai", "N/D")
        nome_mae = info_extra.get("nome_mae", "N/D")

        st.write(f"**Etnia:** {etnia}")
        st.write(f"**Endereço:** {rua}, {numero}, {bairro}, {municipio}")
        st.write(f"**CPF:** {cpf}")
        st.write(f"**Telefone 1:** {telefone1}")
        st.write(f"**Telefone 2:** {telefone2}")
        st.write(f"**Escolaridade:** {escolaridade}")
        if escola_atual.strip():
            st.write(f"**Escola em que estuda:** {escola_atual}")
        else:
            st.write("**Escola em que estuda:** Não se aplica/Não informado")
        st.write(f"**Nome do Pai:** {nome_pai}")
        st.write(f"**Nome da Mãe:** {nome_mae}")

    st.markdown("### Módulos Concluídos:")
    if aluno.get("modulos_concluidos"):
        st.write(", ".join(aluno["modulos_concluidos"]))
    else:
        st.write("Nenhum módulo concluído.")

    st.markdown("### Certificações Obtidas:")
    if aluno.get("certificacoes_obtidas"):
        st.write(", ".join(aluno["certificacoes_obtidas"]))
    else:
        st.write("Nenhuma certificação obtida.")
