from db import iniciar_db
from db import criar_conexao
from models.equipamento import Equipamento
from models.user import Usuario
from models.funcionario import Funcionario
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "chave_segura"

#ROTAS RELACIONADAS AO LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.autenticar(email, senha)

        if usuario:
            session["usuario_id"] = usuario.id
            session["tipo_acesso"] = usuario.tipo_acesso
            return redirect(url_for("index"))  # Redireciona após login bem-sucedido
        
        return render_template("login.html", erro="Email ou senha inválidos.")  # Exibe erro na tela

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario_id", None)  
    session.pop("tipo_acesso", None)  
    return redirect(url_for("login"))  

@app.context_processor
def adicionar_usuario_logado():
    return {"usuario_logado": "usuario_id" in session}

#ROTAS RELACIONADAS A USUÁRIOS
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    # Verifica se o usuário está logado e é admin
    if "usuario_id" not in session or session["tipo_acesso"] != "admin":
        return render_template("erro.html", erro="Acesso negado! Apenas administradores podem cadastrar usuários.")

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        tipo_acesso = request.form["tipo_acesso"]  # Ex: 'admin', 'gerente', 'operador'

        senha_hash = Usuario.gerar_hash(senha)

        conexao = criar_conexao()
        cursor = conexao.cursor()
        

        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, tipo_acesso) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, tipo_acesso)
            )
            conexao.commit()
            return redirect(url_for("index"))  # Redireciona após cadastro
        except Exception as e:
            return render_template("cadastrar.html", erro="Erro ao cadastrar usuário.")

        finally:
            conexao.close()

    return render_template("cadastrar.html")

#ROTAS RELACIONADAS A FUNCIONÁRIOS
@app.route("/funcionario")
def funcionario():
    conexao = criar_conexao()
    funcionarios = Funcionario.listar(conexao)
    conexao.close()
    return render_template("funcionario.html", funcionarios=funcionarios)

@app.route("/excluir_funcionario", methods=["GET","POST"])
def excluir_funcionario():
    if request.method == "POST":
        funcionario_id = request.form.get("funcionario_id")
        conexao = criar_conexao()
        Funcionario.excluir(conexao, funcionario_id)
        conexao.close()
        return redirect(url_for("funcionario"))
    return render_template("excluir_funcionario.html")

@app.route("/cadastrar_funcionario", methods=["GET", "POST"])
def cadastrar_funcionario():
    if "usuario_id" not in session or session["tipo_acesso"] == "operador":
        return render_template("erro.html", erro="Apenas administradores ou gerentes podem cadastrar funcionários.")

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        departamento = request.form["departamento"]

        conexao = criar_conexao()
        try:
            Funcionario.inserir(conexao, nome, departamento, email)
            return redirect(url_for("index"))
        except Exception as e:
            print(f"[ERRO] Falha ao cadastrar funcionário: {e}")
            return render_template("cadastrar_funcionario.html", erro="Erro ao cadastrar funcionário.")
        finally:
            conexao.close()

    return render_template("cadastrar_funcionario.html")

#ROTAS RELACIONADAS AOS EQUIPAMENTOS E PAGINA INICIAL
@app.route("/")
def index():
    usuario_logado = "usuario_id" in session
    conexao = criar_conexao()
    equipamentos = Equipamento.listar(conexao)
    conexao.close()
    return render_template("index.html", equipamentos=equipamentos, usuario_logado=usuario_logado)

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