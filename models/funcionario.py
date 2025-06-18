class Funcionario:
    def __init__(self, id, nome, departamento, email):
        self.id = id
        self.nome = nome
        self.departamento = departamento
        self.email = email
        
    def __str__(self):
        return f"[{self.id}] {self.nome} - {self.departamento}"
        