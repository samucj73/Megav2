from collections import Counter

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
