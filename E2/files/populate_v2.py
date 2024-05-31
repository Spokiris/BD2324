import random
import datetime
import os
import faker

MEDICINE = [['Adderall'], ['Amitriptilina'], ['Amlodipina'], ['Amoxicilina'], ['Ativan'], ['Atorvastatina'], ['Azitromicina'], ['Benzonatato'], ['Botox'], ['Brilinta'], ['Bunavail'], ['Buprenorfina'], ['Cefalexina'], ['Ciprofloxacina'], ['Citalopram'], ['Clindamicina'], ['Clonazepam'], ['Ciclobenzaprina'], ['Cymbalta'], ['Doxiciclina'], ['Dupixente'], ['Entresto'], ['Entívio'], ['Farxiga'], ['Adesivo de Fentanil'], ['Gabapentina'], ['Gemtesa'], ['Humira'], ['Hidroclorotiazida'], ['Ibuprofeno'], ['Imbruvica'], ['Janúvia'], ['Jardiance'], ['Lexapro'], ['Lisinopril'], ['Lofexidina'], ['Loratadina'], ['Lírica'], ['Melatonina'], ['Meloxicam'], ['Metformina'], ['Metadona'], ['Metotrexato'], ['Metoprolol'], ['Mounjaro'], ['Naltrexona'], ['Naproxeno'], ['Narcano'], ['Nurtec'], ['Omeprazol'], ['Opdivo'], ['Otezla'], ['Ozempico'], ['Pantoprazol'], ['Plano B'], ['Prednisona'], ['Probufina'], ['Qulipta'], ['Quviviq'], ['Ribelso'], ['Tepezza'], ['Tramadol'], ['Trazodona'], ['Viagra'], ['Vraylar'], ['Wegovy'], ['Wellbutrin'], ['Xanax'], ['Ervoy'], ['Zubsolv']]
SPECIALITIES = ["radiologia","ortopedia","cardiologia","neurologia","oncologia"]
SYMPTOMS = ['Dor de cabeça', 'Náusea', 'Tontura', 'Fadiga', 'Dor no peito', 'Falta de ar', 'Dor abdominal', 'Dor nas costas', 'Febre', 'Tosse', 'Espirros', 'Coriza', 'Dor de garganta', 'Calafrios', 'Suores noturnos', 'Perda de apetite', 'Perda de peso', 'Ganho de peso', 'Vermelhidão nos olhos', 'Coceira', 'Erupção cutânea', 'Inchaço', 'Dor nas articulações', 'Dificuldade para engolir', 'Sensação de queimação ao urinar', 'Urina turva', 'Fezes com sangue', 'Diarreia', 'Constipação', 'Palpitações', 'Ansiedade', 'Depressão', 'Confusão mental', 'Insônia', 'Sonolência excessiva', 'Zumbido nos ouvidos', 'Alterações na visão', 'Sensibilidade à luz', 'Perda de audição', 'Boca seca', 'Perda de olfato', 'Perda de paladar', 'Vômitos', 'Sangramento nasal', 'Hematomas frequentes', 'Sangramento nas gengivas', 'Sensação de formigamento', 'Rigidez muscular', 'Desmaio', 'Dificuldade para respirar à noite']
METRICS = ['Temperatura corporal (°C)', 'Pressão arterial (mmHg)', 'Frequência cardíaca (bpm)', 'Saturação de oxigênio (%)', 'Frequência respiratória (respirações/min)', 'Glicemia (mg/dL)', 'Nível de colesterol total (mg/dL)', 'Triglicerídeos (mg/dL)', 'Peso corporal (kg)', 'Altura (cm)', 'Índice de Massa Corporal (IMC)', 'Circunferência da cintura (cm)', 'Nível de hemoglobina (g/dL)', 'Contagem de leucócitos (milhões/mm3)', 'Contagem de plaquetas (milhares/mm3)', 'Nível de creatinina (mg/dL)', 'Taxa de filtração glomerular (TFG)', 'Bilirrubina total (mg/dL)', 'Nível de albumina (g/dL)', 'Tempo de protrombina (segundos)']
MAX_CLINICS = 5
MAX_PATIENTS = 5000
MAX_NURSES = 6
MAX_MEDICS = 60

nifs = [i + 100000000 for i in range(5090)]
phones = [i + 910000000 for i in range(5095)]
snss = [i + 10000000000 for i in range(5090)]
clinics = []
nurses = []
medics = []
patients = []
works = []
appointments = []
prescriptions = []
observations = []

fake = faker.Faker("pt_PT")


def get_random_address(char_limit=255):
    address = fake.city() + " " + fake.street_name() + " " + fake.building_number() + " " + fake.postcode()
    address = address.replace("'", "")
    while len(address) > char_limit:
        address = fake.city() + " " + fake.street_name() + " " + fake.building_number() + " " + fake.postcode()
        address = address.replace("'", "")
    return address

def get_random_name(char_limit=80):
    name = fake.first_name() + " " + fake.last_name()
    name = name.replace("'", "")
    while len(name) > char_limit:
        name = fake.first_name() + " " + fake.last_name()
        name = name.replace("'", "")
    return name

def get_random_last_name():
    name = fake.last_name()
    name = name.replace("'", "")
    return name

# clinica:
# nome (varchar(80) UNIQUE NOT NULL)
# telefone (varchar(15) UNIQUE NOT NULL)
# morada (varchar(255) NOT NULL)

def gen_clinics():
    for i in range(MAX_CLINICS):
        clinic = []
        name = "Clinica "+ get_random_last_name()
        clinic.append(name)
        clinic.append(phones.pop(0))
        clinic.append(get_random_address())
        clinics.append(clinic)
    with open("clinica.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("nome, telefone, morada\n")
        for i in clinics:
            csvfile.write(f"{i[0]}, {i[1]}, {i[2]}\n")

# enfermeiro:
# nif (char(9) PRIMARY KEY)
# nome (varchar(80) UNIQUE NOT NULL)
# telefone (varchar(15) NOT NULL)
# morada (varchar(255) NOT NULL)
# nome_clinica (varchar(80) NOT NULL references clinica(nome))

def gen_nurses():
    for i in range(MAX_NURSES):
        for j in range(MAX_CLINICS):
            nurse = []
            nurse.append(nifs.pop(0))
            nurse.append(get_random_name())
            nurse.append(phones.pop(0))
            nurse.append(get_random_address())
            nurse.append(clinics[j][0])
            nurses.append(nurse)
            
    with open("enfermeiro.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("nif, nome, telefone, morada, nome_clinica\n")
        for i in nurses:
            csvfile.write(f"{i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}\n")

# medico:
# nif (char(9) PRIMARY KEY)
# nome (varchar(80) UNIQUE NOT NULL)
# telefone (varchar(15) NOT NULL)
# morada (varchar(255) NOT NULL)
# especialidade (varchar(80) NOT NULL)
#20 médicos de especialidade ‘clínica geral’ e 40 outros distribuídos como entender por até 5
# especialidades diferentes

def gen_medics():
    for i in range(MAX_MEDICS):
        medic = []
        medic.append(nifs.pop(0))
        medic.append(get_random_name())
        medic.append(phones.pop(0))
        medic.append(get_random_address())
        if i < 20:
            medic.append("clínica geral")
        else:
            medic.append(random.choice(SPECIALITIES))
        medics.append(medic)
    with open("medico.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("nif, nome, telefone, morada, especialidade\n")
        for i in medics:
            csvfile.write(f"{i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}\n")

# trabalha:
# nif (char(9) NOT NULL references medico(nif))
# nome (varchar(80) NOT NULL references clinica(nome))
# dia_da_semana SMALLINT
# PRIMARY KEY (nif, dia_da_semana)
# Cada médico deve trabalhar em pelo menos duas clínicas, 
# Cada Clínica tem pelo menos 8 médicos por dia


def gen_works():

    for medic in medics:
        assigned_clinics = random.choices(clinics, k=7)
        assigned_days = range(7)
        for clinic, day in zip(assigned_clinics, assigned_days):
            work = []
            work.append(medic[0])
            work.append(clinic[0])
            work.append(day)
            works.append(work)        
            
    # Write to file
    with open("trabalha.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("nif, nome, dia_da_semana\n")
        for work in works:
            csvfile.write(f"{work[0]}, {work[1]}, {work[2]}\n")

def read_trabalha():
    trabalha = []
    with open("trabalha.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            nif, clinic, weekday = row.strip().split(",")
            trabalha.append([nif, clinic, weekday])
    return trabalha


# paciente:
# ssn (char(11) PRIMARY KEY)
# nif (char(9) UNIQUE NOT NULL)
# nome (varchar(80) NOT NULL)
# telefone (varchar(15) NOT NULL)
# morada (varchar(255) NOT NULL)
# data_nasc DATE NOT NULL

def gen_patients():
    for i in range(MAX_PATIENTS):
        patient = []
        patient.append(snss.pop(0))
        patient.append(nifs.pop(0))
        patient.append(get_random_name())
        patient.append(phones.pop(0))
        patient.append(get_random_address())
        patient.append(fake.date_of_birth(minimum_age=18, maximum_age=92))
        patients.append(patient)
    with open("paciente.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("ssn, nif, nome, telefone, morada, data_nasc\n")
        for i in patients:
            csvfile.write(f"{i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]}, {i[5]}\n")

# consulta:
# id SERIAL PRIMARY KEY
# ssn (char (11) NOT NULL references paciente(ssn))
# nif (char(9) NOT NULL references medico(nif))
# nome (varchar(80) NOT NULL references clinica(nome))
# data DATE NOT NULL
# hora TIME NOT NULL
# codigo_sns CHAR(12) UNIQUE
# UNIQUE (ssn, data, hora)
# UNIQUE (nif, data, hora)
# Desde o início de 2023 até o fim de 2024 
# Cada Clínica tem pelo menos 20 consultas por dia distribuidas por cada médico que trabalhou na clínica nesse dia
# Cada médico tem pelo menos 2 consultas por dia que trabalhou
# Cada Paciente tem pelo menos 1 consulta por ano

def generate_times():
    morning_start_time = datetime.strptime("08:00", "%H:%M")
    morning_end_time = datetime.strptime("12:30", "%H:%M")
    afternoon_start_time = datetime.strptime("14:00", "%H:%M")
    afternoon_end_time = datetime.strptime("18:30", "%H:%M")
    times = []
    
    current_time = morning_start_time
    while current_time <= morning_end_time:
        times.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)
    
    current_time = afternoon_start_time
    while current_time <= afternoon_end_time:
        times.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)
    
    return times

from datetime import *

def gen_appointments():
    codigo_sns = 100000000000
    id_counter = 1
    first_day = datetime(2023, 1, 1)
    times = generate_times()
    
    for i in range(731):
        patients_temp = patients.copy()
        day = first_day + timedelta(days=i)
        for work in works:
            if work[2] == day.weekday(): # x % 7 = (0-6) -> 0 = segunda, 6 = domingo
                times_temp = times.copy()
                for _ in range(3):
                    appointment = []
                    appointment.append(id_counter)
                    patient = random.choice(patients_temp)
                    patients_temp.remove(patient)
                    appointment.append(patient[0])
                    appointment.append(work[0])
                    appointment.append(work[1])
                    appointment.append(day.date())
                    time = random.choice(times_temp)
                    times_temp.remove(time)
                    appointment.append(time)
                    appointment.append(codigo_sns)
                    appointments.append(appointment)
                    id_counter += 1
                    codigo_sns += 1

    seen = set()
    appointments_no_duplicates = []

    for appointment in appointments:
        
        key_nif = (appointment[1], appointment[4], appointment[5])
        key_ssn = (appointment[2], appointment[4], appointment[5])
        
        if key_nif not in seen and key_ssn not in seen:
            appointments_no_duplicates.append(appointment)
            seen.add(key_nif)
            seen.add(key_ssn)

    appointments.clear()
    for i in appointments_no_duplicates:
        appointments.append(i)
                
    with open("consulta.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("id, ssn, nif, nome, data, hora, codigo_sns\n")
        for appointment in appointments_no_duplicates:
            csvfile.write(f"{appointment[0]}, {appointment[1]}, {appointment[2]}, {appointment[3]}, {appointment[4]}, {appointment[5]}, {appointment[6]}\n")

# receita:
# codigo_sns VARCHAR(12)
# medicamento VARCHAR(155)
# quantidade SMALLINT NOT NULL CHECK (quantidade > 0)
# PRIMARY KEY (codigo_sns, medicamento)
# 80% das consultas tem receita médica associada, 
# e as receitas têm 1 a 6 medicamentos em
# quantidades entre 1 e 3
limit_date = datetime(2024, 5, 30).date()

def gen_prescriptions():
    for appointment in appointments:
        date = appointment[4]
        
        if date > limit_date:
            break
        
        if random.random() < 0.8:
            medicine = ""
            prescription = []
            prescription.append(appointment[6])
            for _ in range(random.randint(1, 6)):
                medicine += random.choice(MEDICINE)[0] + " "
            medicine.strip()
            prescription.append(medicine)
            prescription.append(random.randint(1, 3))
            prescriptions.append(prescription)
                
    with open("receita.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("codigo_sns, medicamento, quantidade\n")
        for prescription in prescriptions:
            csvfile.write(f"{prescription[0]}, {prescription[1]}, {prescription[2]}\n")

# observacao:
# id INTEGER NOT NULL references consulta(id)
# parametro VARCHAR(155) NOT NULL
# valor FLOAT
# PRIMARY KEY (id, parametro) Todas as consultas têm 1 a 5 
# observações de sintomas (com parâmetro mas sem valor ("NULL")) e 0 a 3
# observações métricas (com parâmetro e valor).

def gen_observations():
    for appointment in appointments:
        date = appointment[4]
        if date > limit_date:
            break
        app_sypmtoms = []
        for _ in range(random.randint(1, 5)):
            observation = []
            observation.append(appointment[0])
            symptom = random.choice(SYMPTOMS)
            while symptom in app_sypmtoms:
                symptom = random.choice(SYMPTOMS) 
            app_sypmtoms.append(symptom)
            observation.append(symptom)
            observation.append("NULL")
            observations.append(observation)
        for _ in range(random.randint(0, 3)):
            observation = []
            observation.append(appointment[0])
            symptom = random.choice(METRICS)
            while symptom in app_sypmtoms:
                symptom = random.choice(METRICS)
            app_sypmtoms.append(symptom)
            observation.append(symptom)
            observation.append(random.uniform(0, 100))
            observations.append(observation)

    with open("observacao.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("id, parametro, valor\n")
        for observation in observations:
            csvfile.write(f"{observation[0]}, {observation[1]}, {observation[2]}\n")

def csv_to_sql():
    with open("database.sql", "w", encoding='utf-8') as sqlfile:
        files = ["clinica.csv", "enfermeiro.csv", "medico.csv", "trabalha.csv", "paciente.csv", "consulta.csv", "receita.csv", "observacao.csv"]
        tables = ["Clinica", "Enfermeiro", "Medico", "Trabalha", "Paciente", "Consulta", "Receita", "Observacao"]
        columns = [
            "(nome, telefone, morada)",
            "(nif, nome, telefone, morada, nome_clinica)",
            "(nif, nome, telefone, morada, especialidade)",
            "(nif, nome, dia_da_semana)",
            "(ssn, nif, nome, telefone, morada, data_nasc)",
            "(id, ssn, nif, nome, data, hora, codigo_sns)",
            "(codigo_sns, medicamento, quantidade)",
            "(id, parametro, valor)"
        ]

        for file, table, column in zip(files, tables, columns):
            with open(file, "r", encoding='utf-8') as csvfile:
                sqlfile.write(f"INSERT INTO {table} {column} VALUES\n")
                rows = csvfile.readlines()[1:]  # Skip the header
                for row in rows[:-1]:
                    values = ",".join([f"'{x.strip()}'" if x.strip() != "NULL" else "NULL" for x in row.split(",")])
                    sqlfile.write(f"({values}),\n")
                values = ",".join([f"'{x.strip()}'" if x.strip() != "NULL" else "NULL" for x in rows[-1].split(",")])
                sqlfile.write(f"({values});\n")  # Last row with semicolon
            sqlfile.write("\n")  # Add a newline between different tables
            
if __name__ == "__main__":
    while(True):
        print("Selecione a opção que deseja executar:")
        print("1 - Criar ficheiro SQL")
        print("q - Sair")
        input_option = input()

        if input_option == "1":
            gen_clinics()
            print("Clínicas criadas com sucesso!")
            gen_nurses()
            print("Enfermeiros criados com sucesso!")
            gen_medics()
            print("Médicos criados com sucesso!")
            gen_works()
            print("Trabalha criado com sucesso!")
            gen_patients()
            print("Pacientes criados com sucesso!")
            gen_appointments()
            print("Consultas criadas com sucesso!")
            gen_prescriptions()
            print("Receitas criadas com sucesso!")
            gen_observations()
            print("Observações criadas com sucesso!")
            delete_csv = input("Se quiser realizar alguma mudança nos ficheiros CSV, faça-o agora.\nDepois de terminar, pressione 'Enter' para continuar.")
            csv_to_sql()
            os.remove("clinica.csv")
            os.remove("enfermeiro.csv")
            os.remove("medico.csv")
            os.remove("trabalha.csv")
            os.remove("paciente.csv")
            os.remove("consulta.csv")
            os.remove("receita.csv")
            os.remove("observacao.csv")
            print("Ficheiro SQL criado com sucesso!")
            break
            
        elif input_option == "q":
            break