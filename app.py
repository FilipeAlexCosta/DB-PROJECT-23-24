#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
from logging.config import dictConfig

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
# Use the format postgres://username:password@hostname/database_name to connect to the database.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://saude:saude@postgres/saude")

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

def is_integer(any) -> bool:
    try:
        int(any)
        return True
    except ValueError:
        return False

@app.route("/", methods=("GET",))
def lista_clinicas():
    """Lista todas as clínicas (nome e morada)."""
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            clinicas = cur.execute(
                """
                SELECT nome, morada FROM clinica;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(clinicas), 200

@app.route("/c/<clinica>/", methods=("GET",))
def lista_especialidades(clinica):
    """Lista todas as especialidades oferecidas na <clinica>."""
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            especialidades = cur.execute(
                """
                SELECT DISTINCT especialidade
                FROM (SELECT nome FROM clinica WHERE nome = %(nome)s)
                    INNER JOIN trabalha USING(nome) INNER JOIN medico USING(nif);
                """,
                {"nome": clinica},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(especialidades), 200

@app.route("/c/<clinica>/<especialidade>/", methods=("GET",))
def lista_medicos(clinica, especialidade):
    """Lista todos os médicos (nome) da <especialidade> que
    trabalham na <clínica> e os primeiros três horários
    disponíveis para consulta de cada um deles (data e hora)."""
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            medicos = cur.execute(
                """
                WITH datas AS (
                    SELECT
                        x::date AS data, x::time as hora
                    FROM
                        generate_series(timestamp '2024-01-01', timestamp '2024-12-31', interval '30 min') AS x
                    WHERE
                        ((x::time BETWEEN '08:00:00' AND '12:30:00') OR
                        (x::time BETWEEN '14:00:00' AND '18:30:00')) AND
                        x::timestamp > NOW()::timestamp
                ), possible AS (
                    SELECT t.nome_medico, d.data, d.hora
                    FROM (SELECT t.nif, t.dia_da_semana, m.nome AS nome_medico
                    FROM trabalha t INNER JOIN medico m USING(nif)
                    WHERE m.especialidade = %(especialidade)s AND t.nome = %(nome)s) AS t
                    INNER JOIN datas d ON(EXTRACT(dow FROM d.data) = t.dia_da_semana)
                    LEFT OUTER JOIN consulta c ON(t.nif = c.nif AND d.data = c.data AND d.hora = c.hora)
                    WHERE c.id IS NULL
                )
                SELECT p1.nome_medico, (p1.data + p1.hora) AS data
                FROM possible p1 INNER JOIN possible p2 ON (p1.nome_medico = p2.nome_medico AND (p1.data + p1.hora) >= (p2.data + p2.hora))
                GROUP BY p1.nome_medico, p1.data, p1.hora
                HAVING COUNT(*) <= 3
                ORDER BY p1.data, p1.nome_medico, p1.hora;
                """,
                {"nome": clinica, "especialidade": especialidade},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(medicos), 200

def organiza_erro(error):
    erro = ""
    if error.diag.message_primary is not None:
        erro += str(error.diag.message_primary)
    if error.diag.message_detail is not None:
        erro += str(error.diag.message_detail)
    return erro

@app.route("/a/<clinica>/registar", methods=("POST",))
def regista_consulta(clinica):  
    """Registra uma marcação de consulta na <clinica> na base
    de dados (populando a respectiva tabela). Recebe como
    argumentos um paciente, um médico, e uma data e hora
    (posteriores ao momento de agendamento)."""
    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")
    erro = None
    if paciente == None or not is_integer(paciente) or len(paciente) != 11:
        erro = f"o ssn '{paciente}' do paciente é inválido"
    elif medico == None or not is_integer(medico) or len(medico) != 9:
        erro = f"o nif '{medico}' do medico é inválido"
    elif data == None or data == '':
        erro = "Especifique uma data."
    elif hora == None or hora == '':
        erro = "Especifique uma hora."
    if erro is not None:
        return jsonify({"message": erro, "status": "error"}), 400
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            try:
                cur.execute(
                    """
                    SELECT TO_DATE(%(data)s, 'YYYY-MM-DD');
                    """,
                    {"data": data}
                )
            except Exception:
                return jsonify({"message": f"a data '{data}' é inválida (tem de ter formato YYYY-MM-DD)", "status": "error"}), 400
            try:
                cur.execute(
                    """
                    SELECT TO_TIMESTAMP(%(hora)s, 'HH24:MM:SS')::time;
                    """,
                    {"hora": hora}
                )
            except Exception:
                return jsonify({"message": f"a hora '{hora}' é inválida (tem de ter formato HH:MM:SS)", "status": "error"}), 400
            cur.execute(
                """
                SELECT * FROM NOW() AS aux WHERE TO_TIMESTAMP(%(tempo)s, 'YYYY-MM-DD HH24:MI:SS') > aux::timestamp;
                """,
                {"tempo": data + " " + hora}
            )
            if cur.rowcount == 0:
                return jsonify({"message": "o tempo tem de ser posterior ao atual", "status": "error"}), 400
            cur.execute(
                """
                SELECT * FROM clinica where nome = %(nome)s;
                """,
                {"nome": clinica}
            )
            if cur.rowcount == 0:
                return jsonify({"message": "Clinica não encontrada", "status": "error"}), 404
            try:
                cur.execute(
                    """
                    INSERT INTO consulta (ssn, nif, nome, data, hora)
                        VALUES (%(ssn)s, %(nif)s, %(nome)s, %(data)s, %(hora)s);
                    """,
                    {"ssn": paciente, "nif": medico, "nome": clinica, "data": data, "hora": hora},
                )
            except Exception as e:
                return jsonify({"message": organiza_erro(e), "status": "error"}), 400

    return "", 204

@app.route("/a/<clinica>/cancelar", methods=("POST",))
def cancela_consulta(clinica):
    """Cancela uma marcação de consulta que ainda não se realizou 
    na <clinica> (o seu horário é posterior ao momento do cancelamento), 
    removendo a entrada da respectiva tabela na base de dados. 
    Recebe como argumentos um paciente, um médico, e uma data e hora."""
    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")
    erro = None
    if paciente == None or not is_integer(paciente) or len(paciente) != 11:
        erro = f"o ssn '{paciente}' do paciente é inválido"
    elif medico == None or not is_integer(medico) or len(medico) != 9:
        erro = f"o nif '{medico}' do medico é inválido"
    elif data == None or data == '':
        erro = "Especifique uma data."
    elif hora == None or hora == '':
        erro = "Especifique uma hora."
    if erro is not None:
        return jsonify({"message": erro, "status": "error"}), 400
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            try:
                cur.execute(
                    """
                    SELECT TO_DATE(%(data)s, 'YYYY-MM-DD');
                    """,
                    {"data": data}
                )
            except Exception:
                return jsonify({"message": f"a data '{data}' é inválida (tem de ter formato YYYY-MM-DD)", "status": "error"}), 400
            try:
                cur.execute(
                    """
                    SELECT TO_TIMESTAMP(%(hora)s, 'HH24:MI:SS')::time;
                    """,
                    {"hora": hora}
                )
            except Exception as e:
                return jsonify({"message": f"a hora '{hora}' é inválida (tem de ter formato HH:MM:SS)", "status": "error"}), 400
            cur.execute(
                """
                SELECT * FROM NOW() AS aux WHERE TO_TIMESTAMP(%(tempo)s, 'YYYY-MM-DD HH24:MI:SS') > aux::timestamp;
                """,
                {"tempo": data + " " + hora}
            )
            if cur.rowcount == 0:
                return jsonify({"message": "o tempo tem de ser posterior ao atual", "status": "error"}), 400
            cur.execute(
                """
                SELECT * FROM clinica where nome = %(nome)s
                """,
                {"nome": clinica}
            )
            if cur.rowcount == 0:
                return jsonify({"message": "Clinica não encontrada", "status": "error"}), 404
            try: 
                cur.execute(
                    """
                    DELETE FROM 
                    consulta
                    WHERE ssn = %(ssn)s AND nif = %(nif)s AND nome = %(nome)s AND data = %(data)s AND hora = %(hora)s;
                    """,
                    {"ssn": paciente, "nif": medico, "nome": clinica, "data": data, "hora": hora},
                )
            except Exception as e:
                return jsonify({"message": organiza_erro(e), "status": "error"}), 400
            
            if cur.rowcount == 0:
                return jsonify({"message": "Consulta não encontrada", "status": "error"}), 404

    return "", 204

@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"}), 200

if __name__ == "__main__":
    app.run()