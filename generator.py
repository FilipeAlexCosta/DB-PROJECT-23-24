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
            ("Clínica B", 214567890, "Rua Almirante Gago Coutinho, 1885-003 Moscavide"),
            ("Clínica C", 215678901, "Rua do Bom Sucesso, 2695-109 Bobadela"),
            ("Clínica D", 216789012, "Praceta Miguel Torga, 2695-006 Bobadela"),
            ("Clínica E", 217890123, "Rua Rainha Dona Amélia, 2675-287 Odivelas")]

print_table(clinica_out, clinicas)

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

enf_nif_escolhido = deepcopy(nifs_escolhidos)
enf_nome_escolhido = set()
enfermeiros = []

for i in range(5):
    for j in range(6):
        enfermeiros.append((gera_nif_unico(enf_nif_escolhido), gera_nome_unico(enf_nome_escolhido), gera_telefone(), gera_morada(), clinicas[i][0]))
        
print_table(enfermeiro_out, enfermeiros)

nif_pool_clinica = [[[] for _ in range(7)] for _ in range(5)]
trabalha = []

for clinic in range(5):
    med_at = clinic * 12
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
end_date = datetime.date(2024, 12, 31)
current_date = start_date
paciente = 0
while current_date <= end_date:
    for clinic in range(len(clinicas)):
        for nif in nif_pool_clinica[clinic][(current_date.weekday() + 1) % 7]:
            if pacientes[paciente][0] == nif:
                print("ERRO: Há um médico com autoconsulta")
            hora1 = gera_hora_consulta()
            consultas.append([pacientes[paciente][0], nif, clinicas[clinic][0], current_date, hora1, ''])
            paciente = (paciente + 1) % 5000
            hora2 = gera_hora_consulta()
            while hora1 == hora2:
                hora2 = gera_hora_consulta()
            consultas.append([pacientes[paciente][0], nif, clinicas[clinic][0], current_date, hora2, ''])
            paciente = (paciente + 1) % 5000
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
rec_pos = 0
for consulta in range(len(consultas)):
    if consultas[consulta][3] >= datetime.date.today():
        break
    rec_pos += 1
    if not (1 == random.randint(1, 5)):
        rec_geradas += 1
        consultas[consulta][5] = gera_codigo_sns(codigos_sns)
        gera_receita(consultas[consulta][5])
        
print_table(consulta_out, consultas)

print(f"Aproximadamente {rec_geradas / (float) (rec_pos) * 100}% das consultas têm receita (target: 80%)")

print_table(receita_out, receitas)

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

def gera_observacao(id_consulta):
    sintomas = random.randint(1, 5)
    metricas = random.randint(0, 3)
    escolhidos = set()
    for _ in range(sintomas):
        observacoes.append((id_consulta, gera_sintoma(escolhidos), ''))
    for _ in range(metricas):
        param = gera_parametro(escolhidos)
        observacoes.append((id_consulta, param[0], param[1]))

for consulta in range(len(consultas)):
    if consultas[consulta][3] >= datetime.date.today():
        break
    gera_observacao(consulta + 1)

print_table(observacao_out, observacoes)