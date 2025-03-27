{
  "tabelas": [
    {
      "nome": "estoque",
      "campos": [
        {"id": "SERIAL PRIMARY KEY"},
        {"item": "VARCHAR(100)"},
        {"categoria": "VARCHAR(30)"},
        {"tipo": "VARCHAR(30)"},
        {"quantidade": "INTEGER"},
        {"preco_compra": "INTEGER"}
      ]
    },
    {
      "nome": "funcionarios",
      "campos": [
        {"id": "SERIAL PRIMARY KEY"},
        {"nome": "VARCHAR(100) NOT NULL"},
        {"usuario": "VARCHAR(100) NOT NULL"},
        {"senha": "VARCHAR(255) NOT NULL"},
        {"email": "VARCHAR(100) UNIQUE NOT NULL"},
        {"cpf": "VARCHAR(100) UNIQUE NOT NULL"},
        {"cargo": "VARCHAR(30) NOT NULL"},
        {"salario": "NUMERIC(10,2)"}
      ]
    },
    {
      "nome": "controle_receita_despesa",
      "campos": [
        {"id": "SERIAL PRIMARY KEY"},
        {"data": "DATE NOT NULL"},
        {"categoria": "VARCHAR(100) NOT NULL"},
        {"descricao": "TEXT"},
        {"tipo": "VARCHAR(10) CHECK(tipo IN ('receita', 'despesa')) NOT NULL"},
        {"valor": "NUMERIC(10,2) NOT NULL"}
      ],
      "dados": [
        {"data": "2025-03-01", "categoria": "Mensalidade", "descricao": "Pagamento mensal de aluno", "tipo": "receita", "valor": 500.00},
        {"data": "2025-03-05", "categoria": "Salário", "descricao": "Pagamento de professor", "tipo": "despesa", "valor": 3000.00}
      ]
    },
    {
      "nome": "dividas",
      "campos": [
        {"id": "SERIAL PRIMARY KEY"},
        {"data_compra": "DATE NOT NULL"},
        {"data_pagamento": "DATE NOT NULL"},
        {"forma_pagamento": "VARCHAR(20) CHECK(forma_pagamento IN ('a vista', 'parcelado')) NOT NULL"},
        {"n_parcelas": "NUMERIC(3)"},
        {"categoria": "VARCHAR(100) NOT NULL"},
        {"descricao": "TEXT"},
        {"valor": "NUMERIC(10,2) NOT NULL"}
      ]
    },
    {
      "nome": "orcamentos",
      "campos": [
        {"id": "SERIAL PRIMARY KEY"},
        {"data_inicio": "DATE NOT NULL"},
        {"data_termino_previsto": "DATE NOT NULL"},
        {"atraso_dias": "NUMERIC(6)"},
        {"descricao": "TEXT"},
        {"valor_orcado": "NUMERIC(10,2) NOT NULL"},
        {"valor_gasto": "NUMERIC(10,2)"}
      ]
    },
    {
      "nome": "professores",
      "campos": [
        {"id_professor": "SERIAL PRIMARY KEY"},
        {"nome": "VARCHAR(100) NOT NULL"},
        {"email": "VARCHAR(100) UNIQUE NOT NULL"},
        {"telefone": "VARCHAR(20)"},
        {"especialidade": "VARCHAR(100)"}
      ]
    },
    {
      "nome": "alunos",
      "campos": [
        {"id_aluno": "SERIAL PRIMARY KEY"},
        {"nome": "VARCHAR(100) NOT NULL"},
        {"data_nascimento": "DATE NOT NULL"},
        {"email": "VARCHAR(100) UNIQUE NOT NULL"},
        {"telefone": "VARCHAR(20)"},
        {"data_matricula": "DATE NOT NULL"},
        {"data_conclusao": "DATE"},
        {"status": "VARCHAR(20) CHECK (status IN ('ativo', 'concluido', 'desistente')) NOT NULL"},
        {"curso_id": "INT NOT NULL"}
      ]
    },
    {
      "nome": "cursos",
      "campos": [
        {"id_curso": "SERIAL PRIMARY KEY"},
        {"nome": "VARCHAR(100) NOT NULL UNIQUE"},
        {"carga_horaria": "INT NOT NULL"},
        {"professor_id": "INT NOT NULL"}
      ]
    },
    {
      "nome": "matriculas",
      "campos": [
        {"id_matricula": "SERIAL PRIMARY KEY"},
        {"aluno_id": "INT NOT NULL"},
        {"curso_id": "INT NOT NULL"},
        {"professor_id": "INT NOT NULL"},
        {"data_inicio": "DATE NOT NULL"},
        {"data_conclusao": "DATE"},
        {"status": "VARCHAR(20) CHECK (status IN ('ativo', 'concluido', 'desistente')) NOT NULL"}
      ]
    }
  ],
  "funcoes": [
    {
      "nome": "cadastrar_item",
      "entrada": ["item", "categoria", "tipo", "quantidade", "preco_compra"],
      "descricao": "Cadastra um item no estoque."
    },
    {
      "nome": "quantidade_estoque",
      "entrada": ["item", "categoria"],
      "descricao": "Retorna a quantidade disponível de um item específico no estoque."
    },
    {
      "nome": "adicionar_item",
      "entrada": ["item", "categoria", "tipo", "quantidade"],
      "descricao": "Adiciona uma quantidade de itens ao estoque."
    },
    {
      "nome": "retirar_item",
      "entrada": ["item", "categoria", "tipo", "quantidade"],
      "descricao": "Retira uma quantidade de itens do estoque."
    },
    {
      "nome": "excluir_item",
      "entrada": ["item", "categoria", "tipo"],
      "descricao": "Exclui um item do estoque."
    },
    {
      "nome": "cadastrar_funcionario_db",
      "entrada": ["nome", "usuario", "senha_criptografada", "email_confirmado", "cpf_confirmado", "cargo", "salario"],
      "descricao": "Cadastra um funcionário no banco de dados."
    },
    {
      "nome": "modificar_funcionario_db",
      "entrada": ["nome", "usuario", "senha_criptografada", "email_confirmado", "cpf_confirmado", "cargo", "salario"],
      "descricao": "Modifica as informações de um funcionário."
    },
    {
      "nome": "excluir_funcionario_db",
      "entrada": ["nome", "email", "cpf", "cargo"],
      "descricao": "Exclui um funcionário do banco de dados."
    },
    {
      "nome": "listar_funcionario",
      "entrada": [],
      "descricao": "Lista todos os funcionários cadastrados."
    },
    {
      "nome": "inserir_db_receita_despesa",
      "entrada": ["data", "categoria", "descricao", "tipo", "valor"],
      "descricao": "Insere uma receita ou despesa no controle financeiro."
    },
    {
      "nome": "buscar_db_receitas_despesas",
      "entrada": [],
      "descricao": "Busca as transações de receitas e despesas."
    },
    {
      "nome": "excluir_db_receitas_despesas",
      "entrada": ["data", "categoria", "tipo", "valor"],
      "descricao": "Exclui uma transação de receita ou despesa."
    },
    {
      "nome": "inserir_db_dividas",
      "entrada": ["data_compra", "data_pagamento", "forma_pagamento", "n_parcelas", "categoria", "descricao", "valor"],
      "descricao": "Insere uma dívida no banco de dados."
    },
    {
      "nome": "excluir_db_dividas",
      "entrada": ["data_compra", "forma_pagamento", "n_parcelas", "categoria", "valor"],
      "descricao": "Exclui uma dívida do banco de dados."
    },
    {
      "nome": "buscar_db_dividas",
      "entrada": [],
      "descricao": "Busca as dívidas cadastradas."
    },
    {
      "nome": "inserir_db_orcamento",
      "entrada": ["data_inicio", "data_termino_previsto", "atraso_dias", "descricao", "valor_orcado", "valor_gasto"],
      "descricao": "Insere um orçamento no banco de dados."
    },
    {
      "nome": "excluir_db_orcamento",
      "entrada": ["data_inicio", "data_termino_previsto", "decricao", "valor_orcado"],
      "descricao": "Exclui um orçamento do banco de dados."
    },
    {
      "nome": "buscar_db_orcamento",
      "entrada": [],
      "descricao": "Busca os orçamentos cadastrados."
    }
  ]
}
