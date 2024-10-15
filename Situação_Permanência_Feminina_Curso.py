import pandas as pd
import matplotlib.pyplot as plt
from utils.secret import FILE_PATH
from utils.dataset import nomes_femininos, nomes_masculinos
from utils.engenharias import cursos

file_path = FILE_PATH
restante = []

years = range(2019, 2024)

data = {curso: {year: {"Total": 0, "F": 0, "M": 0, "Evasao_F": 0} for year in years} for curso in cursos}

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

                    if EVASAO_FORMA != "Aluno com Vínculo":
                        data[nome_curso][INGRESSO_ANO]["Evasao_F"] += 1

            

taxas_permanencia = {curso: {} for curso in cursos}
for curso, anos in data.items():
    for ano, stats in anos.items():
        total = stats["Total"]
        if total > 0:
            permanencia_feminina = (stats["F"] - stats["Evasao_F"]) / stats["F"] * 100 if stats["F"] > 0 else 0
            taxas_permanencia[curso][ano] = permanencia_feminina

for curso, anos in taxas_permanencia.items():
    plt.figure(figsize=(10, 6))

    anos_plot = list(anos.keys())
    taxas_plot = list(anos.values())

    plt.plot(anos_plot, taxas_plot, marker='o', label="Taxa de Permanência Feminina", color="#C63C51")

    for i, (year, taxa) in enumerate(zip(anos_plot, taxas_plot)):
        plt.text(year, taxa + 0.5, f"{taxa:.2f}%", ha='center', va='bottom', fontsize=10)

    plt.xlabel('Ano de Ingresso')
    plt.ylabel('Taxa de Permanência Feminina (%)')
    plt.title(f"Taxa de Permanência das Alunas no Curso de Eng. {curso}")
    plt.xticks(anos_plot)  
    plt.ylim(0, 100)  
    plt.axhline(50, color='grey', linestyle='--', linewidth=0.8, label='50% de Permanência') 
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'images/Taxa_Permanencia/Taxa_Permanencia_Feminina_{curso}.png', dpi=300, bbox_inches='tight')

print("Gráficos de taxa de permanência gerados com sucesso!")
