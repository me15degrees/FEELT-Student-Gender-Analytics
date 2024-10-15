import pandas as pd
import matplotlib.pyplot as plt
from utils.secret import FILE_PATH
from utils.dataset import nomes_femininos, nomes_masculinos
from utils.engenharias import cursos

file_path = FILE_PATH
restante = []

years = range(2019, 2024)

tipos_evasao = ["Transferência Interna", "Desistente Oficial", "Abandono", "Desistente","Desligamento","Transferido", "Acordo Institucional - Transferência Interna"]

data = {curso: {year: {tipo: 0 for tipo in tipos_evasao} for year in years} for curso in cursos}

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

                if EVASAO_FORMA in tipos_evasao and ALUNO_NOME.split()[0] in nomes_femininos:
                    data[nome_curso][INGRESSO_ANO][EVASAO_FORMA] += 1

for curso in cursos.keys():
    plt.figure(figsize=(10, 6))
    
    anos_plot = list(years)
    
    width = 0.2 
    positions = [anos_plot]  
    for i in range(1, len(tipos_evasao)):
        positions.append([x + (i * width) for x in anos_plot])

    for i, tipo in enumerate(tipos_evasao):
        evasao_values = [data[curso][year][tipo] for year in years]
        plt.bar(positions[i], evasao_values, width=width, label=tipo)

    plt.xlabel('Ano de Ingresso')
    plt.ylabel('Quantidade Absoluta de Evasão')
    plt.title(f'Quantidade de Evasão por Tipo no Curso de {curso}')
    plt.xticks([r + width for r in anos_plot], anos_plot)  
    plt.legend(title="Tipos de Evasão")
    plt.grid(axis='y')

    # Salvar o gráfico
    plt.tight_layout()
    plt.savefig(f'images/Tipos_Evasao_Feminina/Evasao_{curso}.png', dpi=300, bbox_inches='tight')

print("Gráficos de evasão gerados com sucesso para cada curso!")

