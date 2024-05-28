-- 1
%%sql
REFRESH MATERIALIZED VIEW historial_paciente;
SELECT DISTINCT ssn
FROM historial_paciente
WHERE especialidade = 'ortopedia' AND tipo = 'observacao' AND valor IS NULL
GROUP BY ssn, chave
HAVING MAX(data) - MIN(data) >= ALL (
    SELECT MAX(data) - MIN(data)
    FROM historial_paciente
    WHERE especialidade = 'ortopedia' AND tipo = 'observacao' AND valor IS NULL
    GROUP BY ssn, chave
);

-- 2
%%sql
REFRESH MATERIALIZED VIEW historial_paciente;
SELECT DISTINCT chave AS medicamento
FROM historial_paciente
WHERE especialidade = 'cardiologia' AND tipo = 'receita' AND
    (12 * (EXTRACT(YEAR FROM NOW()::date) - ano) + (EXTRACT(MONTH FROM NOW()::date) - mes)) BETWEEN 0 AND 11
GROUP BY ssn, chave
HAVING COUNT(data) >= 12;


-- 3
%%sql
REFRESH MATERIALIZED VIEW historial_paciente;
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