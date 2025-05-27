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
    medicos = []
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            with conn.transaction():
                cur.execute(
                    """
                    DELETE FROM datas WHERE (data + hora) <= NOW();
                    """
                )
                res = cur.execute(
                    """
                    SELECT m.nome, d.data + d.hora
                    FROM trabalha t INNER JOIN medico m USING(nif)
                    INNER JOIN datas d ON(EXTRACT(DOW FROM d.data) = t.dia_da_semana)
                    LEFT OUTER JOIN consulta c ON(t.nif = c.nif and d.data = c.data AND d.hora = c.hora)
                    WHERE c.id IS NULL AND t.nome = %(clinica)s AND m.especialidade = %(especialidade)s
                    ORDER BY m.nome, d.data, d.hora;
                    """,
                    {"clinica": clinica, "especialidade": especialidade}
                ).fetchall()
                ultimo_nif = None
                num_linhas_nif = 0
                for linha in res: # limita a 3 entradas por médico
                    if ultimo_nif != linha[0]:
                        ultimo_nif = linha[0]
                        num_linhas_nif = 1
                        medicos.append(linha)
                        continue
                    if num_linhas_nif < 3:
                        num_linhas_nif += 1
                        medicos.append(linha)

    return jsonify(medicos), 200

def e_tempo_posterior(cursor, data, hora):
    cursor.execute(
        """
        SELECT * FROM NOW() AS aux WHERE TO_TIMESTAMP(%(tempo)s, 'YYYY-MM-DD HH24:MI:SS') > aux::timestamp;
        """,
        {"tempo": data + " " + hora}
    )
    return cursor.rowcount != 0

def verifica_args_regista_cancela(paciente, medico, data, hora):
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
    return erro

def paciente_existe(cursor, paciente):
    cursor.execute(
        """
        SELECT * FROM paciente WHERE ssn = %(paciente)s;
        """,
        {"paciente": paciente}
    )
    if cursor.rowcount == 0:
        raise Exception(f"o paciente '{paciente}' não existe")

def medico_existe(cursor, medico):
    cursor.execute(
        """
        SELECT * FROM medico WHERE nif = %(medico)s;
        """,
        {"medico": medico}
    )
    if cursor.rowcount == 0:
        raise Exception(f"o medico '{medico}' não existe")

def clinica_existe(cursor, clinica):
    cursor.execute(
        """
        SELECT * FROM clinica WHERE nome = %(clinica)s;
        """,
        {"clinica": clinica}
    )
    if cursor.rowcount == 0:
        raise Exception(f"a clinica '{clinica}' não existe")

def horario_livre(cursor, paciente, medico, data, hora):
    res = cursor.execute(
        """
        SELECT ssn, nif
        FROM consulta
        WHERE nif = %(medico)s AND data = %(data)s AND hora = %(hora)s
        UNION ALL
        SELECT ssn, nif
        FROM consulta
        WHERE ssn = %(paciente)s AND data = %(data)s and hora = %(hora)s;
        """,
        {"paciente": paciente, "medico": medico, "data": data, "hora": hora}
    ).fetchall()
    if cursor.rowcount == 0:
        return
    if cursor.rowcount == 2:
        raise Exception(f"tanto o paciente '{paciente}' como o medico '{medico}' já têm consultas marcadas no horário pedido")
    if res[0][0] == paciente:
        raise Exception(f"o paciente '{paciente}' já tem consulta marcada no horário pedido")
    raise Exception(f"o medico '{medico}' já tem consulta marcada no horário pedido")

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
    erro = verifica_args_regista_cancela(paciente, medico, data, hora)
    if erro is not None:
        return jsonify({"message": erro, "status": "error"}), 400
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            try:
                if not e_tempo_posterior(cur, data, hora):
                    return jsonify({"message": f"o horário tem de ser posterior ao atual",
                                    "status": "error"}), 400
            except Exception as e:
                return jsonify({"message": f"o horário '{str(data)} {str(hora)}' é inválido (tem de ter formato YYYY-MM-DD HH:MM:SS)",
                                "status": "error"}), 400
            try:
                with conn.transaction():
                    clinica_existe(cur, clinica)
                    paciente_existe(cur, paciente)
                    medico_existe(cur, medico)
                    horario_livre(cur, paciente, medico, data, hora)
                    cur.execute(
                        """
                        INSERT INTO consulta (ssn, nif, nome, data, hora)
                            VALUES (%(ssn)s, %(nif)s, %(nome)s, %(data)s, %(hora)s);
                        """,
                        {"ssn": paciente, "nif": medico, "nome": clinica,
                         "data": data, "hora": hora},
                    )
            except Exception as e:
                return jsonify({"message": str(e), "status": "error"}), 400
            else:
                if cur.rowcount == 0:
                    return jsonify({"message": "não foi possível marcar a consulta",
                                    "status": "error"}), 400

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
    erro = verifica_args_regista_cancela(paciente, medico, data, hora)
    if erro is not None:
        return jsonify({"message": erro, "status": "error"}), 400
    with psycopg.connect(conninfo=DATABASE_URL) as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            try:
                if not e_tempo_posterior(cur, data, hora):
                    return jsonify({"message": f"o horário tem de ser posterior ao atual",
                                    "status": "error"}), 400
            except Exception as e:
                return jsonify({"message": f"""o horário '{str(data)} {str(hora)}' é inválido (tem de ter formato YYYY-MM-DD HH:MM:SS)""",
                                "status": "error"}), 400
            try: 
                with conn.transaction():
                    clinica_existe(cur, clinica)
                    paciente_existe(cur, paciente)
                    medico_existe(cur, medico)
                    cur.execute(
                        """
                        DELETE FROM consulta
                        WHERE ssn = %(ssn)s AND nif = %(nif)s AND nome = %(nome)s
                            AND data = %(data)s AND hora = %(hora)s;
                        """,
                        {"ssn": paciente, "nif": medico, "nome": clinica,
                         "data": data, "hora": hora},
                    )
            except Exception as e:
                return jsonify({"message": str(e), "status": "error"}), 400
            else:
                if cur.rowcount == 0:
                    return jsonify({"message": "consulta não encontrada",
                                    "status": "error"}), 404

    return "", 204

@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"}), 200

if __name__ == "__main__":
    app.run()