INSERT INTO clinica VALUES 
    ('Clinic A', '123456789', '123 Main Street, City A'),
    ('Clinic B', '987654321', '456 Oak Avenue, City B');

INSERT INTO enfermeiro VALUES 
    ('123456789', 'Nurse A', '987654321', '789 Elm Street, City C', 'Clinic A'),
    ('234567890', 'Nurse B', '876543210', '567 Maple Avenue, City D', 'Clinic B'),
    ('345678901', 'Nurse C', '765432109', '345 Pine Street, City E', 'Clinic A');

INSERT INTO medico VALUES 
    ('456789012', 'Doctor A', '654321098', '234 Cedar Street, City F', 'Cardiology'), -- tmb é o paciente D
    ('567890123', 'Doctor B', '543210987', '456 Birch Avenue, City G', 'Orthopedics'),
    ('678901234', 'Doctor C', '432109876', '678 Elm Street, City H', 'Pediatrics');

-- Doctor A assignments
INSERT INTO trabalha VALUES
    ('456789012', 'Clinic A', 0),  -- Sunday
    ('456789012', 'Clinic B', 1),  -- Monday
    ('456789012', 'Clinic A', 2),  -- Tuesday
    ('456789012', 'Clinic B', 3),  -- Wednesday
    ('456789012', 'Clinic A', 4),  -- Thursday
    ('456789012', 'Clinic B', 5),  -- Friday
    ('456789012', 'Clinic A', 6);  -- Saturday

-- Doctor B assignments
INSERT INTO trabalha VALUES
    ('567890123', 'Clinic B', 0),  -- Sunday
    ('567890123', 'Clinic A', 1),  -- Monday
    ('567890123', 'Clinic B', 2),  -- Tuesday
    ('567890123', 'Clinic A', 3),  -- Wednesday
    ('567890123', 'Clinic B', 4),  -- Thursday
    ('567890123', 'Clinic A', 5),  -- Friday
    ('567890123', 'Clinic B', 6);  -- Saturday

-- Doctor C assignments
INSERT INTO trabalha VALUES
    ('678901234', 'Clinic A', 0),  -- Sunday
    ('678901234', 'Clinic B', 1),  -- Monday
    ('678901234', 'Clinic A', 2),  -- Tuesday
    ('678901234', 'Clinic B', 3),  -- Wednesday
    ('678901234', 'Clinic A', 4),  -- Thursday
    ('678901234', 'Clinic B', 5),  -- Friday
    ('678901234', 'Clinic A', 6);  -- Saturday

INSERT INTO paciente VALUES 
    ('12345678901', '123456789', 'Patient A', '987654321', '123 Elm Street, City X', '1990-05-15'),
    ('23456789012', '234567890', 'Patient B', '876543210', '456 Maple Avenue, City Y', '1985-10-20'),
    ('34567890123', '345678901', 'Patient C', '765432109', '789 Pine Street, City Z', '1978-03-25'),
    ('45678901234', '456789012', 'Patient D', '654321098', '234 Cedar Street, City W', '1995-12-10'),
    ('56789012345', '567890123', 'Patient E', '543210987', '567 Birch Avenue, City V', '1980-08-05'),
    ('67890123456', '678901234', 'Patient F', '432109876', '678 Oak Street, City U', '1992-06-30');

-- Appointments for Patient A
INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns)
    VALUES 
    ('12345678901', '456789012', 'Clinic B', '2024-05-17', '08:00', '123456789012'),
    ('12345678901', '567890123', 'Clinic B', '2024-05-18', '10:30', '234567890123'),
    ('12345678901', '678901234', 'Clinic A', '2024-05-19', '14:00', '345678901234');

-- Appointments for Patient B
INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns)
    VALUES 
    ('23456789012', '567890123', 'Clinic A', '2024-05-17', '09:30', '456789012345'),
    ('23456789012', '678901234', 'Clinic A', '2024-05-18', '11:00', '567890123456'),
    ('23456789012', '456789012', 'Clinic A', '2024-05-19', '15:00', '678901234567');

-- Appointments for Patient C
INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns)
    VALUES 
    ('34567890123', '678901234', 'Clinic B', '2024-05-17', '10:00', '789012345678'),
    ('34567890123', '456789012', 'Clinic A', '2024-05-18', '12:30', '890123456789'),
    ('34567890123', '567890123', 'Clinic B', '2024-05-19', '16:30', '901234567890');

-- Observations
INSERT INTO observacao (id, parametro, valor) VALUES 
    (15, 'Blood Pressure', 120),
    (16, 'Heart Rate', 80),
    (20, 'Blood Pressure', 130),
    (21, 'Heart Rate', 75),
    (23, 'Cough', NULL);

-- Prescriptions
INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES 
    ('123456789012', 'Paracetamol', 20),
    ('234567890123', 'Ibuprofen', 30),
    ('345678901234', 'Amoxicillin', 15);