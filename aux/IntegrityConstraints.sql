ALTER TABLE consulta ADD CONSTRAINT verifica_hora
	CHECK(EXTRACT(SECOND FROM hora) = 0	AND
		(EXTRACT(MINUTE FROM hora) = 0 OR EXTRACT(MINUTE FROM hora) = 30) AND
		(hora BETWEEN '08:00:00' AND '12:30:00' OR hora BETWEEN '14:00:00' AND '18:30:00'));

CREATE OR REPLACE FUNCTION verifica_auto_consulta() RETURNS TRIGGER AS
$$
BEGIN
	IF NEW.nif = (SELECT nif FROM paciente WHERE ssn = NEW.ssn) THEN
		RAISE EXCEPTION 'O médico % não pode consultar-se a si próprio.', NEW.nif;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER proibe_auto_consulta BEFORE INSERT OR UPDATE ON consulta
	FOR EACH ROW EXECUTE FUNCTION verifica_auto_consulta();

CREATE OR REPLACE FUNCTION verifica_local_trabalho() RETURNS TRIGGER AS
$$
BEGIN
	IF NEW.nome != (SELECT nome FROM trabalha WHERE nif = NEW.nif
		AND dia_da_semana = EXTRACT(DOW FROM NEW.data)) THEN
		RAISE EXCEPTION 'O médico % não trabalha na clínica % no dia %',
			NEW.nif, NEW.nome, NEW.data;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER proibe_consultas_fora_clinica BEFORE INSERT OR UPDATE ON consulta
	FOR EACH ROW EXECUTE FUNCTION verifica_local_trabalho();
