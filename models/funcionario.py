class Funcionario:
    def __init__(self, id, nome, departamento, email):
        self.id = id
        self.nome = nome
        self.departamento = departamento
        self.email = email
        
    def __str__(self):
        return f"[{self.id}] {self.nome} - {self.departamento}"
    
    @staticmethod
    def inserir(conexao, nome, departamento, email):
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO Funcionarios (nome, departamento, email)
            VALUES (?, ?, ?)
        """, (nome, departamento, email))
        conexao.commit()

    @staticmethod
    def atualizar(conexao, funcionario_id, campo, novo_valor):
        cursor = conexao.cursor()
        query = f"UPDATE Equipamentos SET {campo} = ? WHERE id = ?"
        cursor.execute(query, (novo_valor, funcionario_id))
        conexao.commit()
        
    @staticmethod
    def listar(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Funcionarios")
        resultados = cursor.fetchall()
        equipamentos = []
        for row in resultados:
            equipamento = Funcionario(*row)
            equipamentos.append(equipamento)
        return equipamentos
    
    @staticmethod
    def excluir(conexao, funcionario_id):
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Funcionarios WHERE id = ?", (funcionario_id,))
        conexao.commit()