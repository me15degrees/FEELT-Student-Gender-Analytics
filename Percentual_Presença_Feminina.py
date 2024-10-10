import pandas as pd
import matplotlib.pyplot as plt
from utils.secret import FILE_PATH
from utils.dataset import nomes_femininos, nomes_masculinos
from utils.engenharias import cursos

file_path = FILE_PATH
restante = []

percentages = {"Elétrica": {"F": 0, "M": 0, "Total_F": 0, "Total_M": 0},
               "de Controle e Automação": {"F": 0, "M": 0, "Total_F": 0, "Total_M": 0},
               "de Computação": {"F": 0, "M": 0, "Total_F": 0, "Total_M": 0},
               "Biomédica": {"F": 0, "M": 0, "Total_F": 0, "Total_M": 0},
               "Eletrônica e de Telecomunicações": {"F": 0, "M": 0, "Total_F": 0, "Total_M": 0}}

for nome_curso, codigo_curso in cursos.items():
    
    with open(FILE_PATH) as ficheiro:
        for linha in ficheiro:
            CURSO_COD, CURSO_NOME, INGRESSO_FORMA, INGRESSO_ANO, PERIODO_INGRE_ITEM, INGRESSO_PERIODO, EVASAO_FORMA, EVASAO_ANO, EVASAO_PERIODO, ALUNO_MATRICULA, ALUNO_NOME = linha.strip().split(",")

            if CURSO_COD == codigo_curso:
                
                if ALUNO_NOME.split()[0] in nomes_femininos:
                    genero = "F"
                    percentages[nome_curso]["Total_F"] += 1
                elif ALUNO_NOME.split()[0] in nomes_masculinos:
                    genero = "M"
                    percentages[nome_curso]["Total_M"] += 1
                else:
                    restante.append(ALUNO_NOME.split()[0])
                    continue

                if EVASAO_FORMA == "Aluno com Vínculo":
                    percentages[nome_curso][genero] += 1

for curso, data in percentages.items():
    data["Perc_F"] = ((data["F"] / (data["F"]+ data["M"])) * 100) 
    data["Perc_M"] = ((data["M"] / (data["F"]+ data["M"]))* 100)

plt.figure(figsize=(10, 6))

courses = list(percentages.keys())
name_courses = []
for name in courses:
    name_courses.append("Eng. "+name)
perc_feminino = [percentages[curso]["Perc_F"] for curso in courses]
perc_masculino = [percentages[curso]["Perc_M"] for curso in courses]

bar_width = 0.35
index = range(len(courses))

bars_feminino = plt.bar(index, perc_feminino, bar_width, color='lightblue')
bars_masculino = plt.bar([i + bar_width for i in index], perc_masculino, bar_width, color='lightcoral')

plt.xlabel('Cursos')
plt.ylabel('Percentual de Alunos com Vínculo nos Cursos da FEELT')
plt.title('Presença Feminina nos Cursos da FEELT (entre 2019 e 2024)')
plt.xticks([i + bar_width / 2 for i in index], name_courses, rotation=10)
plt.legend()

for bar in bars_feminino:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')

for bar in bars_masculino:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('images/Percentual_Vínculo_Gênero.png', dpi=300, bbox_inches='tight')

print("Graph generated successfully!")
