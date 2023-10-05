from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route('/')
def hello_calculadora():
    return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        if nome == "123" and senha == "123":
            return render_template("index.html")
        else:
            return "<h1>Senha ou Login inválidos</h1>"
        
conexao = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'Joao2209',
                database = 'nota_lp',
                auth_plugin='mysql_native_password'
                )
cursor = conexao.cursor()

@app.route('/calculadora', methods=["POST", "GET"])
def calcular_nota():
    if request.method == "POST":
        try:
            nome = request.form.get("nome")
            dre = request.form.get('dre')
            nota_t1 = float(request.form.get('nota_t1'))
            nota_t2 = float(request.form.get('nota_t2'))
            numero_de_tarefas = float(request.form.get('numero_de_tarefas'))
            notas_tarefas = float(request.form.get('notas_tarefas'))

            if nota_t1 >= 0 and nota_t2 >= 0 and numero_de_tarefas >= 0 and notas_tarefas >= 0:
                nota_final = (nota_t1 + nota_t2) * 0.8 + (notas_tarefas / numero_de_tarefas) * 0.2
                
                nome_aluno = nome
                dre_ = dre
                nota = nota_final
                comando = f'INSERT INTO alunos (nome,dre,nota) VALUES ("{nome_aluno}",{dre},{nota})'
               
                cursor.execute(comando)
                conexao.commit()
                #cursor.close()
                
                if nota_final >= 7.0:
                    return "<h1>APROVADO</h1>"
                elif nota_final >= 3.0:
                    return "<h1>PROVA FINAL</h1>"
                elif nota_final > 10:
                    return "<h1>DADOS INVÁLIDOS</h1>"
                else:
                    return "<h1>REPROVADO</h1>"
        except ValueError:
            return "<h1>DADOS INVÁLIDOS</h1>"
         
    return "Erro"

#conexao.close()

comando_2 = f'SELECT * FROM alunos'
cursor.execute(comando_2)
resultado = cursor.fetchall()
print (resultado)

if __name__ == "__main__":
    app.run(debug=True)
