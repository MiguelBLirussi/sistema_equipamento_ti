from db import iniciar_db
from db import criar_conexao
from models.equipamento import Equipamento
from models.user import Usuario
from models.funcionario import Funcionario
from flask import Flask, render_template, request, redirect, url_for, session
import logging

app = Flask(__name__)

app.secret_key = "chave_segura"

#ROTAS RELACIONADAS AO LOGIN
@app.route("/", methods=["GET", "POST"])
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
def adicionar_contexto_global():
    nome_user = None
    if "usuario_id" in session:
        conexao = criar_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM Usuários WHERE id = ?", (session["usuario_id"],))
        resultado = cursor.fetchone()
        if resultado:
            nome_user = resultado[0]
        conexao.close()

    return {
        "usuario_logado": "usuario_id" in session,
        "nome_user": nome_user
    }

#ROTAS RELACIONADAS A USUÁRIOS
@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    # Verifica se o usuário está logado e é admin
    if "usuario_id" not in session or session["tipo_acesso"] != "admin":
        return render_template("erro.html", erro="Acesso negado! Apenas administradores podem cadastrar usuários.")

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]
        tipo_acesso = request.form["tipo_acesso"]
        
        if senha != confirmar_senha:
            return render_template("cadastrar.usuario.html", erro="As senhas não coincidem!")
        elif senha == confirmar_senha:
            senha_hash = Usuario.gerar_hash(senha)

        conexao = criar_conexao()
        cursor = conexao.cursor()
        

        try:
            cursor.execute(
                "INSERT INTO Usuários (nome, email, senha, tipo_acesso) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, tipo_acesso)
            )
            conexao.commit()
            return redirect(url_for("index"))
        except Exception as e:
            return render_template("usuario.html", erro="Erro ao cadastrar usuário.")

        finally:
            conexao.close()

    return render_template("cadastrar_usuario.html")

@app.route("/usuario")
def usuario():
    conexao = criar_conexao()
    usuarios = Usuario.listar(conexao)
    conexao.close()
    return render_template("usuario.html", usuarios=usuarios)

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
@app.route("/home")
def index():
    usuario_logado = "usuario_id" in session
    conexao = criar_conexao()
    equipamentos = Equipamento.listar(conexao)
    conexao.close()
    return render_template("index.html", equipamentos=equipamentos, usuario_logado=usuario_logado)

@app.route("/buscar",methods=["GET","POST"])
def buscar():
    conexao = criar_conexao()
    if request.method == "POST":
        nome_busca = request.form["nome_busca"]
        equipamentos = Equipamento.buscar(conexao,nome_busca)
        conexao.close()
        return render_template("buscar.html", equipamentos=equipamentos)
    conexao.close()
    return render_template("buscar.html", equipamentos=None)

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
        conexao = criar_conexao()
        Equipamento.atualizar(conexao,equipamento_id,campo,novo_valor)
        conexao.close()
        return redirect(url_for("index"))
    return render_template("atualizar.html")
        
if __name__ == "__main__":
    logging.debug("recebendo dados")
    app.run(debug=True)