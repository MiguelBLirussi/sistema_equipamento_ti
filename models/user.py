import bcrypt
from db import criar_conexao

class Usuario:
    def __init__(self, id, nome, email, senha, tipo_acesso):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha  # Senha armazenada em hash
        self.tipo_acesso = tipo_acesso

    @staticmethod
    def gerar_hash(senha):
        """ Gera um hash seguro para a senha """
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
        return senha_hash

    @staticmethod
    def autenticar(email, senha):
        """ Autentica o usuário verificando o email e senha """
        conexao = criar_conexao()
        cursor = conexao.cursor()

        usuario = cursor.execute(
            "SELECT id, nome, email, senha, tipo_acesso FROM Usuários WHERE email = ?",
            (email,)
        ).fetchone()
        conexao.close()

        if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario[3]):  # senha está na posição 3
            return Usuario(*usuario)  # Agora todos os campos estão na ordem certa
        
        return None
    
    @staticmethod
    def listar(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Usuários")
        resultados = cursor.fetchall()
        usuarios = []
        for row in resultados:
            usuario = Usuario(*row)
            usuarios.append(usuario)
        return usuarios
    
