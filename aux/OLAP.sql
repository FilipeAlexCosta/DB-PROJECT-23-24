%%sql
-- SELECT ...
SELECT DISTINCT
    res.ssn
FROM
    (SELECT h.ssn, (MAX(h.data) - MIN(h.data)) AS intervalo
    FROM historial_paciente h INNER JOIN consulta c USING(id)
    WHERE h.especialidade = 'ortopedia' AND h.tipo = 'observacao' AND h.valor IS NULL
    GROUP BY h.ssn, h.chave HAVING (MAX(h.data) - MIN(h.data)) > INTERVAL '0') AS res
WHERE res.intervalo >= ALL (
    SELECT (MAX(h.data) - MIN(h.data))
    FROM historial_paciente h INNER JOIN consulta c USING(id)
    WHERE h.especialidade = 'ortopedia' AND h.tipo = 'observacao' AND h.valor IS NULL
    GROUP BY h.ssn, h.chave HAVING (MAX(h.data) - MIN(h.data)) > INTERVAL '0'
);

Determinar que medicamentos estão a ser usados para tratar doenças crónicas do foro
cardiológico. Considera-se que qualificam quaisquer medicamentos receitados ao mesmo
paciente (qualquer que ele seja) pelo menos uma vez por mês durante os últimos doze meses, em consultas de cardiologia

%%sql
-- SELECT ...
SELECT DISTINCT
    chave AS nome_medicamento
FROM
    historial_paciente
WHERE
    h1.tipo = 'receita' AND h1.especialidade = 'cardiologia'
    AND (12 * (EXTRACT(YEAR FROM CURRENT_DATE()) - ano) + 
      (EXTRACT(MONTH FROM CURRENT_DATE()) - mes)) BETWEEN 0 AND 11
GROUP BY
    ssn, chave
HAVING
    COUNT(data) >= 12
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