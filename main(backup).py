import streamlit as st
import json
import os

JSON_PATH = os.path.join("data", "sec_tecnologia.json")

def carregar_dados(json_path: str):
    """Carrega os dados do JSON especificado."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Arquivo JSON não encontrado.")
        return None
    except json.JSONDecodeError:
        st.error("Erro ao decodificar o JSON.")
        return None

def exibir_funcionamento_secretaria(dados):
    """Exibe as informações de funcionamento da Secretaria."""
    st.title(f"Funcionamento - {dados['nome_secretaria']}")
    funcionamento = dados["funcionamento"]

    st.write("### Horário de Atendimento")
    st.write(funcionamento["horario"])

    st.write("### Dias de Atendimento")
    st.write(", ".join(funcionamento["dias_semana"]))

    st.write("### Local de Atendimento")
    st.write(funcionamento["local_atendimento"])

    st.write("### Meios de Contato")
    st.write(f"📞 *Telefone:* {funcionamento['meios_contato']['telefone']}")
    st.write(f"📧 *E-mail:* {funcionamento['meios_contato']['email']}")
    st.write(f"🌐 *Site:* {funcionamento['meios_contato']['site']}")

    st.write("### Responsável pela Secretaria")
    responsavel = funcionamento["responsavel_pela_secretaria"]
    st.write(f"👤 *Nome:* {responsavel['nome']}")
    st.write(f"🏢 *Cargo:* {responsavel['cargo']}")

def exibir_andamento_projetos(dados):
    """Exibe o andamento dos projetos ativos, incluindo módulos, professores e turmas."""
    st.title("Projetos Ativos")
    for projeto in dados["projetos_ativos"]:
        st.subheader(projeto["nome_projeto"])
        st.write(f"*Descrição:* {projeto['descricao']}")
        st.write(f"*Data de Início:* {projeto['data_inicio']}")
        st.write(f"*Data Prevista de Término:* {projeto['data_prevista_fim']}")
        st.write(f"*Status:* {projeto['status']}")
        st.write(f"👤 *Coordenador:* {projeto['coordenador']}")
        st.write(f"🤝 *Parcerias:* {', '.join(projeto['parcerias'])}")
        
        st.write("### 📚 Módulos do Projeto")
        for modulo in projeto["modulos"]:
            st.write(f"- *{modulo['nome_modulo']}*")
            st.write(f"  📌 Duração: {modulo['duracao_horas']} horas")
            st.write(f"  👨‍🏫 Instrutor: {modulo['instrutor']}")
            st.progress(modulo["percentual_conclusao"] / 100)
        
        # Exibir professores, se houver
        if "professores" in projeto and projeto["professores"]:
            st.write("### 👨‍🏫 Professores")
            for prof in projeto["professores"]:
                st.write(f"- *ID:* {prof['id']} | *Nome:* {prof['nome']}")
                st.write(f"  *Especialidades:* {', '.join(prof.get('especialidades', []))}")
                st.write(f"  *Contato:* Email: {prof['dados_pessoais'].get('email', 'N/A')} | Tel: {prof['dados_pessoais'].get('telefone', 'N/A')}")
        
        # Exibir turmas, se houver
        if "turmas" in projeto and projeto["turmas"]:
            st.write("### 🏫 Turmas")
            for turma in projeto["turmas"]:
                st.write(f"- *Turma {turma['id']} - {turma['nome_curso']}*")
                st.write(f"  *Professor ID:* {turma['professor_id']}")
                st.write(f"  *Dias de Aula:* {', '.join(turma.get('dias_aula', []))}")
                st.write(f"  *Horário:* {turma['horario']['inicio']} às {turma['horario']['fim']}")
                st.write(f"  *Total de Alunos:* {len(turma.get('alunos', []))}")
        
        st.write("---")

def exibir_indicadores_gestao(dados):
    """Exibe os indicadores gerais da Secretaria e dos projetos, incluindo indicadores dos professores."""
    st.title("📊 Indicadores de Gestão")

    # Indicadores gerais da secretaria
    indicadores_gerais = dados["indicadores_gerais"]
    st.subheader("Indicadores Gerais da Secretaria")
    for chave, valor in indicadores_gerais.items():
        st.write(f"{chave.replace('_', ' ').title()}:** {valor}")

    st.write("---")

    # Indicadores por projeto
    st.subheader("Indicadores por Projeto")
    for projeto in dados["projetos_ativos"]:
        st.markdown(f"### {projeto['nome_projeto']}")
        # Indicadores gerais do projeto
        indicadores_projeto = projeto.get("indicadores", {})
        for chave, valor in indicadores_projeto.items():
            st.write(f"{chave.replace('_', ' ').title()}:** {valor}")
        # Indicadores dos professores, se existentes
        if "indicadores_professores" in projeto:
            st.write("*Indicadores dos Professores:*")
            for chave, valor in projeto["indicadores_professores"].items():
                st.write(f"- *{chave.replace('_', ' ').title()}:* {valor}")
        st.write("---")

def exibir_alunos(dados):
    """Exibe informações detalhadas sobre os alunos cadastrados no projeto."""
    st.title("👨‍🎓 Alunos Inscritos")
    for projeto in dados["projetos_ativos"]:
        st.subheader(f"📌 {projeto['nome_projeto']}")
        alunos = projeto.get("alunos", [])
        if not alunos:
            st.write("Nenhum aluno cadastrado.")
        for aluno in alunos:
            st.write(f"*Nome:* {aluno['nome']}")
            st.write(f"📧 *E-mail:* {aluno['email']}")
            st.write(f"🎓 *Módulos Concluídos:* {', '.join(aluno['modulos_concluidos']) if aluno['modulos_concluidos'] else 'Nenhum'}")
            st.write(f"📜 *Certificações Obtidas:* {', '.join(aluno['certificacoes_obtidas']) if aluno['certificacoes_obtidas'] else 'Nenhuma'}")
            st.write(f"💰 *Ticket Médio:* R$ {aluno['ticket_medio']:.2f}")
            st.write("---")

def atualizar_json(json_path: str, chave: str, valor):
    """Atualiza um campo específico no JSON e salva as alterações."""
    dados = carregar_dados(json_path)
    if not dados:
        return
    
    dados[chave] = valor
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    st.success(f"O campo '{chave}' foi atualizado com sucesso!")

def main():
    """Interface principal com abas."""
    st.sidebar.title("📌 Secretaria de Tecnologia")
    
    json_path = st.sidebar.text_input("Caminho do JSON", JSON_PATH)

    dados = carregar_dados(json_path)
    if not dados:
        return

    abas = st.sidebar.radio("Navegar", ["Funcionamento", "Projetos", "Indicadores", "Alunos"])

    if abas == "Funcionamento":
        exibir_funcionamento_secretaria(dados)
    elif abas == "Projetos":
        exibir_andamento_projetos(dados)
    elif abas == "Indicadores":
        exibir_indicadores_gestao(dados)
    elif abas == "Alunos":
        exibir_alunos(dados)

if __name__ == "__main__":
    main()