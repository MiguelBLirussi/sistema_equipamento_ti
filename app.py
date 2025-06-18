from db import iniciar_db
from db import criar_conexao
from models.equipamento import Equipamento
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    conexao = criar_conexao()
    equipamentos = Equipamento.listar(conexao)
    conexao.close()
    return render_template("index.html", equipamentos=equipamentos)

@app.route("/inserir", methods=["GET","POST"])
def inserir():
    if request.method == "POST":
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        data_aquisicao = request.form["data_aquisicao"]
        status = request.form["status"]
        funcionario_id = request.form.get("funcionario_id") or None
        if funcionario_id: funcionario_id = int(funcionario_id)
        
        conexao = criar_conexao()
        Equipamento.inserir(conexao, nome, tipo, marca, modelo, data_aquisicao, status, funcionario_id)
        conexao.close()
        return redirect(url_for("index"))
    return render_template("inserir.html")

@app.route("/atualizar", methods=["GET","POST"])
def atualizar():
    if request.method == "POST":
        campo = request.form["campo"].lower()
        equipamento_id = request.form["equipamento_id"]
        novo_valor = request.form["novo_valor"]
        
        nomes_campos = {
        "Nome": "nome",
        "Tipo": "tipo",
        "Marca": "marca",
        "Modelo": "modelo",
        "Data de Aquisição": "data_aquisicao",
        "Status": "status",
        "funcionario_id": "funcionario_id"
        }

        campo_bruto = request.form["campo"]
        campo = nomes_campos.get(campo_bruto)
        if campo is None:
            return render_template("atualizar.html", erro="Campo inválido.")
        
        try:
            equipamento_id = int(equipamento_id)
        except ValueError:
            return render_template("atualizar.html", erro="O ID deve ser um número inteiro.")

        conexao = criar_conexao()
        Equipamento.atualizar(conexao,equipamento_id,campo,novo_valor)
        conexao.close()
        return redirect(url_for("index"))
    return render_template("atualizar.html")
        
if __name__ == "__main__":
    app.run(debug=True)
    

# def inserir_equipamento():
#     conexao = criar_conexao()
#     nome = input("Qual o nome do equipamento: ")
#     tipo = input("Qual o tipo de equipamento: ")
#     marca = input("Qual a marca do equipamento: ")
#     modelo = input(f"Informe o modelo do {tipo}: ")
#     data_aquisicao = input("Quando o equipamento foi adquirido: ")
#     status = input ("Informe o status do equipamento: ")
#     funcionario_id = input("Informe o ID do funcionário responsável (ou deixe em branco): ")
#     funcionario_id = int(funcionario_id) if funcionario_id.strip() else None
#     Equipamento.inserir(conexao, nome, tipo, marca, modelo, data_aquisicao, status, funcionario_id)
    
# def listar_equipamentos():
#     conexao = criar_conexao()
#     equipamentos = Equipamento.listar(conexao)
#     for eq in equipamentos:
#         print(eq)
    
# def atualizar_equipamento():
#     conexao = criar_conexao()
#     cursor = conexao.cursor()
#     campo = input("Qual campo deseja alterar: ")
#     equipamento_id = input("Qual o ID do equipamento: ")
#     equipamento = cursor.execute("SELECT * FROM Equipamentos WHERE id = ?", (equipamento_id,)).fetchone()
#     print(f"O campo:({campo}) deste equipamento será alterado: {equipamento}")
#     novo_valor = input(f"Qual será o novo {campo}: ")
#     Equipamento.atualizar(conexao, equipamento_id, campo, novo_valor)
    
# iniciar_db()
# listar_equipamentos()
# atualizar_equipamento()



