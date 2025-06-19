import sqlite3

def criar_conexao():
    return sqlite3.connect('estoque.db')

def criar_tabela_equipamentos():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equipamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            tipo TEXT,
            marca TEXT,
            modelo TEXT,
            data_aquisicao TEXT,
            status TEXT,
            funcionario_id INTEGER,
            FOREIGN KEY(funcionario_id) REFERENCES Funcionarios(id)
        ) 
    """)
    conexao.commit()
    conexao.close()
    
def criar_tabela_funcionarios():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            departamento TEXT,
            email TEXT
        ) 
    """)
    conexao.commit()
    conexao.close()
    
def criar_tabela_historico():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipamento_id INTEGER,
            funcionario_id INTEGER,
            data TEXT,
            acao TEXT,
            observacao TEXT,
            FOREIGN KEY(equipamento_id) REFERENCES Equipamentos(id),
            FOREIGN KEY(funcionario_id) REFERENCES Funcionarios(id)

        ) 
    """)
    conexao.commit()
    conexao.close()
    
def criar_tabela_user():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuários (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            senha TEXT,
            tipo_acesso TEXT,
        ) 
    """)

def iniciar_db():
    criar_tabela_funcionarios()
    criar_tabela_equipamentos()
    criar_tabela_historico()
    