import pandas as pd
import matplotlib.pyplot as plt
from utils.secret import FILE_PATH
from utils.dataset import nomes_femininos, nomes_masculinos

file_path = FILE_PATH
df = pd.read_csv(file_path)
restante = []

with open(FILE_PATH) as ficheiro:
    evadidos = {"Aluno com Vínculo": {"F": 0, "M": 0},"Transferência Interna": {"F": 0, "M": 0},"Abandono": {"F": 0, "M": 0},"Desistente Oficial": {"F": 0, "M": 0},"Desistente": {"F": 0, "M": 0},"Formado": {"F": 0, "M": 0},"Desligamento": {"F": 0, "M": 0}}
    for linha in ficheiro:
        CURSO_COD, CURSO_NOME, INGRESSO_FORMA, INGRESSO_ANO, PERIODO_INGRE_ITEM, INGRESSO_PERIODO, EVASAO_FORMA, EVASAO_ANO, EVASAO_PERIODO, ALUNO_MATRICULA, ALUNO_NOME = linha.strip().split(",")
        if CURSO_COD == "1188370BI":

            if ALUNO_NOME.split()[0] in nomes_femininos:
                genero = "F"
            elif ALUNO_NOME.split()[0] in nomes_masculinos:
                genero = "M"
            else:
                restante.append(ALUNO_NOME.split()[0])
                continue  
            
            if EVASAO_FORMA in evadidos:
                evadidos[EVASAO_FORMA][genero] += 1

print("Nomes não identificados:", restante)

plt.figure(figsize=(12, 6))  

situacoes = list(evadidos.keys())
feminino = [evadidos[situação]["F"] for situação in situacoes]
masculino = [evadidos[situação]["M"] for situação in situacoes]

bar_width = 0.35
index = range(len(situacoes))

bars_feminino = plt.bar(index, feminino, bar_width, label='Feminino', color='lightblue')
bars_masculino = plt.bar([i + bar_width for i in index], masculino, bar_width, label='Masculino', color='lightcoral')

plt.xlabel('Situação de Evasão')
plt.ylabel('Número de Alunos')
plt.title('Situação de estudantes em Engenharia Eletrônica e de Telecomunicações por Gênero (2019-2024)')
plt.xticks([i + bar_width / 2 for i in index], situacoes) 
plt.legend()

for bar in bars_feminino:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

for bar in bars_masculino:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

plt.tight_layout() 
plt.savefig('images/situacao_evasao_telecom.png', dpi=300, bbox_inches='tight')
