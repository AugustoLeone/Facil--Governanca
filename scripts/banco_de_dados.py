import streamlit as st
import psycopg2
import pandas as pd

#função que estabelece conexão com o db
def conexao_db ():
    return psycopg2.connect(
        dbname = "fac1l-governanca",
        user="postgres",
        password="Yasmin23@",
        host="localhost",
        port="5432"
    )

#--------------------------------------------------------Criar Tabelas--------------------------------------------------------------------

#cria a tabela de estoque:
def criar_tabela_estoque():

    conn = conexao_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estoque (
        id SERIAL PRIMARY KEY,
        item VARCHAR(100),
        categoria VARCHAR(30),
        tipo VARCHAR(30),
        quantidade INTEGER,
        preco_compra INTEGER
    )""")
    
    conn.commit()
    cursor.close()
    conn.close()

#criar tabela de funcionarios
def create_tb_funcionarios():

    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios(
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) NOT NULL,
            senha VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            cpf VARCHAR(100) UNIQUE NOT NULL,
            cargo VARCHAR(30) NOT NULL,
            salario NUMERIC(10,2)
        )
        """)

    except SyntaxError as e:
        st.error(f'Erro na criação da tabela: {e}')

    conn.commit()
    cursor.close()
    conn.close()

#criar tabela de receitas e despesas
def criar_db_receitas_despesas ():
    
    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                    
            CREATE TABLE IF NOT EXISTS controle_receita_despesa (
                id SERIAL PRIMARY KEY,
                data DATE NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                descricao TEXT,
                tipo VARCHAR(10) CHECK(tipo IN ('receita', 'despesa')) NOT NULL,
                valor NUMERIC(10,2) NOT NULL
            )"""
        )

    except SyntaxError as e:
        st.error(f'Erro na criação da tabela: {e}')
    
    conn.commit()
    cursor.close()
    conn.close()

#criar tabela de dividas
def criar_db_dividas ():
    
    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                    
            CREATE TABLE IF NOT EXISTS dividas (
                id SERIAL PRIMARY KEY,
                data_compra DATE NOT NULL,
                data_pagamento DATE NOT NULL,
                forma_pagamento VARCHAR(20) CHECK(forma_pagamento IN ('a vista', 'parcelado')) NOT NULL,
                n_parcelas NUMERIC(3),
                categoria VARCHAR(100) NOT NULL,
                descricao TEXT,
                valor NUMERIC(10,2) NOT NULL
                    
            )"""
        )

    except SyntaxError as e:
        st.error(f'Erro na criação da tabela: {e}')
    
    conn.commit()
    cursor.close()
    conn.close()

#criar tabela de orçamentos
def criar_db_orcamento ():
    
    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""       
            CREATE TABLE IF NOT EXISTS orcamentos (
                id SERIAL PRIMARY KEY,
                data_inicio DATE NOT NULL,
                data_termino_previsto DATE NOT NULL,
                atraso_dias NUMERIC(6),
                descricao TEXT,
                valor_orcado NUMERIC(10,2) NOT NULL,
                valor_gasto NUMERIC(10,2)
            )""")

    except SyntaxError as e:
        st.error(f'Erro na criação da tabela: {e}')
    
    conn.commit()
    cursor.close()
    conn.close()

#criar tabela de professores
def criar_tabela_professores():
    conexao = conexao_db()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professores (
            id_professor SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            telefone VARCHAR(20),
            especialidade VARCHAR(100)
        );
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()
    
#criar tabela de alunos
def criar_tabela_alunos():
    conexao = conexao_db()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id_aluno SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            data_nascimento DATE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            telefone VARCHAR(20),
            data_matricula DATE NOT NULL,
            data_conclusao DATE,
            status VARCHAR(20) CHECK (status IN ('ativo', 'concluido', 'desistente')) NOT NULL,
            curso_id INT NOT NULL,
            FOREIGN KEY (curso_id) REFERENCES cursos(id_curso)
        );
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

#criar tabela de cursos
def criar_tabela_cursos():
    conexao = conexao_db()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id_curso SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE,
            carga_horaria INT NOT NULL,
            professor_id INT NOT NULL,
            FOREIGN KEY (professor_id) REFERENCES professores(id_professor)
        );
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

#criar tabela de matriculas
def criar_tabela_matriculas():
    conexao = conexao_db()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matriculas (
            id_matricula SERIAL PRIMARY KEY,
            aluno_id INT NOT NULL,
            curso_id INT NOT NULL,
            professor_id INT NOT NULL,
            data_inicio DATE NOT NULL,
            data_conclusao DATE,
            status VARCHAR(20) CHECK (status IN ('ativo', 'concluido', 'desistente')) NOT NULL,
            FOREIGN KEY (aluno_id) REFERENCES alunos(id_aluno),
            FOREIGN KEY (curso_id) REFERENCES cursos(id_curso),
            FOREIGN KEY (professor_id) REFERENCES professores(id_professor)
        );
    ''')
    conexao.commit()
    cursor.close()
    conexao.close()

#--------------------------------------------------------CRUD Estoque--------------------------------------------------------------------

#função de cadastro de item no estoque
def cadastrar_item(item, categoria, tipo, quantidade, preco_compra):

    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO estoque (item, categoria, tipo, quantidade, preco_compra)
        VALUES (%s,%s,%s,%s,%s)""", (item,categoria,tipo,quantidade,preco_compra))
        
        conn.commit()
        cursor.close()
        conn.close()

        st.success(f'Item {item} cadastrado com sucesso')

    except SyntaxError as e:
        st.error(f'Erro ao cadastrar item: {e}')

#pega a quantidade do item selecionado no estoque
def quantidade_estoque(item, categoria):

    conn = conexao_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT quantidade FROM estoque
    WHERE item = %s AND categoria = %s 
    """, (item, categoria))
    result = cursor.fetchone()
    return result[0] if result else 0


#função de adição da quantidade de itens no estoque
def adicionar_item(item, categoria, tipo, quantidade):

    conn = conexao_db()
    cursor = conn.cursor()

    try:
        quantidade_somada = quantidade_estoque(item, categoria) + quantidade

        cursor.execute("""
        UPDATE estoque SET quantidade = %s 
        WHERE item = %s AND categoria = %s AND tipo = %s""", (quantidade_somada, item,categoria,tipo))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f'Item {item} adicionado com sucesso')

    except SyntaxError as e:
        st.error(f'Erro ao adicionar item: {e}')

#função de subtração de itens no estoque
def retirar_item(item, categoria, tipo, quantidade):

    conn = conexao_db()
    cursor = conn.cursor()

    try:
        quantidade_subtraida = quantidade_estoque(item, categoria) - quantidade
        
        cursor.execute("""
        UPDATE estoque SET quantidade = %s 
        WHERE item = %s AND categoria = %s AND tipo = %s""", (quantidade_subtraida,item,categoria,tipo))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f'Item {item} retirado com sucesso')

    except SyntaxError as e:
        st.error(f'Erro ao retirar item: {e}')

#função de exclusao de item no estoque
def excluir_item (item, categoria, tipo):

    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        DELETE FROM estoque
        WHERE item = %s AND categoria = %s AND tipo = %s""",
        (item, categoria, tipo))

        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f'Item {item} excluido com sucesso')

    except SyntaxError as e:
        st.error(f'Erro ao excluir item: {e}')

#--------------------db Funcionarios-----------------------------

#função de cadastro do funcionario
def cadastrar_funcionario_db(nome,usuario,senha_criptografada,email_confirmado,cpf_confirmado,cargo,salario):

    conn = conexao_db()
    cursor = conn.cursor()
     
    try:
        cursor.execute("""
        INSERT INTO funcionarios (nome, usuario, senha, email, cpf, cargo, salario)
        VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (nome, usuario, senha_criptografada, email_confirmado, cpf_confirmado, cargo, salario)
        )
    
        st.success(f'Cadastro do funcionario: {nome} realizado com sucesso!')

    except SyntaxError as e:
        st.error(f'Erro {e} ao cadastrar funcioanrio {nome}')
    
    conn.commit()
    cursor.close()
    conn.close()

#função de modificação dos cmapos do funcionario
def modificar_funcionario_db(nome,usuario,senha_criptografada,email_confirmado,cpf_confirmado,cargo,salario):

    conn = conexao_db()
    cursor = conn.cursor()
     
    try:
        cursor.execute("""
        UPDATE funcionarios SET nome = %s, usuario = %s, senha = %s, cargo = %s, salario = %s
        WHERE email = %s AND cpf = %s""",
        (nome, usuario, senha_criptografada, cargo, salario, email_confirmado, cpf_confirmado))

    except SyntaxError as e:
        st.error(f'Erro {e} ao modificar funcioanrio {nome}')

    conn.commit()
    cursor.close()
    conn.close()

#função que exclui o funcionario
def excluir_funcionario_db(nome,email,cpf,cargo):
    conn = conexao_db()
    cursor = conn.cursor()
     
    try:
        cursor.execute("""
        DELETE FROM funcionarios
        WHERE nome = %s AND email = %s AND cpf = %s AND cargo = %s""",
        (nome, email, cpf, cargo))
    
        st.success(f'Exclusão do funcionario: {nome} realizada com sucesso!')

    except SyntaxError as e:
        st.error(f'Erro {e} ao excluir funcioanrio {nome}')

    conn.commit()
    cursor.close()
    conn.close()

#função que puxa a tabela funcionarios do db
def listar_funcionario():

    conn = conexao_db()
     
    try:
        df = pd.read_sql("SELECT * FROM funcionarios", conn)
    
        st.success(f'Listagem de funcionarios realizada com sucesso!')

    except SyntaxError as e:
        st.error(f'Erro ao listar funcionarios: {e}')
    
    conn.close()
    
    return df

#--------------------------------------------------financeiro----------------------------------------------------------------------------

#função de inserção de dados no db de control de receita e despesas
def inserir_db_receita_despesa(data, categoria, descricao, tipo, valor):

    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        
        INSERT INTO controle_receita_despesa (data, categoria, descricao, tipo, valor)
        VALUES (%s, %s, %s, %s, %s)""",
        (data, categoria, descricao, tipo, valor)
        )

    except SyntaxError as e:
        st.error(f'Erro na inserção dos dados: {e}')

    conn.commit()
    cursor.close()
    conn.close()

#função para buscar os dados da db de controle de receitas e despesas
def buscar_db_receitas_despesas():
    conn = conexao_db()
    if conn is None:
        return pd.DataFrame()

    try:
        df_receitas_despesas = pd.read_sql(
            "SELECT data, categoria, descricao, tipo, valor FROM controle_receita_despesa ORDER BY data DESC",
            conn
        )
        return df_receitas_despesas
    except Exception as e:
        st.error(f'Erro na busca dos dados da db: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

#função de exclusão dos cmapos do controle_receita_despesa
def excluir_db_receitas_despesas(data, categoria, tipo, valor):
    conn = conexao_db()
    cursor = conn.cursor()
    sucesso = False  # Variável para indicar se a exclusão ocorreu

    try:
        cursor.execute("""
        DELETE FROM controle_receita_despesa  
        WHERE data = %s AND categoria = %s AND tipo = %s AND valor = %s""",
        (data, categoria, tipo, valor))
        
        if cursor.rowcount > 0:  # Verifica se algum registro foi deletado
            sucesso = True
            st.success('Exclusão de transação realizada com sucesso!')
        else:
            st.warning('Nenhuma transação encontrada para excluir.')

    except Exception as e:
        st.error(f'Erro ao excluir transação: {e}')

    conn.commit()
    cursor.close()
    conn.close()
    
    return sucesso  # Retorna se a exclusão foi bem-sucedida

#--------------------------------------------------Scripts Dividas----------------------------------------------------------

#função de inserção de dados na db dividas
def inserir_db_dividas(data_compra, data_pagamento, forma_pagamento, n_parcelas, categoria, descricao, valor):

    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        
        INSERT INTO dividas (data_compra, data_pagamento, forma_pagamento, n_parcelas, categoria, descricao, valor)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (data_compra, data_pagamento, forma_pagamento, n_parcelas, categoria, descricao, valor)
        )

    except SyntaxError as e:
        st.error(f'Erro na inserção dos dados: {e}')

    conn.commit()
    cursor.close()
    conn.close()

#função de exclusao de dados da tabela dividas
def excluir_db_dividas(data_compra, forma_pagamento, n_parcelas, categoria, valor):

    conn = conexao_db()
    cursor = conn.cursor()
    sucesso = False  # Variável para indicar se a exclusão ocorreu

    try:
        cursor.execute("""
        DELETE FROM dividas  
        WHERE data_compra = %s AND forma_pagamento = %s AND n_parcelas = %s AND categoria = %s AND valor = %s""",
        (data_compra, forma_pagamento, n_parcelas, categoria, valor))
        
        if cursor.rowcount > 0:  # Verifica se algum registro foi deletado
            sucesso = True
            st.success('Exclusão de divida realizada com sucesso!')
        else:
            st.warning('Nenhuma divida encontrada para excluir.')

    except Exception as e:
        st.error(f'Erro ao excluir divida: {e}')

    conn.commit()
    cursor.close()
    conn.close()
    
    return sucesso  # Retorna se a exclusão foi bem-sucedida

#função de busca da db dividas
def buscar_db_dividas():

    conn = conexao_db()
    cursor= conn.cursor()

    try:
        df_dividas = pd.read_sql(
            "SELECT data_compra, data_pagamento, forma_pagamento, n_parcelas, categoria, descricao, valor FROM dividas ORDER BY data_compra DESC",
            conn
        )
        return df_dividas
    except Exception as e:
        st.error(f'Erro na busca dos dados da db: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

#--------------------------------------------------Scripts orcamento----------------------------------------------------------

#função para inserir dados na tabela orçamento
def inserir_db_orcamento(data_inicio, data_termino_previsto, atraso_dias, descricao, valor_orcado, valor_gasto):

    conn = conexao_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        
        INSERT INTO orcamentos (data_inicio, data_termino_previsto, atraso_dias, descricao, valor_orcado, valor_gasto)
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (data_inicio, data_termino_previsto, atraso_dias, descricao, valor_orcado, valor_gasto))

    except SyntaxError as e:
        st.error(f'Erro na inserção dos dados: {e}')

    conn.commit()
    cursor.close()
    conn.close()

#função de exclusão no database de orçãmentos
def excluir_db_orcamento(data_inicio, data_termino_previsto, decricao, valor_orcado):

    conn = conexao_db()
    cursor = conn.cursor()
    sucesso = False  # Variável para indicar se a exclusão ocorreu

    try:
        cursor.execute("""
        DELETE FROM orcamentos  
        WHERE data_inicio=%s AND data_termino_previsto=%s AND decricao=%s AND valor_orcado=%s """,
        (data_inicio, data_termino_previsto, decricao, valor_orcado))
        
        if cursor.rowcount > 0:  # Verifica se algum registro foi deletado
            sucesso = True
            st.success('Exclusão de orcamento realizada com sucesso!')
        else:
            st.warning('Nenhum orcamento encontrada para excluir.')

    except Exception as e:
        st.error(f'Erro ao excluir orcamento: {e}')

    conn.commit()
    cursor.close()
    conn.close()
    
    return sucesso  # Retorna se a exclusão foi bem-sucedida

#função de busca dentro da tabela orçamentos
def buscar_db_orcamento():

    conn = conexao_db()
    cursor= conn.cursor()

    try:
        df_orcamentos = pd.read_sql(
            "SELECT data_inicio, data_termino_previsto, atraso_dias, descricao, valor_orcado, valor_gasto FROM orcamentos ORDER BY data_inicio DESC",
            conn
        )
        return df_orcamentos
    except Exception as e:
        st.error(f'Erro na busca dos dados da db: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

