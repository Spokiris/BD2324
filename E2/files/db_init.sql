DROP TABLE IF EXISTS clinica CASCADE;
DROP TABLE IF EXISTS enfermeiro CASCADE;
DROP TABLE IF EXISTS medico CASCADE;
DROP TABLE IF EXISTS trabalha CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS receita CASCADE;
DROP TABLE IF EXISTS consulta CASCADE;
DROP TABLE IF EXISTS observacao CASCADE;

CREATE TABLE clinica(
nome VARCHAR(80) PRIMARY KEY,
telefone VARCHAR(15) UNIQUE NOT NULL CHECK (telefone ~ '^[0-9]+$'),
morada VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE enfermeiro(
nif CHAR(9) PRIMARY KEY CHECK (nif ~ '^[0-9]+$'),
nome VARCHAR(80) UNIQUE NOT NULL,
telefone VARCHAR(15) NOT NULL CHECK (telefone ~ '^[0-9]+$'),
morada VARCHAR(255) NOT NULL,
nome_clinica VARCHAR(80) NOT NULL REFERENCES clinica (nome)
);

CREATE TABLE medico(
nif CHAR(9) PRIMARY KEY CHECK (nif ~ '^[0-9]+$'),
nome VARCHAR(80) UNIQUE NOT NULL,
telefone VARCHAR(15) NOT NULL CHECK (telefone ~ '^[0-9]+$'),
morada VARCHAR(255) NOT NULL,
especialidade VARCHAR(80) NOT NULL
);

CREATE TABLE trabalha(
nif CHAR(9) NOT NULL REFERENCES medico,
nome VARCHAR(80) NOT NULL REFERENCES clinica,
dia_da_semana SMALLINT,
PRIMARY KEY (nif, dia_da_semana)
);

CREATE TABLE paciente(
ssn CHAR(11) PRIMARY KEY CHECK (ssn ~ '^[0-9]+$'),
nif CHAR(9) UNIQUE NOT NULL CHECK (nif ~ '^[0-9]+$'),
nome VARCHAR(80) NOT NULL,
telefone VARCHAR(15) NOT NULL CHECK (telefone ~ '^[0-9]+$'),
morada VARCHAR(255) NOT NULL,
data_nasc DATE NOT NULL
);

CREATE TABLE consulta(
id SERIAL PRIMARY KEY,
ssn CHAR(11) NOT NULL REFERENCES paciente,
nif CHAR(9) NOT NULL REFERENCES medico,
nome VARCHAR(80) NOT NULL REFERENCES clinica,
data DATE NOT NULL,
hora TIME NOT NULL,
codigo_sns CHAR(12) UNIQUE CHECK (codigo_sns ~ '^[0-9]+$'),
UNIQUE(ssn, data, hora),
UNIQUE(nif, data, hora)
);

CREATE TABLE receita(
codigo_sns VARCHAR(12) NOT NULL REFERENCES consulta (codigo_sns),
medicamento VARCHAR(155) NOT NULL,
quantidade SMALLINT NOT NULL CHECK (quantidade > 0),
PRIMARY KEY (codigo_sns, medicamento)
);

CREATE TABLE observacao(
id INTEGER NOT NULL REFERENCES consulta,
parametro VARCHAR(155) NOT NULL,
valor FLOAT,
PRIMARY KEY (id, parametro)
);

-- (RI-1)
ALTER TABLE consulta
ADD CONSTRAINT consulta_time_check CHECK (
    (EXTRACT(MINUTE FROM hora) IN (0, 30)) AND 
    ((EXTRACT(HOUR FROM hora) BETWEEN 8 AND 13) OR (EXTRACT(HOUR FROM hora) BETWEEN 14 AND 19))
);

-- (RI-2)
CREATE OR REPLACE FUNCTION is_self_consulta(ssn character, nif character) RETURNS boolean AS $$
BEGIN
    RETURN EXISTS (SELECT 1 FROM paciente p WHERE p.ssn = is_self_consulta.ssn AND p.nif = is_self_consulta.nif);
END;
$$ LANGUAGE plpgsql;

ALTER TABLE consulta
ADD CONSTRAINT self_consulta_check CHECK (is_self_consulta(ssn, nif) = false);

-- (RI-3)
CREATE OR REPLACE FUNCTION is_valid_clinic_day(nif character, data date) RETURNS boolean AS $$
BEGIN
    RETURN EXISTS (SELECT 1 FROM trabalha WHERE trabalha.nif = is_valid_clinic_day.nif AND dia_da_semana = EXTRACT(DOW FROM data));
END;
$$ LANGUAGE plpgsql;

ALTER TABLE consulta
ADD CONSTRAINT clinic_day_check CHECK (is_valid_clinic_day(nif, data) = true);