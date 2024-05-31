from flask import Flask, request, jsonify
from datetime import datetime
from psycopg import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from collections import defaultdict

app = Flask(__name__)

# Criando a engine de conexão com o banco de dados
engine = create_engine('postgresql://ist1105865:cuth8107@db.tecnico.ulisboa.pt/ist1105865')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Definindo as classes das tabelas do banco de dados
class Consulta(Base):
    __tablename__ = 'consulta'
    id = Column(Integer, primary_key=True, server_default=text("nextval('consulta_id_seq')"))
    ssn = Column(String(11), ForeignKey('paciente.ssn'), nullable=False)
    nif = Column(String(9), ForeignKey('medico.nif'), nullable=False)
    nome = Column(String(80), ForeignKey('clinica.nome'), nullable=False)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    codigo_sns = Column(String(12), unique=True)

    paciente = relationship("Paciente", back_populates="consulta")
    medico = relationship("Medico", back_populates="consultas")
    clinica = relationship("Clinica", back_populates="consultas")

class Clinica(Base):
    __tablename__ = 'clinica'
    nome = Column(String(80), primary_key=True)
    telefone = Column(String(15), unique=True, nullable=False)
    morada = Column(String(255), unique=True, nullable=False)

    trabalha = relationship("Trabalha", back_populates="clinica")
    consultas = relationship("Consulta", back_populates="clinica")

class Medico(Base):
    __tablename__ = 'medico'
    nif = Column(String(9), primary_key=True)
    nome = Column(String(80), unique=True, nullable=False)
    telefone = Column(String(15), nullable=False)
    morada = Column(String(255), nullable=False)
    especialidade = Column(String(80), nullable=False)

    trabalha = relationship("Trabalha", back_populates="medico")
    consultas = relationship("Consulta", back_populates="medico")

class Trabalha(Base):
    __tablename__ = 'trabalha'

    nif = Column(String(9), ForeignKey('medico.nif'), primary_key=True)
    nome = Column(String(80), ForeignKey('clinica.nome'), primary_key=True)
    dia_da_semana = Column(Integer, nullable=False)

    medico = relationship("Medico", back_populates="trabalha")
    clinica = relationship("Clinica", back_populates="trabalha")

class Paciente(Base):
    __tablename__ = 'paciente'
    ssn = Column(String(11), primary_key=True)
    nif = Column(String(9), unique=True, nullable=False)
    nome = Column(String(80), nullable=False)
    telefone = Column(String(15), nullable=False)
    morada = Column(String(255), nullable=False)
    data_nasc = Column(Date, nullable=False)

    consulta = relationship("Consulta", back_populates="paciente")


# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)

# Endpoint para listar todas as clínicas
@app.route('/', methods=['GET'])
def list_clinics():
    session = Session()
    clinics = session.query(Clinica).all()
    clinic_list = [{'nome': clinic.nome, 'telefone': clinic.telefone, 'morada': clinic.morada} for clinic in clinics]
    session.close()
    return jsonify({'clinics': clinic_list})

# Endpoint para listar todas as especialidades oferecidas em uma clínica específica
@app.route('/c/<clinica>/', methods=['GET'])
def list_specialties(clinica):
    session = Session()
    result = session.query(Medico.especialidade).join(Trabalha).filter(Trabalha.nome == clinica).distinct().all()
    specialties = [row[0] for row in result]  # Extrair apenas o primeiro elemento de cada tupla
    session.close()
    return jsonify({'specialties': specialties})

# Endpoint para listar todos os médicos e seus primeiros três horários disponíveis para uma especialidade em uma clínica específica
@app.route('/c/<clinica>/<especialidade>/', methods=['GET'])
def list_doctors(clinica, especialidade):
    session = Session()
    
    # Consultar os médicos que trabalham na clínica e têm a especialidade especificada
    doctors = session.query(Medico).join(Trabalha).filter(Trabalha.nome == clinica, Medico.especialidade == especialidade).all()
    
    appointments = defaultdict(list)  # Usando defaultdict para evitar a necessidade de verificar se a chave existe
    
    # Para cada médico, recuperar as primeiras 3 consultas
    for doctor in doctors:
        appointment_3 = session.query(Consulta).filter(Consulta.nome == clinica, Consulta.nif == doctor.nif).order_by(Consulta.data, Consulta.hora).limit(3).all()
        appointment_3 = [(consulta.data.strftime("%Y-%m-%d"), consulta.hora.strftime("%H:%M:%S")) for consulta in appointment_3]  # Convertendo para formato de data e hora
        appointments[doctor.nome] = appointment_3
    
    session.close()
    return jsonify({'doctors': list(appointments.keys()), 'appointments': dict(appointments)})

@app.route('/a/<clinica>/registar/', methods=['POST'])
def register_appointment(clinica):
    data = request.json
    paciente = data['paciente']
    medico = data['medico']
    data_hora = datetime.strptime(data['data_hora'], "%Y-%m-%d %H:%M:%S")
    session = Session()

    try:
        nova_consulta = Consulta(ssn=paciente['ssn'], nif=medico['nif'], nome=clinica, data=data_hora.date(), hora=data_hora.time())
        session.add(nova_consulta)
        session.commit()
        consulta_id = nova_consulta.id  # Obter o ID da nova consulta
        print("Consulta ID: ", consulta_id)    
        session.close()
        return jsonify({"message": "Marcação registrada com sucesso", "consulta_id": consulta_id})
    except IntegrityError as e:
        session.rollback()
        session.close()
        return jsonify({"error": str(e)}), 400  # Retornar o erro como parte da resposta JSON com o código de status 400


# Endpoint para cancelar uma marcação de consulta
@app.route('/a/<clinica>/cancelar/', methods=['POST'])
def cancel_appointment(clinica):
    data = request.json
    consulta_id = data['consulta_id']  # Aqui você recebe o índice da consulta a ser cancelada
    session = Session()
    consulta = session.query(Consulta).filter_by(id=consulta_id).first()
    if consulta:
        session.delete(consulta)
        session.commit()
        session.close()
        return jsonify({"message": "Marcação cancelada com sucesso"})
    else:
        session.close()
        return jsonify({"message": "Marcação não encontrada"}), 404
if __name__ == '__main__':
    app.run(debug=True)


