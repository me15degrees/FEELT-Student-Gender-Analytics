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
        
        INGRESSO_ANO = int(INGRESSO_ANO)
        if INGRESSO_ANO in years:

            if CURSO_COD in cursos.values():
                nome_curso = [key for key, value in cursos.items() if value == CURSO_COD][0]
                
                if ALUNO_NOME.split()[0] in nomes_femininos:
                    genero = "F"
                    data[nome_curso][INGRESSO_ANO]["F"] += 1
                elif ALUNO_NOME.split()[0] in nomes_masculinos:
                    genero = "M"
                    data[nome_curso][INGRESSO_ANO]["M"] += 1
                else:
                    restante.append(ALUNO_NOME.split()[0])
                    continue

                data[nome_curso][INGRESSO_ANO]["Total"] += 1

for curso, anos in data.items():
    for ano, stats in anos.items():
        total = stats["Total"]
        if total > 0:
            stats["Perc_F"] = (stats["F"] / total) * 100
            stats["Perc_M"] = (stats["M"] / total) * 100
        else:
            stats["Perc_F"] = 0
            stats["Perc_M"] = 0

for curso, anos in data.items():
    plt.figure(figsize=(10, 6))
    
    ingressantes_femininas = [stats["F"] for year, stats in anos.items()]
    ingressantes_totais = [stats["Total"] for year, stats in anos.items()]
    percentual_feminino = [stats["Perc_F"] for year, stats in anos.items()]
    
    anos_plot = list(anos.keys())

    plt.bar(anos_plot, ingressantes_totais, label="Total de Ingressantes", color="#7E60BF", alpha=0.7)
    plt.bar(anos_plot, ingressantes_femininas, label="Ingressantes Femininas", color="#433878", alpha=0.7)


    for i, year in enumerate(anos_plot):
        plt.text(year, ingressantes_femininas[i] + 0.5, f"{percentual_feminino[i]:.2f}%", ha='center', va='bottom')
    
    plt.xlabel('Ano de Ingresso')
    plt.ylabel('Número de Ingressantes')
    plt.title(f"Ingressantes Femininas e Percentual por Ano no Curso de Eng. {curso}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'images/Ingressantes_Barra/Ingressantes_Femininas_{curso}_Barra.png', dpi=300, bbox_inches='tight')

print("Gráficos gerados com sucesso!")
