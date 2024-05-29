#!/usr/bin/python3
import os
from logging.config import dictConfig
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuração de logs
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.config.from_prefixed_env()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'postgresql+psycopg://postgres:postgres@postgres/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
log = app.logger

# Modelos baseados no esquema fornecido
class Clinica(db.Model):
    __tablename__ = 'clinica'
    nome = db.Column(db.String(80), primary_key=True)
    telefone = db.Column(db.String(15), unique=True, nullable=False)
    morada = db.Column(db.String(255), unique=True, nullable=False)

class Medico(db.Model):
    __tablename__ = 'medico'
    nif = db.Column(db.String(9), primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    morada = db.Column(db.String(255), nullable=False)
    especialidade = db.Column(db.String(80), nullable=False)

class Trabalha(db.Model):
    __tablename__ = 'trabalha'
    nif = db.Column(db.String(9), db.ForeignKey('medico.nif'), primary_key=True)
    nome = db.Column(db.String(80), db.ForeignKey('clinica.nome'), primary_key=True)
    dia_da_semana = db.Column(db.SmallInteger)

class Paciente(db.Model):
    __tablename__ = 'paciente'
    ssn = db.Column(db.String(11), primary_key=True)
    nif = db.Column(db.String(9), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    morada = db.Column(db.String(255), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False)

class Consulta(db.Model):
    __tablename__ = 'consulta'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssn = db.Column(db.String(11), db.ForeignKey('paciente.ssn'), nullable=False)
    nif = db.Column(db.String(9), db.ForeignKey('medico.nif'), nullable=False)
    nome = db.Column(db.String(80), db.ForeignKey('clinica.nome'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    codigo_sns = db.Column(db.String(12), unique=True)

class Receita(db.Model):
    __tablename__ = 'receita'
    codigo_sns = db.Column(db.String(12), db.ForeignKey('consulta.codigo_sns'), primary_key=True)
    medicamento = db.Column(db.String(155), primary_key=True)
    quantidade = db.Column(db.SmallInteger, nullable=False)

class Observacao(db.Model):
    __tablename__ = 'observacao'
    id = db.Column(db.Integer, db.ForeignKey('consulta.id'), primary_key=True)
    parametro = db.Column(db.String(155), primary_key=True)
    valor = db.Column(db.Float)

# Endpoints
@app.route('/ping', methods=['GET'])
def ping():
    log.debug("ping!")
    return jsonify({"message": "ZARA!"}), 200

@app.route('/')
def listar_clinicas():
    clinicas = Clinica.query.all()
    return jsonify([{'nome': clinica.nome, 'telefone': clinica.telefone, 'morada': clinica.morada} for clinica in clinicas])

@app.route('/c/<clinica>/', methods=['GET'])
def listar_especialidades(clinica):
    clinica_obj = Clinica.query.filter_by(nome=clinica).first_or_404()
    medicos = Medico.query.join(Trabalha, Trabalha.nif == Medico.nif).filter(Trabalha.nome == clinica).all()
    especialidades = list(set([medico.especialidade for medico in medicos]))
    return jsonify(especialidades)

@app.route('/c/<clinica>/<especialidade>/', methods=['GET'])
def listar_medicos(clinica, especialidade):
    clinica_obj = Clinica.query.filter_by(nome=clinica).first_or_404()
    medicos = Medico.query.filter_by(especialidade=especialidade).join(Trabalha, Trabalha.nif == Medico.nif).filter(Trabalha.nome == clinica).all()
    resultado = []
    for medico in medicos:
        consultas = Consulta.query.filter_by(nif=medico.nif).order_by(Consulta.data, Consulta.hora).limit(3).all()
        horarios = [{'data': consulta.data.isoformat(), 'hora': consulta.hora.isoformat()} for consulta in consultas]
        resultado.append({'nome': medico.nome, 'horarios': horarios})
    return jsonify(resultado)

@app.route('/a/<clinica>/registar/', methods=['POST'])
def registar_marcacao(clinica):
    data = request.json
    clinica_obj = Clinica.query.filter_by(nome=clinica).first_or_404()
    medico = Medico.query.filter_by(nome=data['medico']).join(Trabalha, Trabalha.nif == Medico.nif).filter(Trabalha.nome == clinica).first_or_404()
    paciente = Paciente.query.filter_by(nif=data['paciente_nif']).first_or_404()
    data_hora = datetime.fromisoformat(data['data_hora'])
    
    if data_hora <= datetime.now():
        return jsonify({'error': 'Data e hora devem ser no futuro.'}), 400

    nova_consulta = Consulta(ssn=paciente.ssn, nif=medico.nif, nome=clinica, data=data_hora.date(), hora=data_hora.time(), codigo_sns=data.get('codigo_sns'))
    db.session.add(nova_consulta)
    db.session.commit()
    return jsonify({'message': 'Marcação registrada com sucesso.'})

@app.route('/a/<clinica>/cancelar/', methods=['POST'])
def cancelar_marcacao(clinica):
    data = request.json
    clinica_obj = Clinica.query.filter_by(nome=clinica).first_or_404()
    medico = Medico.query.filter_by(nome=data['medico']).join(Trabalha, Trabalha.nif == Medico.nif).filter(Trabalha.nome == clinica).first_or_404()
    data_hora = datetime.fromisoformat(data['data_hora'])
    
    marcacao = Consulta.query.filter_by(ssn=data['paciente_nif'], nif=medico.nif, data=data_hora.date(), hora=data_hora.time()).first_or_404()
    
    if marcacao.data <= datetime.now().date() and marcacao.hora <= datetime.now().time():
        return jsonify({'error': 'Não é possível cancelar uma marcação passada.'}), 400
    
    db.session.delete(marcacao)
    db.session.commit()
    return jsonify({'message': 'Marcação cancelada com sucesso.'})

if __name__ == "__main__":
    app.run()

