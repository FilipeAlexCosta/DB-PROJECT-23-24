-- Como ssn é chave primária em paciente e id é chave primária em consulta,
-- não é necessário indíces nessas colunas.
-- Porém, no que toca ao parametro e valor em observacao é beneficial
-- criar um índice composto em (parametro, valor) de maneira a otimizar
-- o filtro no query, dado que passará a fazer um Index Only Scan em vez de
-- um Index Scan, o que faz melhorar o desempenho do filtro.
CREATE INDEX param_val ON observacao (parametro, valor);

-- Assumindo que o UNIQUE não cria um índice no codigo_sns em consulta,
-- devemos criar um índice para fazer mais eficientemente o join entre
-- consulta e receita.
-- De maneira a otimizar o filtro em WHERE devemos de criar um índice na coluna
-- data em consulta, de maneira a permitir operações de range eficientes pelo
-- uso de uma B-Tree.
-- Um índice na coluna especialidade em consulta também aumentará o desempenho
-- no Group By, que passa de um Sequential Scan para um Index Scan. 
CREATE INDEX codigo_sns_fk ON consulta (codigo_sns);
CREATE INDEX data_idx ON consulta (data);
CREATE INDEX especialidade_idx ON consulta (especialidade);