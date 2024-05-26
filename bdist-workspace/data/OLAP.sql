-- 1
SELECT DISTINCT
    ssn, nome
FROM
    (SELECT ssn, MAX(DATETIME(data, hora)) - MIN(DATETIME(data, hora)) AS intervalo
    FROM historial_paciente
    WHERE especialidade = 'ortopedia' AND tipo = 'observacao' AND valor IS NULL
    GROUP BY ssn, chave HAVING intervalo > 0
    )
WHERE intervalo >= ALL (
    SELECT MAX(DATETIME(data, hora)) - MIN(DATETIME(data, hora)) AS intervalo
    FROM historial_paciente
    WHERE especialidade = 'ortopedia' AND tipo = 'observacao' AND valor IS NULL
    GROUP BY ssn, chave HAVING intervalo > 0
);

-- 2
-- Determinar que medicamentos estão a ser usados para tratar doenças crónicas do foro
-- cardiológico. Considera-se que qualificam quaisquer medicamentos receitados ao mesmo
-- paciente (qualquer que ele seja) pelo menos uma vez por mês durante pelo menos doze meses
-- consecutivos, em consultas de cardiologia.
SELECT DISTINCT
    chave AS nome_medicamento
FROM
    historial_paciente h1 INNER JOIN historial_paciente h2 ON(h1.ssn = h2.ssn AND
    h1.tipo = h2.tipo AND h1.chave = h2.chave AND h1.especialidade = h2.especialidade AND
    EXTRACT(MONTH FROM (DATE(h2.ano|| '-' || h2.mes || '-01') - DATE(h1.ano|| '-' || h1.mes || '-01'))) <= 11 AND
    EXTRACT(MONTH FROM (DATE(h2.ano|| '-' || h2.mes || '-01') - DATE(h1.ano|| '-' || h1.mes || '-01'))) >= 0)
WHERE
    h1.tipo = 'receita' AND h1.especialidade = 'cardiologia'
GROUP BY
    h1.ssn, h1.chave
HAVING
    COUNT(h1.data) = 12
;

-- 3
-- Explorar as quantidades totais receitadas de cada medicamento em 2023, globalmente, e com
-- drill down nas dimensões espaço (localidade > clinica), tempo (mes > dia_do_mes), e médico
-- (especialidade > nome [do médico]), separadamente.
SELECT
    localidade, clinica, mes, dia_do_mes, especialidade, m.nome AS nome_medico, SUM(valor) AS quantidade_total
FROM
    historial_paciente h INNER JOIN medico m USING(nif)
WHERE
    tipo = 'receita' AND ano = 2023
GROUP BY GROUPING SETS
    ((localidade), (localidade, clinica),
     (mes), (mes, dia_do_mes),
     (especialidade), (especialidade, nome_medico))
; -- FALTA ACTUALLY EXTRAIR A LOCALIDADE A PARTIR DA MORADA!!!!!!!!!!!!!!!!!!!!

-- 4
-- Determinar se há enviesamento na medição de algum parâmetros entre clínicas, especialidades
-- médicas ou médicos, sendo para isso necessário listar o valor médio e desvio padrão de todos os
-- parâmetros de observações métricas (i.e. com valor não NULL) com drill down na dimensão
-- médico (globalmente > especialidade > nome [do médico]) e drill down adicional (sobre o
-- anterior) por clínica.
SELECT
    chave AS parametro, especialidade, m.nome AS nome_medico, clinica,
    AVG(valor) AS media, STDDEV(valor) AS desvio_padrao
FROM
    historial_paciente h INNER JOIN medico m USING(nif)
WHERE
    tipo = 'observacao' AND valor IS NOT NULL
GROUP BY GROUPING SETS
    ((parametro),
     (parametro,  especialidade),
     (parametro, especialidade, nome_medico),
     (parametro, especialidade, nome_medico, clinica))
;