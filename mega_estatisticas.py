from collections import Counter
import math

def dezenas_mais_sorteadas(dezenas_reais, top=6):
    todas = [num for sub in dezenas_reais for num in sub]
    contagem = Counter(todas)
    return contagem.most_common(top)

def dezenas_menos_sorteadas(dezenas_reais, bottom=6):
    todas = [num for sub in dezenas_reais for num in sub]
    contagem = Counter(todas)
    todas_dezenas = range(1, 61)
    todas_frequencias = {d: contagem.get(d, 0) for d in todas_dezenas}
    ordenadas = sorted(todas_frequencias.items(), key=lambda x: x[1])
    return ordenadas[:bottom]

def pares_impares(dezenas):
    pares = sum(1 for d in dezenas if d % 2 == 0)
    impares = len(dezenas) - pares
    return pares, impares

def soma_total(dezenas):
    return sum(dezenas)

def primos(dezenas):
    primos_set = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                  31, 37, 41, 43, 47, 53, 59}
    return [d for d in dezenas if d in primos_set]

def fibonacci(dezenas):
    fibonacci_set = {1, 2, 3, 5, 8, 13, 21, 34, 55}
    return [d for d in dezenas if d in fibonacci_set]

def quadrados_perfeitos(dezenas):
    return [d for d in dezenas if int(math.sqrt(d))**2 == d]

def repetidas_concurso_anterior(dezenas_reais):
    if len(dezenas_reais) < 2:
        return []
    atual = set(dezenas_reais[-1])
    anterior = set(dezenas_reais[-2])
    return sorted(atual & anterior)

def distribuicao_linhas_colunas(dezenas_reais):
    if not dezenas_reais:
        return {}, {}
    dezenas = dezenas_reais[-1]
    linhas = {i: 0 for i in range(1, 7)}
    colunas = {i: 0 for i in range(1, 11)}
    for d in dezenas:
        linha = ((d - 1) // 10) + 1
        coluna = ((d - 1) % 10) + 1
        linhas[linha] += 1
        colunas[coluna] += 1
    return linhas, colunas

def encontrar_sequencias(dezenas_reais):
    if not dezenas_reais:
        return []
    dezenas = sorted(dezenas_reais[-1])
    sequencias = []
    seq = [dezenas[0]]
    for i in range(1, len(dezenas)):
        if dezenas[i] == dezenas[i - 1] + 1:
            seq.append(dezenas[i])
        else:
            if len(seq) > 1:
                sequencias.append(seq)
            seq = [dezenas[i]]
    if len(seq) > 1:
        sequencias.append(seq)
    return sequencias

def contar_duplas_triplas(dezenas_reais):
    if not dezenas_reais:
        return 0, 0
    dezenas = dezenas_reais[-1]
    linhas, colunas = {}, {}
    for d in dezenas:
        linha = ((d - 1) // 10) + 1
        coluna = ((d - 1) % 10) + 1
        linhas.setdefault(linha, []).append(d)
        colunas.setdefault(coluna, []).append(d)
    duplas = sum(1 for grupo in list(linhas.values()) + list(colunas.values()) if len(grupo) == 2)
    triplas = sum(1 for grupo in list(linhas.values()) + list(colunas.values()) if len(grupo) == 3)
    return duplas, triplas
