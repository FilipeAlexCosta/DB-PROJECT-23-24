SELECT mt.nif, d.data
FROM (SELECT nif, dia_da_semana FROM clinica
    INNER JOIN trabalha USING(nome) INNER JOIN medico USING(nif)
    WHERE especialidade = %(especialidade)s AND nome = %(nome)s) AS mt
    INNER JOIN datas d ON(EXTRACT(dow FROM d.data) = mt.dia_da_semana)
    LEFT OUTER JOIN consulta c ON(mt.nif = c.nif AND d.data = c.data AND d.hora = c.hora)
WHERE c.id IS NULL
ORDER BY mt.nif, d.data
