# scripts/agendamentos.py
import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
import uuid

def initialize_sched_db():
    """Inicializa o banco de dados para agendamentos, criando a tabela se não existir."""
    conn = sqlite3.connect("web.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS compromissos(
            compromisso_id TEXT PRIMARY KEY,
            name TEXT,
            tipo TEXT,
            date DATE,
            horario TEXT,
            descricao TEXT,
            carg_participacao TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao carregar este módulo
initialize_sched_db()

# Conexão persistente para o app de agendamentos
conn_sched = sqlite3.connect("web.db", check_same_thread=False)
c_sched = conn_sched.cursor()

def calc_id_s(tipo, reunioes, vistorias, fiscalizacoes):
    """Gera um ID para o compromisso com base no tipo utilizando UUID para garantir unicidade."""
    if tipo == 'Reunião':
        prefix = '1.00'
    elif tipo == 'Vistoria':
        prefix = '2.00'
    elif tipo == 'Fiscalização':
        prefix = '3.00'
    else:
        st.error("Tipo de compromisso inválido!")
        st.stop()
    return prefix + str(uuid.uuid4().hex[:6])

def insercao_de_compromissos_s():
    """Formulário para inserir um novo compromisso (agendamento)."""
    with st.form("form_insercao_agendamento", clear_on_submit=True):
        compromisso = st.text_input('Qual o compromisso que deseja inserir')
        tipo = st.selectbox('Tipo de compromisso', ("Reunião", "Vistoria", "Fiscalização"))
        data = st.date_input('Data')
        horario = st.time_input('Horário do compromisso')
        descricao = st.text_input('Descrição do compromisso')
        carg_participacao = st.text_input('Cargo/Participação')
        
        submit = st.form_submit_button("Inserir evento")
        if submit:
            data_str = data.isoformat()
            horario_str = horario.strftime('%H:%M:%S')
            reunioes = len(list(c_sched.execute("SELECT * FROM compromissos WHERE tipo = 'Reunião'")))
            vistorias = len(list(c_sched.execute("SELECT * FROM compromissos WHERE tipo = 'Vistoria'")))
            fiscalizacoes = len(list(c_sched.execute("SELECT * FROM compromissos WHERE tipo = 'Fiscalização'")))
            id_value = calc_id_s(tipo, reunioes, vistorias, fiscalizacoes)
            
            c_sched.execute('''
                INSERT INTO compromissos (compromisso_id, name, tipo, date, horario, descricao, carg_participacao, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (id_value, compromisso, tipo, data_str, horario_str, descricao, carg_participacao, 'ativo'))
            conn_sched.commit()
            st.success('Inserção realizada com sucesso!')

def exclusao_de_compromissos_s():
    """Formulário para excluir um compromisso selecionado."""
    query_all = "SELECT compromisso_id, name, date, horario FROM compromissos ORDER BY date ASC, horario ASC"
    df_all = pd.read_sql(query_all, con=conn_sched)
    
    if df_all.empty:
        st.info("Não há eventos para excluir.")
        return

    event_options = {}
    for _, row in df_all.iterrows():
        event_options[row['compromisso_id']] = f"{row['name']} - {row['date']} {row['horario']}"
    
    with st.form("form_exclusao_agendamento", clear_on_submit=True):
        selected_event = st.selectbox("Selecione o evento a excluir", 
                                      options=list(event_options.keys()), 
                                      format_func=lambda x: event_options[x])
        confirm = st.checkbox("Confirmo a exclusão do evento selecionado.")
        submit = st.form_submit_button("Excluir evento")
        
        if submit:
            if confirm:
                c_sched.execute("DELETE FROM compromissos WHERE compromisso_id = ?", (selected_event,))
                conn_sched.commit()
                st.success("Exclusão realizada com sucesso.")
            else:
                st.warning("Por favor, confirme a exclusão marcando a caixa de confirmação.")

def exibir_evento(evento, now, referencia):
    """Exibe os detalhes de um compromisso com uma progress bar indicando o tempo restante."""
    try:
        meeting_date = datetime.strptime(evento['date'], '%Y-%m-%d').date()
    except Exception:
        meeting_date = date.today()
    try:
        meeting_time = datetime.strptime(evento['horario'], '%H:%M:%S').time()
    except Exception:
        meeting_time = time(0, 0, 0)
    meeting_datetime = datetime.combine(meeting_date, meeting_time)
    
    remaining_seconds = (meeting_datetime - now).total_seconds() if meeting_datetime > now else 0
    total_duration = (meeting_datetime - referencia).total_seconds() if meeting_datetime > referencia else 1
    progress_percentage = int(100 * remaining_seconds / total_duration) if total_duration > 0 else 0
    
    st.write(f"**Compromisso:** {evento['name']}  |  **Data:** {evento['date']}  |  **Horário:** {evento['horario']}")
    st.write(f"**Descrição:** {evento.get('descricao', '')}")
    st.write(f"**Cargo/Participação:** {evento.get('carg_participacao', '')}")
    if meeting_datetime > now:
        st.progress(progress_percentage)
        st.write(f"**Falta:** {str(timedelta(seconds=int(remaining_seconds)))} para o evento")
    else:
        st.write("**Evento já ocorreu.**")
    st.markdown("---")

def remover_eventos_passados():
    """
    Remove da base de dados os compromissos que já passaram.
    Um compromisso é considerado passado se a data for anterior a hoje
    ou se for hoje mas o horário já passou.
    """
    now = datetime.now()
    query_all = "SELECT compromisso_id, date, horario FROM compromissos"
    df_all = pd.read_sql(query_all, con=conn_sched)
    for _, row in df_all.iterrows():
        try:
            event_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            event_time = datetime.strptime(row['horario'], '%H:%M:%S').time()
            event_datetime = datetime.combine(event_date, event_time)
        except Exception:
            continue
        if event_datetime < now:
            c_sched.execute("DELETE FROM compromissos WHERE compromisso_id = ?", (row['compromisso_id'],))
            conn_sched.commit()

def agendamentos_app():
    """Interface do app de agendamentos."""
    # Remove compromissos que já passaram antes de exibir os eventos
    remover_eventos_passados()
    
    st.header("Agendamentos")
    now = datetime.now()
    dia_atual = date.today()
    dia_atual_str = dia_atual.isoformat()
    
    with st.expander("Inserir evento"):
        insercao_de_compromissos_s()
    with st.expander("Excluir evento"):
        exclusao_de_compromissos_s()
    
    st.subheader("Compromissos de hoje")
    query_hoje = "SELECT * FROM compromissos WHERE date = ? ORDER BY horario ASC"
    df_hoje = pd.read_sql(query_hoje, con=conn_sched, params=(dia_atual_str,), index_col='compromisso_id')
    start_of_day = datetime.combine(dia_atual, time(0, 0, 0))
    if not df_hoje.empty:
        for idx, row in df_hoje.iterrows():
            exibir_evento(row, now, start_of_day)
    else:
        st.info("Nenhum compromisso para hoje.")
    
    st.subheader("Compromissos futuros")
    query_futuro = "SELECT * FROM compromissos WHERE date > ? ORDER BY date ASC, horario ASC"
    df_futuro = pd.read_sql(query_futuro, con=conn_sched, params=(dia_atual_str,), index_col='compromisso_id')
    if df_futuro.empty:
        st.info("Não há compromissos futuros marcados.")
    else:
        remaining_times = []
        for idx, row in df_futuro.iterrows():
            try:
                meeting_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            except Exception:
                meeting_date = date.today()
            try:
                meeting_time = datetime.strptime(row['horario'], '%H:%M:%S').time()
            except Exception:
                meeting_time = time(0, 0, 0)
            meeting_datetime = datetime.combine(meeting_date, meeting_time)
            remaining = (meeting_datetime - now).total_seconds()
            remaining_times.append(remaining if remaining > 0 else 0)
        for idx, row in df_futuro.iterrows():
            exibir_evento(row, now, now)
# scripts/agendamentos.py

# ... (código existente permanece inalterado)

from datetime import datetime, date, time, timedelta
import sqlite3
import streamlit as st
import pandas as pd
import uuid

# Função nova para alertar sobre eventos programados que acontecerão em breve
def alertar_eventos_programados(threshold_minutes=5):
    """
    Verifica os eventos agendados que ocorrerão em breve (dentro do tempo especificado em minutos) 
    e alerta o usuário.
    """
    now = datetime.now()
    threshold = timedelta(minutes=threshold_minutes)
    
    query_all = "SELECT compromisso_id, name, date, horario FROM compromissos WHERE status = 'ativo'"
    df_all = pd.read_sql(query_all, con=conn_sched)
    
    for _, row in df_all.iterrows():
        try:
            event_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
            event_time = datetime.strptime(row['horario'], '%H:%M:%S').time()
            event_datetime = datetime.combine(event_date, event_time)
        except Exception:
            continue
        
        if now <= event_datetime <= now + threshold:
            minutes_left = int((event_datetime - now).total_seconds() // 60)
            st.warning(f"Alerta: O evento '{row['name']}' começará em aproximadamente {minutes_left} minutos!")

# Atualização da função agendamentos_app para chamar alertar_eventos_programados
def agendamentos_app():
    """Interface do app de agendamentos."""
    # Remove compromissos que já passaram
    remover_eventos_passados()
    
    # Alerta sobre eventos que ocorrerão em breve
    alertar_eventos_programados(threshold_minutes=5)
    
    st.header("Agendamentos")
    now = datetime.now()
    dia_atual = date.today()
    dia_atual_str = dia_atual.isoformat()
    
    with st.expander("Inserir evento"):
        insercao_de_compromissos_s()
    with st.expander("Excluir evento"):
        exclusao_de_compromissos_s()
    
    st.subheader("Compromissos de hoje")
    query_hoje = "SELECT * FROM compromissos WHERE date = ? ORDER BY horario ASC"
    df_hoje = pd.read_sql(query_hoje, con=conn_sched, params=(dia_atual_str,), index_col='compromisso_id')
    start_of_day = datetime.combine(dia_atual, time(0, 0, 0))
    if not df_hoje.empty:
        for idx, row in df_hoje.iterrows():
            exibir_evento(row, now, start_of_day)
    else:
        st.info("Nenhum compromisso para hoje.")
    
    st.subheader("Compromissos futuros")
    query_futuro = "SELECT * FROM compromissos WHERE date > ? ORDER BY date ASC, horario ASC"
    df_futuro = pd.read_sql(query_futuro, con=conn_sched, params=(dia_atual_str,), index_col='compromisso_id')
    if df_futuro.empty:
        st.info("Não há compromissos futuros marcados.")
    else:
        for idx, row in df_futuro.iterrows():
            exibir_evento(row, now, now)
