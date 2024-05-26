"""
SELECT mt.nif, d.data
FROM (SELECT nif, dia_da_semana FROM clinica
INNER JOIN trabalha USING(nome) INNER JOIN medico USING(nif)
WHERE especialidade = %(especialidade)s AND nome = %(nome)s) AS mt
INNER JOIN datas d ON(EXTRACT(dow FROM d.data) = mt.dia_da_semana)
LEFT OUTER JOIN consulta c ON(mt.nif = c.nif AND d.data = c.data AND d.hora = c.hora)
WHERE c.id IS NULL
ORDER BY mt.nif, d.data
LIMIT 3;
"""

SELECT
    m.nif AS nif, d.data AS data, d.hora AS hora
FROM
    medico m INNER JOIN (
        SELECT t.nif, d.data, d.hora
        FROM trabalha t INNER JOIN datas d
        ON(EXTRACT(dow FROM d.data) = t.dia_da_semana)
        LEFT OUTER JOIN consulta c ON(t.nif = c.nif AND d.data = c.data AND d.hora = c.hora)
        WHERE t.nif = m.nif AND c.id IS NULL
        ORDER BY d.data, d.hora
        LIMIT 3
    ) ON(m.nif = t.nif)
WHERE
    m.especialidade = %(especialidade)s
ORDER BY m.nif, d.data, d.hora;

SELECT mt.nif, d.data
FROM medico m INNER JOIN (SELECT nif, dia_da_semana FROM clinica
INNER JOIN trabalha USING(nome) INNER JOIN medico USING(nif)
WHERE especialidade = %(especialidade)s AND nome = %(nome)s) AS mt
INNER JOIN datas d ON(EXTRACT(dow FROM d.data) = mt.dia_da_semana)
LEFT OUTER JOIN consulta c ON(mt.nif = c.nif AND d.data = c.data AND d.hora = c.hora)
WHERE c.id IS NULL
ORDER BY d.data, d.hora
LIMIT 3) ON (m.nif = mt.nif)
ORDER BY mt.nif, d.data, d.hora;

WITH aux AS (SELECT mt.nif AS nif, d.data AS data, d.hora AS hora
FROM (SELECT nif, dia_da_semana FROM clinica
INNER JOIN trabalha USING(nome) INNER JOIN medico USING(nif)
WHERE especialidade = %(especialidade)s AND nome = %(nome)s) AS mt
INNER JOIN datas d ON(EXTRACT(dow FROM d.data) = mt.dia_da_semana)
LEFT OUTER JOIN consulta c ON(mt.nif = c.nif AND d.data = c.data AND d.hora = c.hora)
WHERE c.id IS NULL)

SELECT a1.nif AS NIF, a1.data AS DATA, a1.hora AS hora
FROM aux a1 INNER JOIN aux a2 ON(a1.nif = a2.nif AND a1.data >= a2.data AND a1.hora >= a2.hora)
GROUP BY a1.nif, a1.data, a1.hora HAVING COUNT(*) <= 3