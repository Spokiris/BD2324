import requests
import json
from datetime import datetime, timedelta

# URL base da API
BASE_URL = 'http://localhost:5000'

def test_ping():
    response = requests.get(f'{BASE_URL}/ping')
    print('Test Ping:', response.status_code, response.json())

def test_listar_clinicas():
    response = requests.get(f'{BASE_URL}/')
    print('Listar Clínicas:', response.status_code, response.json())

def test_listar_especialidades(clinica):
    response = requests.get(f'{BASE_URL}/c/{clinica}/')
    print(f'Listar Especialidades de {clinica}:', response.status_code, response.json())

def test_listar_medicos(clinica, especialidade):
    response = requests.get(f'{BASE_URL}/c/{clinica}/{especialidade}/')
    print(f'Listar Médicos de {especialidade} em {clinica}:', response.status_code, response.json())

def test_registar_marcacao(clinica, paciente_nif, medico, data_hora, codigo_sns):
    data = {
        'paciente_nif': paciente_nif,
        'medico': medico,
        'data_hora': data_hora.isoformat(),
        'codigo_sns': codigo_sns
    }
    response = requests.post(f'{BASE_URL}/a/{clinica}/registar/', json=data)
    print(f'Registrar Marcação em {clinica}:', response.status_code, response.json())

def test_cancelar_marcacao(clinica, paciente_nif, medico, data_hora):
    data = {
        'paciente_nif': paciente_nif,
        'medico': medico,
        'data_hora': data_hora.isoformat()
    }
    response = requests.post(f'{BASE_URL}/a/{clinica}/cancelar/', json=data)
    print(f'Cancelar Marcação em {clinica}:', response.status_code, response.json())

if __name__ == "__main__":
    test_ping()
    test_listar_clinicas()


