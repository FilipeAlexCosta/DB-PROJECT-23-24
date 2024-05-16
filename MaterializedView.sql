CREATE MATERIALIZED VIEW IF NOT EXISTS historial_paciente AS
    SELECT
        con.id AS id, con.ssn AS ssn, con.nif AS nif, con.nome AS nome, con.data AS data,
        EXTRACT(YEAR FROM con.data) AS ano, EXTRACT(MONTH FROM con.data) AS mes, EXTRACT(DAY FROM con.data) AS dia_do_mes,
        cli.morada AS localidade,
        med.especialidade AS especialidade,
        'observacao' AS tipo,
        obs.parametro AS chave,
        obs.valor AS valor
    FROM
        consulta con INNER JOIN clinica cli ON con.nome = cli.nome
        INNER JOIN medico med ON con.nif = med.nif 
        INNER JOIN observacao obs ON con.id = obs.id
    UNION
    SELECT
        con.id AS id, con.ssn AS ssn, con.nif AS nif, con.nome AS nome, con.data AS data,
        EXTRACT(YEAR FROM con.data) AS ano, EXTRACT(MONTH FROM con.data) AS mes, EXTRACT(DAY FROM con.data) AS dia_do_mes,
        cli.morada AS localidade,
        med.especialidade AS especialidade,
        'receita' AS tipo,
        rec.medicamento AS chave,
        rec.quantidade AS valor
    FROM
        consulta con INNER JOIN clinica cli ON con.nome = cli.nome
        INNER JOIN medico med ON con.nif = med.nif 
        INNER JOIN receita rec ON con.codigo_sns = con.codigo_sns;





CREATE MATERIALIZED VIEW IF NOT EXISTS historial_paciente AS
    SELECT
        con.id AS id, con.ssn AS ssn, con.nif AS nif, con.nome AS nome, con.data AS data,
        EXTRACT(YEAR FROM con.data) AS ano, EXTRACT(MONTH FROM con.data) AS mes, EXTRACT(DAY FROM con.data) AS dia_do_mes,
        cli.morada AS localidade,
        med.especialidade AS especialidade,
        CASE
            WHEN obs.id IS NOT NULL THEN 'observacao'
            ELSE 'receita'
        END AS tipo,
        CASE
            WHEN obs.parametro IS NOT NULL THEN obs.parametro
            ELSE rec.medicamento
        END AS chave,
        CASE
            WHEN obs.valor IS NOT NULL THEN obs.valor
            ELSE rec.quantidade
        END AS valor
    FROM
        consulta con INNER JOIN clinica cli ON con.nome = cli.nome
        INNER JOIN medico med ON con.nif = med.nif
        LEFT OUTER JOIN observacao obs ON con.id = obs.id
        LEFT OUTER JOIN receita rec ON rec.codigo_sns.= med.codigo_sns;
            

