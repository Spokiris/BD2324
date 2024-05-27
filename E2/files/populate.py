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

fake = faker.Faker("pt_PT")

def get_random_address():
    address = fake.city() + " " + fake.street_name() + " " + fake.building_number() + " " + fake.postcode()
    return address

def populate_clinics():
    # Creates a CSV file with the clinics
    with open("clinica.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("nome, telefone, morada\n")
        for i in range(MAX_CLINICS):
            name = "Clínica " + fake.company()
            phone = random.randint(900000000, 999999999)
            address = get_random_address()
            csvfile.write(f"{name},{phone},{address}\n")

def read_clinics():
    clinics = []
    with open("clinica.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            name, phone, address = row.strip().split(",")
            clinics.append([name, phone, address])
    return clinics

def populate_nurses():
    clinics = read_clinics()
    # Creates a CSV file with the nurses
    with open("enfermeiro.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("nif, nome, telefone, morada, nome_clinica\n")
        for i in range(MAX_CLINICS):
            for j in range(MAX_NURSES):
                nif = random.randint(100000000, 999999999)
                name = fake.name()
                phone = random.randint(900000000, 999999999)
                address = get_random_address()
                csvfile.write(f"{nif},{name},{phone},{address},{clinics[i][0]}\n")

def read_nurses():
    nurses = []
    with open("enfermeiro.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            nif, name, phone, morada, clinic = row.strip().split(",")
            nurse = [nif, name, phone, morada, clinic]
            nurses.append(nurse)
    return nurses

def populate_medics():
    with open("medico.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("nif, nome, telefone, morada, especialidade\n")
        for i in range(20):
            nif = random.randint(100000000, 999999999)
            name = fake.name()
            phone = random.randint(900000000, 999999999)
            address = get_random_address()
            speciality = "clínica geral"
            csvfile.write(f"{nif},{name},{phone},{address},{speciality}\n")
        for i in range(8):
            for speciality in SPECIALITIES:
                nif = random.randint(100000000, 999999999)
                name = fake.name()
                phone = random.randint(900000000, 999999999)
                address = get_random_address()
                csvfile.write(f"{nif},{name},{phone},{address},{speciality}\n")

def read_medics():
    medics = []
    with open("medico.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            nif, name, phone, morada, speciality = row.strip().split(",")
            medic = [nif, name, phone, morada, speciality]
            medics.append(medic)
    return medics

def populate_trabalha():
    nifs = [medic[0] for medic in read_medics()]
    clinics = [clinic[0] for clinic in read_clinics()]
    schedule = {nif: [] for nif in nifs}
    clinic_doctors = {clinic: {day: [] for day in range(1, 8)} for clinic in clinics}

    # Assign each doctor to two different clinics on different days
    for nif in nifs:
        clinic_days = random.sample(list(clinic_doctors.items()), 2)
        for clinic, days in clinic_days:
            day = random.choice(list(days.keys()))
            while len(days[day]) >= 8:
                day = random.choice(list(days.keys()))
            schedule[nif].append((clinic, day))
            days[day].append(nif)

    # Check if each clinic has at least 8 doctors for each day
    for clinic, days in clinic_doctors.items():
        for day, doctors in days.items():
            while len(doctors) < 8:
                nif = random.choice(nifs)
                while (clinic, day) in schedule[nif]:
                    nif = random.choice(nifs)
                schedule[nif].append((clinic, day))
                doctors.append(nif)

    # Write the schedule to the CSV file
    with open("trabalha.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("nif, nome_clinica, dia_da_semana\n")
        for nif, workdays in schedule.items():
            for clinic, day in workdays:
                csvfile.write(f"{nif},{clinic},{day}\n")

def read_trabalha():
    trabalha = []
    with open("trabalha.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            nif, clinic, weekday = row.strip().split(",")
            trabalha.append([nif, clinic, weekday])
    return trabalha

def populate_patients():
    with open("paciente.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("ssn, nif, nome, telefone, morada, data_nasc\n")
        for i in range(MAX_PATIENTS):
            ssn = random.randint(100000000, 999999999)
            nif = random.randint(100000000, 999999999)
            name = fake.name()
            phone = random.randint(900000000, 999999999)
            address = get_random_address()
            birthdate = fake.date_of_birth(minimum_age=18, maximum_age=78)
            csvfile.write(f"{ssn},{nif},{name},{phone},{address},{birthdate}\n")

def read_patients():
    patients = []
    with open("paciente.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            ssn, nif, name, phone, morada, birthdate = row.strip().split(",")
            patient = [ssn, nif, name, phone, morada, birthdate]
            patients.append(patient)
    return patients

def populate_consulta():
    patients = [patient[0] for patient in read_patients()]
    medics = [medic[0] for medic in read_medics()]
    clinics = [clinic[0] for clinic in read_clinics()]
    appointments = {}
    clinic_appointments = {clinic: {date: [] for date in range(1, 731)} for clinic in clinics}  # 731 days in 2023 and 2024
    medic_appointments = {medic: {date: [] for date in range(1, 731)} for medic in medics}

    # Assign each patient to a random clinic and doctor on a random day and time
    for ssn in patients:
        clinic = random.choice(clinics)
        medic = random.choice(medics)
        date = random.randint(1, 730)
        time = random.randint(8, 20)  # Assuming the clinic operates from 8:00 to 20:00
        snscod = random.randint(100000000000, 999999999999)
        id = len(appointments) + 1
        appointments[id] = (ssn, medic, clinic, date, time, snscod)
        clinic_appointments[clinic][date].append(id)
        medic_appointments[medic][date].append(id)

    # Check if each clinic has at least 20 appointments for each day and each doctor has at least 2 appointments for each day
    for clinic, dates in clinic_appointments.items():
        for date, ids in dates.items():
            while len(ids) < 20:
                ssn = random.choice(patients)
                medic = random.choice(medics)
                time = random.randint(8, 20)
                snscod = ''.join(random.choices('0123456789', k=12))
                id = len(appointments) + 1
                appointments[id] = (ssn, medic, clinic, date, time, snscod)
                ids.append(id)
                medic_appointments[medic][date].append(id)

    for medic, dates in medic_appointments.items():
        for date, ids in dates.items():
            while len(ids) < 2:
                ssn = random.choice(patients)
                clinic = random.choice(clinics)
                time = random.randint(8, 20)
                snscod = ''.join(random.choices('0123456789', k=12))
                id = len(appointments) + 1
                appointments[id] = (ssn, medic, clinic, date, time, snscod)
                ids.append(id)
                clinic_appointments[clinic][date].append(id)

    # Write the schedule to the CSV file
    with open("consulta.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("id, ssn, nif, nome, data, hora, codigo_sns\n")
        for id, (ssn, medic, clinic, date, time, snscod) in appointments.items():
            date_str = (datetime.datetime(2023, 1, 1) + datetime.timedelta(days=date-1)).strftime('%Y-%m-%d')
            csvfile.write(f"{id},{ssn},{medic},{clinic},{date_str},{time},{snscod}\n")

def read_consultas():
    consulta = []
    with open("consulta.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            id, ssn, medic, clinic, date, time, snscod = row.strip().split(",")
            consulta.append([id, ssn, medic, clinic, date, time, snscod])
    return consulta

def populate_receita():
    snscodes = [consulta[6] for consulta in read_consultas()]
    with open("receita.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("codigo_ssn, medicamento, quantidade\n")
        for snscod in snscodes:
            if random.random() > 0.8:
                continue
            medicine_count = random.randint(1, 6)
            drugs = random.sample(MEDICINE, medicine_count)
            drugs = [drug[0] for drug in drugs]
            while len(' '.join(drugs)) > 155:
                drugs.pop()
            medicine = ' '.join(drugs)
            dosage = random.randint(1, 3)
            csvfile.write(f"{snscod},{medicine},{dosage}\n")

def read_receita():
    receita = []
    with open("receita.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            snscod, medicine, dosage = row.strip().split(",")
            receita.append([snscod, medicine, dosage])
    return receita

def populate_observacao():
    ids = [consulta[0] for consulta in read_consultas()]
    with open("observacao.csv","w", encoding='utf-8') as csvfile:
        csvfile.write("id, parametro, valor\n")
        for id in ids:
            symptoms_count = random.randint(1, 5)
            symptoms = random.sample(SYMPTOMS, symptoms_count)
            symptoms = [symptom for symptom in symptoms]
            for symptom in symptoms:
                csvfile.write(f"{id},{symptom},NULL\n")
            metrics_count = random.randint(0, 3)
            metrics = random.sample(METRICS, metrics_count)
            metrics = [metric for metric in metrics]
            for metric in metrics:
                value = round(random.uniform(1, 100), 2)
                csvfile.write(f"{id},{metric},{value}\n")

def read_observacao():
    observacao = []
    with open("observacao.csv", "r", encoding='utf-8') as csvfile:
        next(csvfile) # Skip the header
        for row in csvfile:
            id, observation, value = row.strip().split(",")
            observacao.append([id, observation, value])
    return observacao

def csv_to_sql():
    with open("database.sql", "w", encoding='utf-8') as sqlfile:
        files = ["clinica.csv", "enfermeiro.csv", "medico.csv", "trabalha.csv", "paciente.csv", "consulta.csv", "receita.csv", "observacao.csv"]
        tables = ["Clinica", "Enfermeiro", "Medico", "Trabalha", "Paciente", "Consulta", "Receita", "Observacao"]
        columns = [
            "(nome, telefone, morada)",
            "(nif, nome, telefone, morada, nome_clinica)",
            "(nif, nome, telefone, morada, especialidade)",
            "(nif, nome_clinica, dia_da_semana)",
            "(ssn, nif, nome, telefone, morada, data_nasc)",
            "(id, ssn, nif, nome, data, hora, codigo_sns)",
            "(codigo_ssn, medicamento, quantidade)",
            "(id, parametro, valor)"
        ]

        for file, table, column in zip(files, tables, columns):
            with open(file, "r", encoding='utf-8') as csvfile:
                sqlfile.write(f"INSERT INTO {table} {column} VALUES\n")
                rows = csvfile.readlines()[1:]  # Skip the header
                for row in rows[:-1]:
                    values = ", ".join([f"'{x}'" if isinstance(x, str) else str(x) for x in row.strip().split(",")])
                    sqlfile.write(f"({values}),\n")
                values = ", ".join([f"'{x}'" if isinstance(x, str) else str(x) for x in rows[-1].strip().split(",")])
                sqlfile.write(f"({values});\n")  # Last row with semicolon
            sqlfile.write("\n")  # Add a newline between different tables

if __name__ == "__main__":
    while(True):
        print("Selecione a opção que deseja executar:")
        print("1 - Criar ficheiro SQL")
        print("q - Sair")
        input_option = input()

        if input_option == "1":
            populate_clinics()
            print("Clínicas criadas com sucesso!")
            populate_nurses()
            print("Enfermeiros criados com sucesso!")
            populate_medics()
            print("Médicos criados com sucesso!")
            populate_trabalha()
            print("Trabalha criado com sucesso!")
            populate_patients()
            print("Pacientes criados com sucesso!")
            populate_consulta()
            print("Consultas criadas com sucesso!")
            populate_receita()
            print("Receitas criadas com sucesso!")
            populate_observacao()
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