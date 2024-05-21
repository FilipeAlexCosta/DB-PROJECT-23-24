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