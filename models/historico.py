class Historico:
    def __init__(self, id, equipamento_id, data, acao, observacao=None):
        self.id = id
        self.equipamento_id = equipamento_id
        self.data = data
        self.acao = acao  # Exemplo: "Emprestado", "Devolvido", "Manutenção"
        self.observacao = observacao

    def __str__(self):
        return f"[{self.data}] {self.acao} (Equipamento ID: {self.equipamento_id})"