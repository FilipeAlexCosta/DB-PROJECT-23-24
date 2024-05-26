%%sql
-- SELECT ...
SELECT DISTINCT
    res.ssn
FROM
    (SELECT h.ssn, (MAX(h.data + c.hora) - MIN(h.data + c.hora)) AS intervalo
    FROM historial_paciente h INNER JOIN consulta c USING(id)
    WHERE h.especialidade = 'ortopedia' AND h.tipo = 'observacao' AND h.valor IS NULL
    GROUP BY h.ssn, h.chave HAVING (MAX(h.data + c.hora) - MIN(h.data + c.hora)) > INTERVAL '0') AS res
WHERE res.intervalo >= ALL (
    SELECT (MAX(h.data + c.hora) - MIN(h.data + c.hora))
    FROM historial_paciente h INNER JOIN consulta c USING(id)
    WHERE h.especialidade = 'ortopedia' AND h.tipo = 'observacao' AND h.valor IS NULL
    GROUP BY h.ssn, h.chave HAVING (MAX(h.data + c.hora) - MIN(h.data + c.hora)) > INTERVAL '0'
);

%%sql
-- SELECT ...
SELECT DISTINCT
    h1.chave AS nome_medicamento
FROM
    historial_paciente h1 INNER JOIN historial_paciente h2 ON(h1.ssn = h2.ssn AND
    h1.tipo = h2.tipo AND h1.chave = h2.chave AND h1.especialidade = h2.especialidade AND
    ((12 * (h2.ano - h1.ano) + (h2.mes - h1.mes)) BETWEEN 0 AND 11))
WHERE
    h1.tipo = 'receita' AND h1.especialidade = 'cardiologia'
GROUP BY
    h1.ssn, h1.chave
HAVING
    COUNT(h1.data) = 12
;

%%sql
-- SELECT ...
SELECT
    SUBSTRING(localidade FROM '[0-9]{4}-[0-9]{3} (.+)$') AS localidade, h.nome, mes, dia_do_mes, h.especialidade, m.nome AS nome_medico, SUM(valor) AS quantidade_total
FROM
    historial_paciente h INNER JOIN medico m USING(nif)
WHERE
    tipo = 'receita' AND ano = 2023
GROUP BY GROUPING SETS
    ((SUBSTRING(localidade FROM '[0-9]{4}-[0-9]{3} (.+)$')), (SUBSTRING(localidade FROM '[0-9]{4}-[0-9]{3} (.+)$'), h.nome),
     (mes), (mes, dia_do_mes),
     (h.especialidade), (h.especialidade, nome_medico))
;

%%sql
-- SELECT ...
SELECT
    chave AS parametro, h.especialidade, m.nome AS nome_medico, h.nome,
    AVG(valor) AS media, STDDEV(valor) AS desvio_padrao
FROM
    historial_paciente h INNER JOIN medico m USING(nif)
WHERE
    tipo = 'observacao' AND valor IS NOT NULL
GROUP BY GROUPING SETS
    ((parametro),
     (parametro,  h.especialidade),
     (parametro, h.especialidade, nome_medico),
     (parametro, h.especialidade, nome_medico, h.nome))
ORDER BY parametro, especialidade, nome_medico, nome
;