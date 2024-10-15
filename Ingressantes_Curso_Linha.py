import pandas as pd
import matplotlib.pyplot as plt
from utils.secret import FILE_PATH
from utils.dataset import nomes_femininos, nomes_masculinos
from utils.engenharias import cursos

file_path = FILE_PATH
restante = []

years = range(2019, 2025)


data = {curso: {year: {"Total": 0, "F": 0, "M": 0} for year in years} for curso in cursos}

with open(FILE_PATH) as ficheiro:
    next(ficheiro) 
    for linha in ficheiro:
        CURSO_COD, CURSO_NOME, INGRESSO_FORMA, INGRESSO_ANO, PERIODO_INGRE_ITEM, INGRESSO_PERIODO, EVASAO_FORMA, EVASAO_ANO, EVASAO_PERIODO, ALUNO_MATRICULA, ALUNO_NOME = linha.strip().split(",")

        try:
            INGRESSO_ANO = int(INGRESSO_ANO)
        except ValueError:
            continue 
        if INGRESSO_ANO in years:
            if CURSO_COD in cursos.values():
                nome_curso = [key for key, value in cursos.items() if value == CURSO_COD][0]

                if ALUNO_NOME.split()[0] in nomes_femininos:
                    data[nome_curso][INGRESSO_ANO]["F"] += 1
                elif ALUNO_NOME.split()[0] in nomes_masculinos:
                    data[nome_curso][INGRESSO_ANO]["M"] += 1

                data[nome_curso][INGRESSO_ANO]["Total"] += 1

percentuais = {curso: {} for curso in cursos}
for curso, anos in data.items():
    for ano, stats in anos.items():
        total = stats["Total"]
        if total > 0:
            stats["Perc_F"] = (stats["F"] / total) * 100
        else:
            stats["Perc_F"] = 0

        percentuais[curso][ano] = stats["Perc_F"]


for curso, anos in percentuais.items():
    plt.figure(figsize=(10, 6))

    anos_plot = list(anos.keys())
    percentuais_femininas = list(anos.values())


    plt.plot(anos_plot, percentuais_femininas, marker='o', label="Percentual de Ingressantes Femininas", color="#384B70")


    for i, (year, percentage) in enumerate(zip(anos_plot, percentuais_femininas)):
        plt.text(year, percentage + 0.5, f"{percentage:.2f}%", ha='center', va='bottom', fontsize=10)

    plt.xlabel('Ano de Ingresso')
    plt.ylabel('Percentual de Ingressantes Femininas (%)')
    plt.title(f"Percentual de Ingressantes Femininas por Ano no Curso de Eng. {curso}")
    plt.xticks(anos_plot)  
    plt.ylim(0, 100)  
    plt.axhline(50, color='grey', linestyle='--', linewidth=0.8, label='50% de Ingressantes Femininas')  
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'images/Ingressantes_Linha/Percentual_Ingressantes_Femininas_Temporal_{curso}.png', dpi=300, bbox_inches='tight')

print("Gráficos gerados com sucesso!")
