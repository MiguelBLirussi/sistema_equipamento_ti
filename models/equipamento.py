from datetime import datetime

class Equipamento:
    def __init__(self, id, nome, tipo, marca, modelo, data_aquisicao, status, funcionario_id=None):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.data_aquisicao = data_aquisicao
        self.status = status
        self.funcionario_id = funcionario_id

    def __str__(self):
        return f"[{self.id}] {self.nome} ({self.tipo}) - {self.marca}/{self.modelo}"
    
    @staticmethod
    def inserir(conexao, nome, tipo, marca, modelo, data_aquisicao, status, funcionario_id=None):
        cursor = conexao.cursor()

        if funcionario_id is not None:
            cursor.execute("""
                INSERT INTO Equipamentos (nome, tipo, marca, modelo, data_aquisicao, status, funcionario_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, tipo, marca, modelo, data_aquisicao, status, funcionario_id))
        else:
            cursor.execute("""
                INSERT INTO Equipamentos (nome, tipo, marca, modelo, data_aquisicao, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, tipo, marca, modelo, data_aquisicao, status))
        conexao.commit()
        
    @staticmethod
    def listar(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Equipamentos")
        resultados = cursor.fetchall()
        equipamentos = []
        for row in resultados:
            data_aquisicao = datetime.strptime(row[5], '%Y-%m-%d').strftime('%d/%m/%Y')
            equipamento = Equipamento(row[0],row[1],row[2],row[3],row[4],data_aquisicao,row[6],row[7]) 
            equipamentos.append(equipamento)
        return equipamentos
    
    @staticmethod
    def atualizar(conexao, equipamento_id, campo, novo_valor):
        campos_permitidos = ["nome", "tipo", "marca", "modelo", "data_aquisicao", "status", "funcionario_id"]
        if campo.lower() not in campos_permitidos:
            print("Campo inválido.")
            return

        cursor = conexao.cursor()
        query = f"UPDATE Equipamentos SET {campo} = ? WHERE id = ?"
        cursor.execute(query, (novo_valor, equipamento_id))
        conexao.commit()

    @staticmethod
    def buscar(conexao, nome_busca):
        equipamentos = []
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Equipamentos WHERE nome LIKE ?", (f"%{nome_busca}%",))
        resultados = cursor.fetchall()
        for row in resultados:
            data_aquisicao = datetime.strptime(row[5], '%Y-%m-%d').strftime('%d/%m/%Y')
            equipamento = Equipamento(row[0],row[1],row[2],row[3],row[4],data_aquisicao,row[6],row[7]) 
            equipamentos.append(equipamento)
        return equipamentos
