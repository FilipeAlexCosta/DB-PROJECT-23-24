import random
from faker import Faker
from copy import deepcopy
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

clinicas = [("Clínica A", 213456789, "Rua Vasco da Gama, 1885-007 Moscavide"),
            ("Clinica B", 214567890, "Rua Almirante Gago Coutinho, 1885-003 Moscavide"),
            ("Clínica C", 215678901, "Rua do Bom Sucesso, 2695-109 Bobadela"),
            ("Clínica D", 216789012, "Praceta Miguel Torga, 2695-006 Bobadela"),
            ("Clínica E", 217890123, "Rua Rainha Dona Amélia, 2675-287 Odivelas")]

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

# Teste 5.1
medicos.append(("510510510", "Nicolau Junior", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "ortopedia"))
nifs_escolhidos.add(510510510)
nomes_escolhidos.add('Nicolau Junior')


gera_medicos(20, ['clínica geral'])
gera_medicos(40, especialidades)

enf_nif_escolhido = deepcopy(nifs_escolhidos)
enf_nome_escolhido = set()
enfermeiros = []

for i in range(5):
    for j in range(6):
        enfermeiros.append((gera_nif_unico(enf_nif_escolhido), gera_nome_unico(enf_nome_escolhido), gera_telefone(), gera_morada(), clinicas[i][0]))
        

nif_pool_clinica = [[[] for _ in range(7)] for _ in range(5)]
trabalha = []

# Teste 5.1
trabalha.append(("510510510", "Clínica A", "0"))

for clinic in range(5):
    med_at = clinic * 12
    for dow in range(7):
        for docs in range(12):
            if med_at == 0: # medico do 5.1
                continue
            trabalha.append((medicos[med_at][0], clinicas[clinic][0], dow))
            nif_pool_clinica[clinic][dow].append(medicos[med_at][0])
            med_at = (med_at + 1) % 60

pacientes = []
ssn_escolhidos = set()
nifs_escolhidos_pac = set()
cons_pacientes = dict()

def gera_pacientes(count: int):
    for _ in range(count):
        pacientes.append((gera_ssn_unico(ssn_escolhidos), gera_nif_unico(nifs_escolhidos_pac), gera_nome(), gera_telefone(), gera_morada(), gera_data()))

# Teste 5.1
pacientes.append(("05151515151", "051515151", "Osvaldo", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "2003-10-20"))
ssn_escolhidos.add("05151515151")
nifs_escolhidos_pac.add("051515151")

pacientes.append(("51515151510", "515151510", "Osvaldo Junior", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "2003-10-20"))
ssn_escolhidos.add("51515151510")
nifs_escolhidos_pac.add("515151510")

pacientes.append(("15151515150", "151515151", "Osvaldo Junior", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "2003-10-20"))
ssn_escolhidos.add("15151515150")
nifs_escolhidos_pac.add("151515151")

pacientes.append(("05151515100", "151515100", "Osvaldo Avô", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "2003-10-20"))
ssn_escolhidos.add("05151515100")
nifs_escolhidos_pac.add("151515100")

gera_pacientes(5000)

def gera_hora_consulta():
    horas = random.choice([str(random.randint(8, 12)), str(random.randint(14, 18))])
    if (int(horas) < 10):
        horas = '0' + horas
    mins = [':00:00', ':30:00']
    minutos = random.choice(mins)
    return horas + minutos

def gera_codigo_sns(escolhidos):
    codigo = random.randint(100000000000, 999999999999)
    while codigo in escolhidos:
        codigo = random.randint(100000000000, 999999999999)
    escolhidos.add(codigo)
    return codigo

consultas = []
codigos_sns = set()

start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)
current_date = start_date
paciente = 4 # anteriores sao para testar 5.1

consultas.append((0, "05151515151", "510510510", "Clínica A", "2023-01-01", "08:00:00", gera_codigo_sns(codigos_sns)))
consultas.append((1, "05151515151", "510510510", "Clínica A", "2023-06-04", "08:00:00", gera_codigo_sns(codigos_sns)))

consultas.append((2, "51515151510", "510510510", "Clínica A", "2023-01-01", "09:00:00", gera_codigo_sns(codigos_sns)))
consultas.append((3, "51515151510", "510510510", "Clínica A", "2023-12-03", "08:00:00", gera_codigo_sns(codigos_sns)))

consultas.append((6, "15151515150", "510510510", "Clínica A", "2023-01-01", "09:30:00", gera_codigo_sns(codigos_sns)))
consultas.append((7, "15151515150", "510510510", "Clínica A", "2023-12-03", "09:00:00", gera_codigo_sns(codigos_sns)))

consultas.append((4, "05151515100", "510510510", "Clínica A", "2023-01-01", "10:00:00", gera_codigo_sns(codigos_sns)))
consultas.append((5, "05151515100", "510510510", "Clínica A", "2023-03-05", "08:00:00", gera_codigo_sns(codigos_sns)))

id = 8
while current_date <= end_date:
    for clinic in range(len(clinicas)):
        for nif in nif_pool_clinica[clinic][(current_date.weekday() + 1) % 7]:
            if nif == 510510510: # medico para o 5.1
                continue
            if pacientes[paciente][0] == nif:
                print("ERRO: Há um médico com autoconsulta")
            hora1 = gera_hora_consulta()
            consultas.append((id, pacientes[paciente][0], nif, clinicas[clinic][0], current_date, hora1, gera_codigo_sns(codigos_sns)))
            paciente = (paciente + 1) % 5000
            id += 1
            if paciente < 4:
                paciente = 4
                continue
            hora2 = gera_hora_consulta()
            while hora1 == hora2:
                hora2 = gera_hora_consulta()
            consultas.append((id, pacientes[paciente][0], nif, clinicas[clinic][0], current_date, hora2, gera_codigo_sns(codigos_sns)))
            paciente = (paciente + 1) % 5000
            id += 1
            if paciente < 4:
                paciente = 4
                continue
    current_date += datetime.timedelta(days=1)

receitas = []
medicamentos_disp = [
    "Prozac",
    "Lipitor",
    "Zoloft",
    "Metformin",
    "Advil",
    "Xanax",
    "Amoxicillin",
    "Tylenol",
    "Prednisone",
    "Gabapentin",
    "Viagra",
    "Lisinopril",
    "Adderall",
    "Ciprofloxacin",
    "Celexa",
    "Ativan",
    "Plavix",
    "Albuterol",
    "Ambien",
    "Risperdal",
    "Crestor",
    "Prilosec",
    "Synthroid",
    "Nexium",
    "Paxil",
    "Flonase",
    "Vicodin",
    "Percocet",
    "Cialis",
    "Flexeril",
    "Wellbutrin",
    "Cymbalta",
    "Dilantin",
    "Imitrex",
    "Claritin",
    "OxyContin",
    "Seroquel",
    "Remeron",
    "Klonopin",
    "Clindamycin",
    "Tramadol",
    "Suboxone",
    "Concerta",
    "Neurontin",
    "Lamictal",
    "Topamax",
    "Valium",
    "Depakote",
    "Zyrtec",
    "Effexor",
    "Ambien",
    "Singulair",
    "Levaquin",
    "Celebrex",
    "Allegra",
    "Lyrica",
    "Zofran",
    "Prilosec",
    "Zantac",
    "Lunesta",
    "Ritalin",
    "Klonopin",
    "Wellbutrin",
    "Symbicort",
    "Strattera",
    "Pravachol",
    "Fosamax",
    "Elavil",
    "Boniva",
    "Lunesta",
    "OxyContin",
    "Suboxone",
    "Cymbalta",
    "Lexapro",
    "Lamictal",
    "Nasonex",
    "Vyvanse",
    "Geodon",
    "Lyrica",
    "Protonix",
    "Namenda",
    "Aricept",
    "Crestor",
    "Adderall",
    "Ambien",
    "Claritin",
    "Singulair",
    "Xanax",
    "Effexor",
    "Zoloft",
    "Ativan",
    "Zantac",
    "Paxil",
    "Tricor",
    "Prozac",
    "Neurontin",
    "Diovan",
    "Plavix",
    "Klonopin",
    "Tramadol"
]

def gera_medicamento(escolhidos):
    medicamento = random.choice(medicamentos_disp)
    while medicamento in escolhidos:
        medicamento = random.choice(medicamentos_disp)
    escolhidos.add(medicamento)
    return medicamento

def gera_receita(codigo_sns):
    quant = random.randint(1, 6)
    medicamentos = set()
    for _ in range(quant):
        receitas.append((codigo_sns, gera_medicamento(medicamentos), random.randint(1, 3)))

rec_geradas = 0
for consulta in consultas:
    if not (1 == random.randint(1, 5)):
        rec_geradas += 1
        gera_receita(consulta[6])
        

print(f"Aproximadamente {rec_geradas / (float) (len(consultas)) * 100}% das consultas têm receita (target: 80%)")

observacoes = []

sintomas_disp = [
        "dor de cabeça",
        "náusea",
        "vômito",
        "tontura",
        "fadiga",
        "febre",
        "calafrios",
        "diarreia",
        "constipação",
        "dor de garganta",
        "tosse",
        "dor no peito",
        "falta de ar",
        "coriza",
        "perda de apetite",
        "perda de peso",
        "sudorese",
        "dor nas costas",
        "dor abdominal",
        "dor nas articulações",
        "dor muscular",
        "inchaço",
        "vermelhidão",
        "coceira",
        "dor no ouvido",
        "visão embassada",
        "sensibilidade à luz",
        "zumbido",
        "dificuldade de concentração",
        "dificuldade de memória",
        "irritabilidade",
        "ansiedade",
        "depressão",
        "insônia",
        "sonolência",
        "alterações no paladar",
        "alterações no olfato",
        "dor nos olhos",
        "olhos vermelhos",
        "olhos secos",
        "inchaço nos olhos",
        "sangramento nasal",
        "dificuldade de engolir",
        "rouquidão",
        "dor no peito",
        "batimentos cardíacos irregulares",
        "pressão arterial alta",
        "pressão arterial baixa"
    ]

observacoes_disp = [
        "temperatura corporal",
        "pressao arterial sistolica",
        "pressao arterial diastolica",
        "frequencia cardiaca",
        "frequencia respiratoria",
        "saturacao oxigenio",
        "glicemia",
        "hemoglobina",
        "hematocrito",
        "plaquetas",
        "leucocitos",
        "creatinina",
        "colesterol total",
        "triglicerideos",
        "hdl colesterol",
        "ldl colesterol",
        "glicose",
        "insulina",
        "hormonio tireoide"
    ]


def gera_sintoma(escolhidos):
    sintoma = random.choice(sintomas_disp)
    while sintoma in escolhidos:
        sintoma = random.choice(sintomas_disp)
    escolhidos.add(sintoma)
    return sintoma

def gera_parametro(escolhidos):
    param = random.choice(observacoes_disp)
    while param in escolhidos:
        param = random.choice(observacoes_disp)
    escolhidos.add(param)
    return (param, random.uniform(0.1, 100))

def gera_observacao(id):
    sintomas = random.randint(1, 5)
    metricas = random.randint(0, 3)
    escolhidos = set()
    for _ in range(sintomas):
        observacoes.append((id, gera_sintoma(escolhidos), ''))
    for _ in range(metricas):
        param = gera_parametro(escolhidos)
        observacoes.append((id, param[0], param[1]))


observacoes.append((0, "dor na canela", ''))
observacoes.append((1, "dor na canela", ''))

observacoes.append((2, "dor na canelona", ''))
observacoes.append((3, "dor na canelona", ''))

observacoes.append((4, "dor na canelonaa", ''))
observacoes.append((5, "dor na canelonaa", ''))

observacoes.append((6, "dor na canelonaa2", ''))
observacoes.append((7, "dor na canelonaa2", ''))

i = 0
for consulta in consultas:
    if (i < 8):
        i += 1
        continue
    gera_observacao(consulta[0])


# TEST 5.1
# Determinar que paciente(s) tiveram menos progresso no tratamento das suas doenças do foro
# ortopédico para atribuição de uma consulta gratuita. Considera-se que o indicador de falta de
# progresso é o intervalo temporal máximo entre duas observações do mesmo sintoma (i.e.
# registos de tipo ‘observacao’ com a mesma chave e com valor NULL) em consultas de ortopedia

# Usar 3 pacientes:
# pacientes.append(("05151515151", "051515151", "Osvaldo", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "2003-10-20"))
# pacientes.append(("51515151510", "515151510", "Osvaldo Junior", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "2003-10-20"))
# pacientes.append(("05151515100", "151515100", "Osvaldo Avô", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "2003-10-20"))

# Médico a usar:
# medicos.append(("510510510", "Nicolau Junior", "999999999", "Av. Rovisco Pais, 1 1049-001 Lisboa", "ortopedia"))

# Clinica a usar: Clinica A, dow-0 (dom)
# trabalha.append(("510510510", "Clínica A", "0"))

#Consultas: fazer pares de consultas para cada 1
# consultas.append((id, "05151515151", "510510510", "Clínica A", "2023-01-01", "08:00:00", gera_codigo_sns(codigos_sns)))
# consultas.append((id+1, "05151515151", "510510510", "Clínica A", "2023-12-03", "08:00:00", gera_codigo_sns(codigos_sns)))

# consultas.append((id+2, "51515151510", "510510510", "Clínica A", "2023-01-01", "08:00:00", gera_codigo_sns(codigos_sns)))
# consultas.append((id+3, "51515151510", "510510510", "Clínica A", "2023-06-04", "08:00:00", gera_codigo_sns(codigos_sns)))

# consultas.append((id+4, "05151515100", "510510510", "Clínica A", "2023-01-01", "08:00:00", gera_codigo_sns(codigos_sns)))
# consultas.append((id+5, "05151515100", "510510510", "Clínica A", "2023-03-05", "08:00:00", gera_codigo_sns(codigos_sns)))

#observações:
# observacoes.append((id, "dor na canela", ''))
# observacoes.append((id+1, "dor na canela"))

# observacoes.append((id+2, "dor na canelona", ''))
# observacoes.append((id+3, "dor na canelona", ''))

# observacoes.append((id+4, "dor na canelonaa", ''))
# observacoes.append((id+5, "dor na canelonaa", ''))


## PRINT TABLES ##

print_table(clinica_out, clinicas)
print_table(medico_out, medicos)
print_table(enfermeiro_out, enfermeiros)
print_table(trabalha_out, trabalha)
print_table(paciente_out, pacientes)
print_table(consulta_out, consultas)
print_table(receita_out, receitas)
print_table(observacao_out, observacoes)