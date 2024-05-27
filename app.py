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

    return jsonify(clinicas)

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

    return jsonify(especialidades)

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
                    WHERE m.especialidade = 'cardiologia' AND t.nome = 'Clinica B') AS t
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
            print(medicos)
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(medicos)

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
    if paciente == None:
        erro = "Especifique um paciente."
    elif medico == None:
        erro = "Especifique um medico."
    elif data == None:
        erro = "Especifique uma data."
    elif hora == None:
        erro = "Especifique uma hora."
    if erro is not None:
        return erro, 400
    else:
        with psycopg.connect(conninfo=DATABASE_URL) as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                regista_consulta = cur.execute(
                    """
                    INSERT INTO consulta (ssn, nif, nome, data, hora)
                        VALUES (%(ssn)s, %(nif)s, %(nome)s, %(data)s, %(hora)s);
                    """,
                    {"ssn": paciente, "nif": medico, "nome": clinica, "data": data, "hora": hora},
                )

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
    if paciente == None:
        erro = "Especifique um paciente."
    elif medico == None:
        erro = "Especifique um medico."
    elif data == None:
        erro = "Especifique uma data."
    elif hora == None:
        erro = "Especifique uma hora."
    if erro is not None:
        return erro, 400
    else:
        with psycopg.connect(conninfo=DATABASE_URL) as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                    DELETE FROM 
                    consulta 
                    WHERE ssn = %(ssn)s AND nif = %(nif)s AND nome = %(nome)s AND data = %(data)s AND hora = %(hora)s;
                    """,
                    {"ssn": paciente, "nif": medico, "nome": clinica, "data": data, "hora": hora},
                )

    return "", 204

@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})

@app.route("/load", methods=("POST",))
def loadDB():
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            f = open("data/LoadDB.sql")
            cur.execute(f.read())
            f.close()
            f = open("data/IntegrityConstraints.sql")
            cur.execute(f.read())
            f.close()
            f = open("data/Populate.sql")
            cur.execute(f.read())
            f.close()
            f = open("data/MaterializedView.sql")
            cur.execute(f.read())
            f.close()

if __name__ == "__main__":
    app.run()