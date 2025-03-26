import streamlit as st
from datetime import datetime, time
from scripts.utils import load_data, save_data, get_estacao_tech_project

def cadastrar_professor(json_path: str):
    """Cadastra um novo professor na Estação Tech sem solicitar horários disponíveis."""
    data = load_data(json_path)
    if data is None:
        st.error("Erro ao carregar os dados do projeto.")
        return

    projeto = get_estacao_tech_project(data)
    if projeto is None:
        st.error("Projeto 'Estação Tech' não encontrado. Cadastre o projeto antes.")
        return

    st.header("Cadastrar Professor")
    with st.form("form_cadastrar_professor", clear_on_submit=True):
        nome = st.text_input("Nome Completo")
        especialidades = st.text_input("Especialidades (separadas por vírgula)")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        rua = st.text_input("Rua")
        numero = st.text_input("Numero")
        bairro = st.text_input("Bairro")
        municipio = st.text_input("Município")
        senha = st.text_input("Senha", type="password")  # Campo para a senha
        submitted = st.form_submit_button("Cadastrar Professor")
    
    if submitted:
        if not nome or not email or not senha:
            st.error("Nome, Email e Senha são obrigatórios!")
            return
        novo_professor = {
            "id": len(projeto.get("professores", [])) + 1,
            "nome": nome,
            "especialidades": [s.strip() for s in especialidades.split(",") if s.strip()],
            "dados_pessoais": {
                "email": email,
                "telefone": telefone,
                "rua": rua,
                "numero": numero,
                "bairro": bairro,
                "municipio": municipio,
                "senha": senha
            }
        }
        if "professores" not in projeto:
            st.info("Nenhum professor cadastrado ainda. Por favor, cadastre um professor.")
            projeto["professores"] = []
        projeto["professores"].append(novo_professor)
        save_data(json_path, data)
        st.success(f"Professor {nome} cadastrado com sucesso!")

def cadastrar_curso(json_path: str):
    """
    Cadastro de Curso em etapas:
    
    Passo 1: Informações Básicas – Nome do curso, seleção do professor (lista dos cadastrados)
             e número de dias de aula.
             
    Passo 2: Para cada dia, o gestor informa a data exata e os horários (início e fim) da aula.
    
    Passo 3: Número de vagas e inclusão opcional de alunos (selecionados da lista de alunos cadastrados).
    """
    data = load_data(json_path)
    if data is None:
        st.error("Erro ao carregar os dados.")
        return

    projeto = get_estacao_tech_project(data)
    if projeto is None:
        st.error("Projeto 'Estação Tech' não encontrado.")
        return

    # Inicializa a etapa se não estiver definida
    if "curso_step" not in st.session_state:
        st.session_state.curso_step = 1

    # Passo 1: Informações Básicas
    if st.session_state.curso_step == 1:
        st.header("Passo 1: Informações Básicas do Curso")
        nome_curso = st.text_input("Nome da Cadeira/Curso", key="curso_nome")
        opcoes_prof = {f"{prof['id']} - {prof['nome']}": prof for prof in projeto.get("professores", [])}
        professor_sel = st.selectbox("Selecione o Professor", list(opcoes_prof.keys()), key="curso_prof")
        num_dias = st.number_input("Número de dias de aula", min_value=1, value=1, step=1, key="curso_num_dias")
        if st.button("Próximo - Passo 2"):
            if nome_curso and num_dias:
                st.session_state.curso_info = {
                    "nome_curso": nome_curso,
                    "professor_id": opcoes_prof[professor_sel]["id"],
                    "num_dias": int(num_dias)
                }
                st.session_state.curso_step = 2
            else:
                st.error("Preencha todos os campos!")

    # Passo 2: Datas e Horários das Aulas
    elif st.session_state.curso_step == 2:
        st.header("Passo 2: Datas e Horários das Aulas")
        num_dias = st.session_state.curso_info["num_dias"]
        aulas = []
        for i in range(num_dias):
            st.subheader(f"Aula {i+1}")
            data_aula = st.date_input(f"Data da Aula {i+1}", key=f"data_aula_{i}")
            hora_inicio = st.time_input(f"Horário de Início da Aula {i+1}", key=f"hora_inicio_{i}", value=time(8,0))
            hora_fim = st.time_input(f"Horário de Fim da Aula {i+1}", key=f"hora_fim_{i}", value=time(12,0))
            aulas.append({
                "data": data_aula.isoformat(),
                "horario": {
                    "inicio": hora_inicio.strftime("%H:%M"),
                    "fim": hora_fim.strftime("%H:%M")
                }
            })
        if st.button("Próximo - Passo 3"):
            st.session_state.aulas = aulas
            st.session_state.curso_step = 3

    # Passo 3: Vagas e Inclusão de Alunos
    elif st.session_state.curso_step == 3:
        st.header("Passo 3: Vagas e Inclusão de Alunos")
        num_vagas = st.number_input("Número de vagas", min_value=1, value=10, step=1, key="curso_num_vagas")
        # Carrega os alunos cadastrados no projeto
        alunos_disponiveis = projeto.get("alunos", [])
        if alunos_disponiveis:
            alunos_opcoes = {f"{aluno['id']} - {aluno['nome']}": aluno for aluno in alunos_disponiveis}
            alunos_selecionados = st.multiselect("Selecione os alunos a serem incluídos (opcional)", list(alunos_opcoes.keys()), key="curso_alunos")
        else:
            alunos_selecionados = []
            st.info("Nenhum aluno cadastrado no sistema para inclusão.")
        if st.button("Finalizar Cadastro do Curso"):
            curso_info = st.session_state.curso_info
            novo_curso = {
                "id": len(projeto.get("turmas", [])) + 1,
                "nome_curso": curso_info["nome_curso"],
                "professor_id": curso_info["professor_id"],
                "aulas": st.session_state.aulas,
                "numero_vagas": int(num_vagas),
                "alunos": [alunos_opcoes[sel]["id"] for sel in alunos_selecionados] if alunos_selecionados else []
            }
            if "turmas" not in projeto:
                projeto["turmas"] = []
            projeto["turmas"].append(novo_curso)
            save_data(json_path, data)
            st.success(f"Curso '{curso_info['nome_curso']}' cadastrado com sucesso!")
            # Reinicia o processo para um novo cadastro
            st.session_state.curso_step = 1
            for key in list(st.session_state.keys()):
                if key.startswith("curso_") or key.startswith("data_aula_") or key.startswith("hora_"):
                    del st.session_state[key]
            if "curso_info" in st.session_state:
                del st.session_state.curso_info
            if "aulas" in st.session_state:
                del st.session_state.aulas

def cadastrar_turma(json_path: str):
    """
    Atribui um aluno a uma turma existente, registrando frequência e aprovação.
    Agora, impede que o gestor cadastre um aluno que não está cadastrado no sistema.
    Mostra o nome do aluno no selectbox (ao invés do email).
    """
    from scripts.utils import load_data, save_data, get_estacao_tech_project
    import streamlit as st

    data = load_data(json_path)
    if data is None:
        st.error("Erro ao carregar os dados do JSON.")
        return

    projeto = get_estacao_tech_project(data)
    if projeto is None:
        st.error("Projeto 'Estação Tech' não encontrado.")
        return

    if "turmas" not in projeto or len(projeto["turmas"]) == 0:
        st.error("Nenhum curso cadastrado. Cadastre um curso primeiro.")
        return

    # Carrega todos os alunos cadastrados no sistema
    alunos_cadastrados = projeto.get("alunos", [])
    # Cria um dicionário de alunos pelo ID
    alunos_por_id = {aluno["id"]: aluno for aluno in alunos_cadastrados}

    st.header("Atribuir Aluno à Turma")
    with st.form("form_atribuir_aluno", clear_on_submit=True):
        # Seleciona a turma
        opcoes_turmas = {f"{turma['id']} - {turma['nome_curso']}": turma for turma in projeto["turmas"]}
        turma_sel = st.selectbox("Selecione o Curso/Turma", list(opcoes_turmas.keys()), key="turma_select")
        turma = opcoes_turmas[turma_sel]
        st.markdown("### Dados do Aluno")

        if not alunos_por_id:
            st.info("Não há alunos cadastrados no sistema. Cadastre alunos antes de atribuí-los a uma turma.")
            st.stop()

        # Exibe selectbox mostrando o ID e o NOME do aluno
        opcoes_alunos = {
            f"{a['id']} - {a['nome']}": a  # AQUI USAMOS 'nome'
            for a in alunos_cadastrados
        }
        aluno_sel = st.selectbox("Selecione o Aluno", list(opcoes_alunos.keys()))
        aluno_id = opcoes_alunos[aluno_sel]["id"]

        frequencia = st.number_input("Frequência (%)", min_value=0, max_value=100, step=1)
        aprovacao = st.selectbox("Aprovação", options=["Pendente", "Aprovado", "Reprovado"], key="turma_aprovacao")
        submitted = st.form_submit_button("Atribuir Aluno")

    if submitted:
        # Verifica se o aluno ID existe no sistema
        if aluno_id not in alunos_por_id:
            st.error(f"O aluno com ID {aluno_id} não está cadastrado no sistema. Cadastre-o primeiro.")
            return

        # Prossegue normalmente
        if not turma.get("alunos"):
            turma["alunos"] = []
        novo_aluno = {
            "id": aluno_id,
            "nome": alunos_por_id[aluno_id]["nome"],
            "frequencia": frequencia,
            "aprovado": aprovacao
        }
        turma["alunos"].append(novo_aluno)
        save_data(json_path, data)
        st.success(f"Aluno '{novo_aluno['nome']}' atribuído à turma '{turma['nome_curso']}' com sucesso!")

def visualizar_turmas(json_path: str):
    """
    Visualiza as turmas cadastradas e exibe os detalhes, incluindo a lista de alunos.
    Se algum aluno for apenas um ID (int), exibe de forma adequada para não dar erro.
    """

    data = load_data(json_path)
    if data is None:
        return
    projeto = get_estacao_tech_project(data)
    if projeto is None:
        return
    turmas = projeto.get("turmas", [])
    st.header("Visualização de Turmas")
    if not turmas:
        st.info("Nenhuma turma cadastrada.")
        return

    for turma in turmas:
        turma_id = turma.get("id", "N/D")
        nome_curso = turma.get("nome_curso", "N/D")
        st.markdown(f"### Turma {turma_id} - {nome_curso}")
        st.write(f"Professor ID: {turma.get('professor_id', 'N/D')}")

        # Verifica e exibe dados de datas ou dias de aula
        if "datas_aula" in turma:
            st.write("Datas de Aula:")
            for d in turma["datas_aula"]:
                st.write(f"- {d}")
        elif "aulas" in turma and turma["aulas"]:
            st.write("Aulas definidas (data e horário):")
            for aula in turma["aulas"]:
                data_aula = aula.get("data", "N/D")
                horario_inicio = aula.get("horario", {}).get("inicio", "N/D")
                horario_fim = aula.get("horario", {}).get("fim", "N/D")
                st.write(f"- Data: {data_aula}, {horario_inicio} às {horario_fim}")
        elif "dias_aula" in turma:
            dias = turma["dias_aula"]
            st.write("Dias de Aula: " + ", ".join(dias) if dias else "Dias de Aula: Não definido")
        else:
            st.write("Não há datas ou dias de aula definidos para esta turma.")

        # Verifica se a turma possui informações de horário
        if "horario" in turma:
            inicio = turma["horario"].get("inicio", "N/D")
            fim = turma["horario"].get("fim", "N/D")
            st.write(f"Horário Geral: {inicio} às {fim}")
        else:
            st.write("Horário Geral: Não definido. Cadastre o horário no app do gestor.")

        # Exibe dados de alunos
        alunos_na_turma = turma.get("alunos", [])
        st.write(f"Total de Alunos: {len(alunos_na_turma)}")
        st.markdown("**Alunos:**")
        if not alunos_na_turma:
            st.write("Nenhum aluno cadastrado nesta turma.")
        else:
            for aluno in alunos_na_turma:
                # Se aluno for um dict com dados
                if isinstance(aluno, dict):
                    a_id = aluno.get("id", "N/D")
                    a_nome = aluno.get("nome", "N/D")
                    frequencia = aluno.get("frequencia", "N/A")
                    aprovado = aluno.get("aprovado", "N/A")
                    st.markdown(f"- {a_id} - {a_nome} (Frequência: {frequencia}%, Situação: {aprovado})")
                # Se aluno for apenas um ID (int)
                elif isinstance(aluno, int):
                    st.markdown(f"- Aluno ID: {aluno}")
                else:
                    st.markdown(f"- Formato de aluno não reconhecido: {aluno}")

        st.markdown("---")
