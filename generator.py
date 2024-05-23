import random
from faker import Faker
import datetime

fake = Faker('pt_PT')

clinica_out = "clinica.txt"
enfermeiro_out = "enfermeiro.txt"
medico_out = "medico.txt"
trabalha_out = "trabalha.txt"
paciente_out = "paciente.txt"
consulta_out = "consulta.txt"
receita_out = "receita.txt"
observacao_out = "observacao.txt"
separator = ";"
endl = "\n"

def print_row(f, row):
    out = ""
    for i in range(len(row) - 1):
        out += str(row[i]) + separator
    if (len(row) > 0):
        out += str(row[len(row) - 1]) + endl
    f.write(out);

def print_table(path, table):
    with open(path, 'w') as f:
        for row in table:
            print_row(f, row)

clinicas = [("Clínica A", 213456789, "Rua A, 2750-001 Cascais"),
            ("Clinica B", 214567890, "Rua B, 1700-001 Alvalade"),
            ("Clínica C", 215678901, "Rua C, 1991-901 Oriente"),
            ("Clínica D", 216789012, "Rua D, 1249-290 Cais do Sodré"),
            ("Clínica E", 217890123, "Rua E, 2705-304 Sintra")]

print_table(clinica_out, clinicas)

enfermeiros = [('123456789', 'Enfermeiro Ana', '912345678', 'Rua das Flores, 10', 'Clinica A'),
    ('223456789', 'Enfermeiro João', '912345679', 'Avenida das Américas, 20', 'Clinica A'),
    ('323456789', 'Enfermeiro Carlos', '912345680', 'Rua dos Pioneiros, 30', 'Clinica A'),
    ('423456789', 'Enfermeiro Maria', '912345681', 'Rua do Sol, 40', 'Clinica A'),
    ('523456789', 'Enfermeiro José', '912345682', 'Avenida do Brasil, 50', 'Clinica B'),
    ('623456789', 'Enfermeiro Marta', '912345683', 'Rua da Saudade, 60', 'Clinica B'),
    ('723456789', 'Enfermeiro Pedro', '912345684', 'Rua das Acácias, 70', 'Clinica B'),
    ('823456789', 'Enfermeiro Sofia', '912345685', 'Avenida Central, 80', 'Clinica B'),
    ('923456789', 'Enfermeiro Luís', '912345686', 'Rua do Mercado, 90', 'Clinica C'),
    ('133456789', 'Enfermeiro Rita', '912345687', 'Rua das Palmeiras, 100', 'Clinica C'),
    ('233456789', 'Enfermeiro Tiago', '912345688', 'Avenida dos Anjos, 110', 'Clinica C'),
    ('333456789', 'Enfermeiro Inês', '912345689', 'Rua Nova, 120', 'Clinica C'),
    ('433456789', 'Enfermeiro Paulo', '912345690', 'Rua da Liberdade, 130', 'Clinica D'),
    ('533456789', 'Enfermeiro Clara', '912345691', 'Avenida da Paz, 140', 'Clinica D'),
    ('633456789', 'Enfermeiro Miguel', '912345692', 'Rua das Laranjeiras, 150', 'Clinica D'),
    ('733456789', 'Enfermeiro Helena', '912345693', 'Rua do Parque, 160', 'Clinica D'),
    ('833456789', 'Enfermeiro Ricardo', '912345694', 'Avenida das Nações, 170', 'Clinica E'),
    ('933456789', 'Enfermeiro Teresa', '912345695', 'Rua da Alegria, 180', 'Clinica E'),
    ('143456789', 'Enfermeiro André', '912345696', 'Rua das Pedras, 190', 'Clinica E'),
    ('243456789', 'Enfermeiro Daniela', '912345697', 'Avenida dos Navegantes, 200', 'Clinica E'),
    ('343456789', 'Enfermeiro Francisco', '912345698', 'Rua dos Jacarandás, 210', 'Clinica A'),
    ('443456789', 'Enfermeiro Patrícia', '912345699', 'Rua do Rio, 220', 'Clinica A'),
    ('543456789', 'Enfermeiro Hugo', '912345700', 'Avenida das Águas, 230', 'Clinica B'),
    ('643456789', 'Enfermeiro Raquel', '912345701', 'Rua dos Pinheiros, 240', 'Clinica B'),
    ('743456789', 'Enfermeiro Bruno', '912345702', 'Rua do Mar, 250', 'Clinica C'),
    ('843456789', 'Enfermeiro Laura', '912345703', 'Avenida dos Ventos, 260', 'Clinica C'),
    ('943456789', 'Enfermeiro Jorge', '912345704', 'Rua do Horizonte, 270', 'Clinica D'),
    ('153456789', 'Enfermeiro Carla', '912345705', 'Rua da Serra, 280', 'Clinica D'),
    ('253456789', 'Enfermeiro Diogo', '912345706', 'Avenida dos Lagos, 290', 'Clinica E'),
    ('353456789', 'Enfermeiro Vanessa', '912345707', 'Rua das Amoras, 300', 'Clinica E')]

print_table(enfermeiro_out, enfermeiros)

especialidades = ('ortopedia', 'cardiologia', 'neurologia', 'nefrologia', 'oncologia')
nomes_escolhidos = set()
nifs_escolhidos = set()
medicos = []

def gera_nome():
    return fake.name()

def gera_nome_unico(escolhidos):
    n = gera_nome()
    while n in escolhidos:
        n = gera_nome()
    escolhidos.add(n)
    return n

def gera_nif():
    return random.randint(100000000, 999999999)

def gera_nif_unico(escolhidos):
    nif = gera_nif()
    while nif in escolhidos:
        nif = gera_nif()
    escolhidos.add(nif)
    return nif

def gera_ssn():
    return random.randint(10000000000, 99999999999)

def gera_ssn_unico(escolhidos):
    ssn = gera_ssn()
    while ssn in escolhidos:
        ssn = gera_ssn()
    escolhidos.add(ssn)
    return ssn

def gera_data():
    return fake.date_between(datetime.date(1974, 1, 1), datetime.date(2004, 12, 31))

def gera_morada():
    return fake.address().replace("\n", " ")

def gera_telefone():
    return random.randint(900000000, 999999999)

def gera_medicos(count: int, especialidades):
    for _ in range(count):
        medicos.append((gera_nif_unico(nifs_escolhidos), gera_nome_unico(nomes_escolhidos), gera_telefone(), gera_morada(), random.choice(especialidades)))

gera_medicos(20, ['clínica geral'])
gera_medicos(40, especialidades)

print_table(medico_out, medicos)

nif_pool_clinica = [[[] for _ in range(7)] for _ in range(5)]
trabalha = []

for clinic in range(5):
    med_at = clinic * 12;
    for dow in range(7):
        for docs in range(12):
            trabalha.append((medicos[med_at][0], clinicas[clinic][0], dow))
            nif_pool_clinica[clinic][dow].append(medicos[med_at][0])
            med_at = (med_at + 1) % 60

print_table(trabalha_out, trabalha)

pacientes = []
ssn_escolhidos = set()
nifs_escolhidos_pac = set()
cons_pacientes = dict()

def gera_pacientes(count: int):
    for _ in range(count):
        pacientes.append((gera_ssn_unico(ssn_escolhidos), gera_nif_unico(nifs_escolhidos_pac), gera_nome(), gera_telefone(), gera_morada(), gera_data()))

gera_pacientes(5000)

print_table(paciente_out, pacientes)

def gera_data_consulta():
    dia = fake.date_between(datetime.date(2023, 1, 1), datetime.date(2023, 12, 31))
    horas = random.choice([str(random.randint(8, 13)), str(random.randint(14, 19))])
    if (int(horas) < 10):
        horas = '0' + horas
    mins = [':00:00', ':30:00']
    return str(dia) + " " + horas + random.choice(mins)

consultas = []
con_id = 0