
import matplotlib.pyplot as plt
from collections import Counter

def dezenas_mais_sorteadas(historico):
    contagem = Counter()
    for jogo in historico:
        contagem.update(jogo)
    return contagem.most_common(6)

def dezenas_menos_sorteadas(historico):
    contagem = Counter()
    for jogo in historico:
        contagem.update(jogo)
    return contagem.most_common()[:-7:-1]

def pares_impares(resultado):
    pares = len([n for n in resultado if n % 2 == 0])
    impares = 6 - pares
    return f"Pares: {pares}, Ímpares: {impares}"

def soma_dezenas(resultado):
    return f"Soma das dezenas: {sum(resultado)}"

def distribuicao_linha_coluna(resultado):
    colunas = [0]*10
    for n in resultado:
        colunas[(n-1)//6] += 1
    return f"Distribuição por faixa de dezenas (1-10, ..., 51-60): {colunas}"

def graficos_estatisticos():
    # Exemplo com números fictícios
    dezenas = list(range(1, 61))
    freq = [i % 10 + 1 for i in dezenas]

    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(dezenas, freq, color="green")
    ax.set_title("Frequência Fictícia das Dezenas (Exemplo)")
    ax.set_xlabel("Dezena")
    ax.set_ylabel("Frequência")
    return fig
