# git remote -v
# git pull origin master(ou main)
# clonar o projeto --> git clone https://caminho.do.projeto
# instalar extensão python
# abrir terminal e verificar se abre (.venv), caso nao abra --> ctrl + shift + p
# digitar enviroment e criar um ambiente virtual

# pip install flask
# pip install Flask-SQLAlchemy
# pip install Flask-Migrate
# pip install Flask-Script
# pip install pymysql
# flask db init
# flask db migrate -m "Migração Inicial"
# executo quando nao tenho o arquivo python na pasta versions ^
# flask db upgrate
# executo quando minhas tabelas nao estao criadas no banco de dados ^
# flask run --debug

# subir pro github
# rm -Rf .git
# git remote -v
# git init
# git remote add origin https://github.com/juliaaurea/flask_juliaaurea.git
# git add .
# git config user.name 'juliaaurea'
# git config user.email 'juliaaurea.rezende@gmail.com'
# git commit -m 'aula aula'
# git push origin master

from flask import Flask, render_template, request, flash, redirect
from database import db
from flask_migrate import Migrate
from models import Consultas
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SNF37Y7dzbfbhFDSBFdzfhKEUdhdf'

# drive://usuario:senha@servidor/banco_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/Consultas"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dados', methods=['POST'])
def dados():
    flash('Dados Enviados!!!')
    dados = request.form
    return render_template('dados.html', dados=dados)

@app.route('/consultas')
def consultas():
    c = Consultas.query.all()
    return render_template('consultas_lista.html', dados=c)

@app.route('/consultas/add')
def consultas_add():
    return render_template('consultas_add.html')

@app.route('/consultas/save', methods=['POST'])
def consultas_save():
    paciente = request.form.get('paciente')
    data_consulta = request.form.get('data_consulta')
    medico = request.form.get('medico')
    if paciente and data_consulta and medico:
        consultas = Consultas(paciente, data_consulta, medico)
        db.session.add(consultas)
        db.session.commit()
        flash('Consulta marcada com sucesso!')
        return redirect('/consultas')
    else:
        flash('Preencha todos os campos!')
        return redirect('/consultas/add')
    
@app.route('/consultas/remove/<int:id_consultas>')
def consultas_remove(id_consultas):
    consultas = Consultas.query.get(id_consultas)
    if id_consultas:
        db.session.delete(consultas)
        db.session.commit()
        flash('Consulta cancelada com sucesso')
        return redirect('/consultas')
    else:
        flash('Caminho incorreto')
        return redirect('/consultas')
    
@app.route('/consultas/edita/<int:id_consultas>')
def consultas_edita(id_consultas):
    consultas = Consultas.query.get(id_consultas)
    return render_template('consultas_edita.html', dados=consultas)

@app.route('/consultas/editasave', methods=["POST"])
def consultas_editasave():
    id_consultas = request.form.get('id_consultas')
    paciente = request.form.get('paciente')
    data_consulta = request.form.get('data_consulta')
    medico = request.form.get('medico')
    if id_consultas and paciente and data_consulta and medico:
        consultas = Consultas.query.get(id_consultas)
        consultas.paciente = paciente
        consultas.data_consulta = data_consulta
        consultas.medico = medico
        db.session.commit()
        flash("Dados atualizados com sucesso!")
        return redirect("/consultas")
    else:
        flash("Dados incompletos")
        return redirect("/consultas")


if __name__ == '__main__':
    app.run()