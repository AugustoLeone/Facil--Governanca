# pages/professor.py

import streamlit as st
import streamlit.components.v1 as components
import datetime
import json
import sqlite3
from datetime import date
from scripts.config import JSON_PATH
from scripts.utils import load_data

# ------------------ Inicializa o banco de dados de presenças ------------------
def init_attendance_db():
    conn = sqlite3.connect("attendance.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            student_id INTEGER,
            date TEXT,
            present INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_attendance_db()

# ------------------ Funções de login e logout ------------------
def teacher_login():
    """Tela de login para professores."""
    st.title("Login - Área do Professor")
    teacher_username = st.text_input("Nome de usuário:")
    teacher_password = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        data = load_data(JSON_PATH)
        if data:
            for projeto in data.get("projetos_ativos", []):
                if projeto.get("nome_projeto") == "Estação Tech":
                    professores = projeto.get("professores", [])
                    for prof in professores:
                        if (prof.get("nome", "").strip().lower() == teacher_username.strip().lower()
                            and prof.get("dados_pessoais", {}).get("senha", "") == teacher_password):
                            st.session_state.logged_in_teacher = True
                            st.session_state.teacher_name = teacher_username
                            st.session_state.teacher_id = prof.get("id")
                            st.success(f"Bem-vindo, {teacher_username}!")
                            # Após login, direcionamos ao professor_home
                            st.session_state.view = "professor_home"
                            return
                    st.error("Credenciais inválidas. Verifique seu cadastro no app do gestor.")
                    return
        st.error("Erro ao carregar os dados. Tente novamente mais tarde.")

# ------------------ Funções utilitárias ------------------
def show_calendar():
    """Gera e retorna o HTML de um calendário (FullCalendar) com as aulas do professor logado."""
    data = load_data(JSON_PATH)
    teacher_id = st.session_state.get("teacher_id")
    events = []
    if data:
        for projeto in data.get("projetos_ativos", []):
            if projeto.get("nome_projeto") == "Estação Tech":
                turmas = projeto.get("turmas", [])
                for turma in turmas:
                    if turma.get("professor_id") == teacher_id:
                        # Se tiver datas_aula (exatas)
                        if "datas_aula" in turma:
                            for d in turma["datas_aula"]:
                                event = {
                                    "title": turma.get("nome_curso", "Curso"),
                                    "start": d + "T" + turma.get("horario", {}).get("inicio", "00:00"),
                                    "end": d + "T" + turma.get("horario", {}).get("fim", "00:00")
                                }
                                events.append(event)
                        # Se tiver aulas detalhadas (lista)
                        elif "aulas" in turma:
                            for aula in turma["aulas"]:
                                data_aula = aula.get("data")
                                inicio = aula.get("horario", {}).get("inicio", "00:00")
                                fim = aula.get("horario", {}).get("fim", "00:00")
                                event = {
                                    "title": turma.get("nome_curso", "Curso"),
                                    "start": data_aula + "T" + inicio,
                                    "end": data_aula + "T" + fim
                                }
                                events.append(event)
                        # Se tiver dias_aula (recorrentes)
                        elif "dias_aula" in turma:
                            day_map = {
                                "segunda": 1,
                                "terca": 2,
                                "quarta": 3,
                                "quinta": 4,
                                "sexta": 5,
                                "sabado": 6,
                                "domingo": 0
                            }
                            daysOfWeek = [
                                day_map[day.lower()]
                                for day in turma["dias_aula"]
                                if day.lower() in day_map
                            ]
                            event = {
                                "title": turma.get("nome_curso", "Curso"),
                                "daysOfWeek": daysOfWeek,
                                "startTime": turma.get("horario", {}).get("inicio", "00:00"),
                                "endTime": turma.get("horario", {}).get("fim", "00:00")
                            }
                            events.append(event)
                break
    events_json = json.dumps(events)
    html_code = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/index.global.min.css' rel='stylesheet' />
        <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/index.global.min.js'></script>
        <style>
          body {{
            margin: 0;
            padding: 0;
            font-family: Arial, Helvetica, sans-serif;
          }}
          #calendar {{
            max-width: 900px;
            margin: 40px auto;
          }}
        </style>
      </head>
      <body>
        <div id='calendar'></div>
        <script>
          document.addEventListener('DOMContentLoaded', function() {{
            var calendarEl = document.getElementById('calendar');
            var calendar = new FullCalendar.Calendar(calendarEl, {{
              initialView: 'dayGridMonth',
              headerToolbar: {{
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
              }},
              events: {events_json},
              eventTimeFormat: {{ hour: '2-digit', minute: '2-digit', hour12: false }},
            }});
            calendar.render();
          }});
        </script>
      </body>
    </html>
    """
    return html_code

def check_class_today():
    """Verifica se o professor tem aula hoje, retornando a lista de turmas que ocorrem na data atual."""
    data = load_data(JSON_PATH)
    teacher_id = st.session_state.get("teacher_id")
    today = datetime.date.today().isoformat()
    courses_today = []
    if data:
        for projeto in data.get("projetos_ativos", []):
            if projeto.get("nome_projeto") == "Estação Tech":
                turmas = projeto.get("turmas", [])
                for turma in turmas:
                    if turma.get("professor_id") == teacher_id:
                        # Se a turma possui datas exatas
                        if "datas_aula" in turma and today in turma["datas_aula"]:
                            courses_today.append(turma)
                        # Se a turma possui aulas detalhadas
                        elif "aulas" in turma:
                            for aula in turma["aulas"]:
                                if aula.get("data") == today:
                                    courses_today.append(turma)
                                    break
    return courses_today

# ------------------ Funções de Presença ------------------
def init_db():
    conn = sqlite3.connect("attendance.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            student_id INTEGER,
            date TEXT,
            present INTEGER
        )
    """)
    conn.commit()
    conn.close()

def existing_attendance_today(course_id, date_str):
    """
    Retorna True se já existir chamada registrada para o (course_id, date_str).
    """
    conn = sqlite3.connect("attendance.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE course_id = ? AND date = ?
    """, (course_id, date_str))
    count = cursor.fetchone()[0]
    conn.close()
    return (count > 0)

def remove_attendance_today(course_id, date_str):
    """
    Remove os registros de chamada do (course_id, date_str).
    """
    conn = sqlite3.connect("attendance.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM attendance
        WHERE course_id = ? AND date = ?
    """, (course_id, date_str))
    conn.commit()
    conn.close()

def insert_attendance(course_id, attendance_list, date_str):
    """
    Insere os registros de presença para (course_id, date_str).
    """
    conn = sqlite3.connect("attendance.db", check_same_thread=False)
    cursor = conn.cursor()
    for student_id, present in attendance_list:
        cursor.execute("""
            INSERT INTO attendance (course_id, student_id, date, present)
            VALUES (?, ?, ?, ?)
        """, (course_id, student_id, date_str, int(present)))
    conn.commit()
    conn.close()

def get_attendance_status(course_id, total_classes):
    conn = sqlite3.connect("attendance.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT student_id, SUM(CASE WHEN present = 0 THEN 1 ELSE 0 END) as absences
        FROM attendance
        WHERE course_id = ?
        GROUP BY student_id
    """, (course_id,))
    results = cursor.fetchall()
    conn.close()
    status = {student_id: absences for student_id, absences in results}
    for student_id in status:
        status[student_id] = (status[student_id] / total_classes) * 100 if total_classes > 0 else 0
    return status

def get_course_by_id(course_id, data):
    for projeto in data.get("projetos_ativos", []):
        if projeto.get("nome_projeto") == "Estação Tech":
            for turma in projeto.get("turmas", []):
                if turma.get("id") == course_id:
                    return turma
    return None

def exibir_status_turma(course_id, turma, alunos):
    """Exibe o status de faltas após a chamada."""
    total_classes = 0
    if "datas_aula" in turma:
        total_classes = len(turma["datas_aula"])
    elif "aulas" in turma:
        total_classes = len(turma["aulas"])
    if total_classes == 0:
        st.info("Não há datas definidas para este curso, não foi possível calcular status.")
        return

    status = get_attendance_status(course_id, total_classes)
    st.subheader("Status da Turma (Percentual de Faltas)")
    table_data = []
    for aluno in alunos:
        student_id = aluno.get("id")
        faltas = status.get(student_id, 0)
        table_data.append({
            "Aluno": aluno.get("nome", "N/D"),
            "Percentual de Faltas": f"{faltas:.1f}%"
        })
    st.table(table_data)
    st.info("Concluído.")

# ------------------ VIEWS ------------------
def professor_home():
    """
    Tela inicial para o professor com dois botões, com emojis, tamanho aumentado:
    1) Agenda
    2) Visualizar Turma
    """
    st.markdown(
        """
        <style>
        /* Aumenta o tamanho dos botões e permite emojis em linhas diferentes */
        div.stButton > button {
            height: 100px;
            width: 220px;
            font-size: 20px;
            white-space: pre-line;
        }
        div.stButton {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Área do Professor")
    st.write(f"Bem-vindo, {st.session_state.teacher_name}!")
    st.write("Selecione a funcionalidade desejada:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅\nAgenda"):
            st.session_state.view = "agenda"
    with col2:
        if st.button("👨‍🏫\nVisualizar Turma"):
            st.session_state.view = "visualizar"

def agenda_view():
    """Exibe o calendário (agenda) e, se houver aulas hoje, um botão para chamada."""
    st.subheader("Agenda de Aulas")
    components.html(show_calendar(), height=600)

    # Verifica se há aulas hoje e exibe botão de chamada
    courses_today = check_class_today()
    if courses_today:
        st.success("Você tem aula(s) agendada(s) para hoje!")
        st.write("Selecione um curso para realizar a chamada:")
        for turma in courses_today:
            curso_nome = turma.get("nome_curso", "N/D")
            turma_id = turma.get("id")
            if st.button(f"Realizar Chamada para '{curso_nome}'", key=f"btn_chamada_{turma_id}"):
                st.session_state.selected_course_id = turma_id
                st.session_state.view = "chamada"
    else:
        st.info("Não há aulas agendadas para hoje.")

    # Botão Voltar
    if st.button("Voltar ao Menu Principal"):
        st.session_state.view = "professor_home"

def chamada_view():
    """Tela de chamada de presença."""
    st.subheader("Registro de Presença")
    course_id = st.session_state.get("selected_course_id")
    if not course_id:
        st.warning("Nenhum curso selecionado para chamada.")
        if st.button("Voltar ao Menu Principal"):
            st.session_state.view = "professor_home"
        return

    data = load_data(JSON_PATH)
    turma = get_course_by_id(course_id, data)
    if turma is None:
        st.error("Curso não encontrado.")
        if st.button("Voltar ao Menu Principal"):
            st.session_state.view = "professor_home"
        return
    
    st.write(f"Chamada - {turma.get('nome_curso', 'N/D')}")
    alunos = turma.get("alunos", [])
    if not alunos:
        st.info("Nenhum aluno cadastrado nesse curso.")
        if st.button("Voltar ao Menu Principal"):
            st.session_state.view = "professor_home"
        return

    # Ordena alunos
    alunos = sorted(alunos, key=lambda a: a.get("nome", "").lower())
    st.write("Marque se o aluno está presente:")

    with st.form("chamada_form"):
        attendance = {}
        for aluno in alunos:
            presente = st.checkbox(aluno.get("nome", "N/D"), value=True, key=f"aluno_{aluno.get('id')}")
            attendance[aluno.get("id")] = presente
        submitted = st.form_submit_button("OK")

    if submitted:
        today_str = datetime.date.today().isoformat()
        if existing_attendance_today(course_id, today_str):
            st.warning("Já existe chamada registrada para hoje. Deseja sobrescrever a chamada anterior?")
            colA, colB = st.columns(2)
            with colA:
                if st.button("Sim, sobrescrever"):
                    remove_attendance_today(course_id, today_str)
                    insert_attendance(course_id, [(sid, val) for sid, val in attendance.items()], today_str)
                    st.success("Chamada sobrescrita com sucesso!")
                    exibir_status_turma(course_id, turma, alunos)
            with colB:
                if st.button("Não registrar"):
                    st.warning("Chamada não foi registrada nem sobrescrita.")
        else:
            # Não existe registro anterior
            insert_attendance(course_id, [(sid, val) for sid, val in attendance.items()], today_str)
            st.success("Chamada registrada com sucesso!")
            exibir_status_turma(course_id, turma, alunos)

    # Botão Voltar
    if st.button("Voltar ao Menu Principal"):
        st.session_state.view = "professor_home"

def visualizar_turma_view():
    """
    Exibe as turmas do professor, mostrando os alunos e a frequência deles.
    Corrige o problema quando 'aluno' é somente um int, sem campos .get().
    """
    import streamlit as st
    import sqlite3
    from scripts.utils import load_data
    from datetime import date

    st.subheader("Visualizar Turma")
    
    data = load_data(JSON_PATH)
    if data is None:
        st.error("Erro ao carregar dados.")
        return

    teacher_id = st.session_state.get("teacher_id")
    # Filtra apenas as turmas do professor logado
    professor_turmas = []
    for projeto in data.get("projetos_ativos", []):
        if projeto.get("nome_projeto") == "Estação Tech":
            professor_turmas = [
                t for t in projeto.get("turmas", [])
                if t.get("professor_id") == teacher_id
            ]
            break

    if not professor_turmas:
        st.info("Você não ministra nenhuma turma no momento.")
        if st.button("Voltar ao Menu Principal"):
            st.session_state.view = "professor_home"
        return

    conn = sqlite3.connect("attendance.db", check_same_thread=False)

    for turma in professor_turmas:
        st.markdown(f"### Turma: {turma.get('nome_curso', 'N/D')}")
        alunos_na_turma = turma.get("alunos", [])
        if not alunos_na_turma:
            st.write("Nenhum aluno cadastrado nessa turma.")
            st.markdown("---")
            continue

        # Calcula total de aulas
        total_classes = 0
        if "datas_aula" in turma:
            total_classes = len(turma["datas_aula"])
        elif "aulas" in turma:
            total_classes = len(turma["aulas"])

        st.write(f"Total de Aulas Definidas: {total_classes}")

        # Consulta as ausências no DB
        cursor = conn.cursor()
        results = cursor.execute("""
            SELECT student_id, SUM(CASE WHEN present = 0 THEN 1 ELSE 0 END)
            FROM attendance
            WHERE course_id = ?
            GROUP BY student_id
        """, (turma["id"],)).fetchall()

        # Monta um dicionario {student_id: faltas}
        faltas_por_aluno = {r[0]: r[1] for r in results}

        table_data = []
        # Precisamos lidar com a possibilidade de 'aluno' ser um int ou um dict
        # Se for dict, extraímos nome; se for int, exibimos 'Aluno ID'
        def sort_key(a):
            if isinstance(a, dict):
                return a.get("nome", "").lower()
            return str(a).lower()

        # Ordena considerando que pode ter ints ou dicts
        alunos_ordenados = sorted(alunos_na_turma, key=sort_key)

        for aluno in alunos_ordenados:
            if isinstance(aluno, dict):
                sid = aluno.get("id")
                nome = aluno.get("nome", "N/D")
            else:
                # Caso seja apenas um int
                sid = aluno
                nome = f"Aluno ID: {aluno}"

            faltas = faltas_por_aluno.get(sid, 0)
            freq_percent = 0.0
            if total_classes > 0:
                freq_percent = 100.0 * (1.0 - (faltas / total_classes))
            table_data.append({
                "Aluno": nome,
                "Frequência (%)": f"{freq_percent:.1f}%"
            })

        st.table(table_data)
        st.markdown("---")

    conn.close()

    if st.button("Voltar ao Menu Principal"):
        st.session_state.view = "professor_home"

# ------------------ MAIN APP ------------------
def main():
    init_db()

    # Se o professor não estiver logado, exibe a tela de login
    if "logged_in_teacher" not in st.session_state or not st.session_state.logged_in_teacher:
        teacher_login()
        return

    # Controle de view
    if "view" not in st.session_state:
        st.session_state.view = "professor_home"

    if st.session_state.view == "professor_home":
        professor_home()
    elif st.session_state.view == "agenda":
        agenda_view()
    elif st.session_state.view == "chamada":
        chamada_view()
    elif st.session_state.view == "visualizar":
        visualizar_turma_view()

    # Botão de logout global
    if st.button("Logout"):
        st.session_state.logged_in_teacher = False
        st.session_state.teacher_name = ""
        st.session_state.teacher_id = None
        st.session_state.view = "professor_home"
        st.experimental_rerun()

if __name__ == "__main__":
    main()
