import os
from logging.config import dictConfig

from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg://postgres:postgres@postgres/postgres")

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": True,
        "row_factory": namedtuple_row,
    },
    min_size=4,
    max_size=10,
    open=True,
    name="postgres_pool",
    timeout=5,
)

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
log = app.logger


@app.route("/", methods=["GET"])
def list_clinics():
    """Lista todas as clínicas (nome e morada)."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            clinics = cur.execute("SELECT nome, morada FROM clinicas").fetchall()
            log.debug(f"Found {cur.rowcount} clinics.")
    return jsonify(clinics), 200


@app.route("/c/<clinica>/", methods=["GET"])
def list_specialties(clinica):
    """Lista todas as especialidades oferecidas na <clinica>."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            specialties = cur.execute(
                "SELECT especialidade FROM especialidades WHERE clinica = %(clinica)s",
                {"clinica": clinica}
            ).fetchall()
            log.debug(f"Found {cur.rowcount} specialties for clinic {clinica}.")
    return jsonify(specialties), 200


@app.route("/c/<clinica>/<especialidade>/", methods=["GET"])
def list_doctors(clinica, especialidade):
    """Lista todos os médicos (nome) da <especialidade> que trabalham na <clínica> e os primeiros três horários disponíveis para consulta de cada um deles (data e hora)."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            doctors = cur.execute(
                """
                SELECT medicos.nome, horarios.data_hora
                FROM medicos
                JOIN horarios ON medicos.id = horarios.medico_id
                WHERE medicos.clinica = %(clinica)s
                AND medicos.especialidade = %(especialidade)s
                ORDER BY horarios.data_hora ASC
                LIMIT 3;
                """,
                {"clinica": clinica, "especialidade": especialidade}
            ).fetchall()
            log.debug(f"Found {cur.rowcount} doctors and available slots for clinic {clinica}, specialty {especialidade}.")
    return jsonify(doctors), 200


@app.route("/a/<clinica>/registar/", methods=["POST"])
def register_appointment(clinica):
    """Registra uma marcação de consulta na <clinica> na base de dados."""
    data = request.json
    paciente = data.get('paciente')
    medico = data.get('medico')
    data_hora = data.get('data_hora')

    if not paciente or not medico or not data_hora:
        return jsonify({"message": "Paciente, médico e data/hora são necessários.", "status": "error"}), 400

    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO consultas (clinica, paciente, medico, data_hora)
                    VALUES (%(clinica)s, %(paciente)s, %(medico)s, %(data_hora)s);
                    """,
                    {"clinica": clinica, "paciente": paciente, "medico": medico, "data_hora": data_hora}
                )
                log.debug(f"Inserted new appointment for clinic {clinica}, patient {paciente}, doctor {medico} at {data_hora}.")
            except Exception as e:
                return jsonify({"message": str(e), "status": "error"}), 500
    return jsonify({"message": "Consulta registrada com sucesso.", "status": "success"}), 201


@app.route("/a/<clinica>/cancelar/", methods=["POST"])
def cancel_appointment(clinica):
    """Cancela uma marcação de consulta que ainda não se realizou na <clinica>."""
    data = request.json
    paciente = data.get('paciente')
    medico = data.get('medico')
    data_hora = data.get('data_hora')

    if not paciente or not medico or not data_hora:
        return jsonify({"message": "Paciente, médico e data/hora são necessários.", "status": "error"}), 400

    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    DELETE FROM consultas
                    WHERE clinica = %(clinica)s AND paciente = %(paciente)s AND medico = %(medico)s AND data_hora = %(data_hora)s;
                    """,
                    {"clinica": clinica, "paciente": paciente, "medico": medico, "data_hora": data_hora}
                )
                if cur.rowcount == 0:
                    return jsonify({"message": "Consulta não encontrada ou já realizada.", "status": "error"}), 404
                log.debug(f"Deleted appointment for clinic {clinica}, patient {paciente}, doctor {medico} at {data_hora}.")
            except Exception as e:
                return jsonify({"message": str(e), "status": "error"}), 500
    return jsonify({"message": "Consulta cancelada com sucesso.", "status": "success"}), 200


@app.route("/ping", methods=["GET"])
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
