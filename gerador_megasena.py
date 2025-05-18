import random
from collections import Counter

def gerar_cartao():
    """Gera um cartão aleatório simples com 6 dezenas únicas entre 1 e 60."""
    return sorted(random.sample(range(1, 61), 6))

def gerar_cartoes(qtd):
    """Gera múltiplos cartões aleatórios simples."""
    return [gerar_cartao() for _ in range(qtd)]

def gerar_cartoes_inteligentes(qtd, ultimos_resultados, fixas=[]):
    """
    Gera cartões com base nas estatísticas dos últimos concursos:
    - Dezenas mais frequentes nos últimos resultados
    - Dezenas repetidas entre os dois últimos concursos
    - Dezenas fixas escolhidas pelo usuário
    """
    dezenas_reais = [dez for _, dez in ultimos_resultados]
    todas_dezenas = [num for dez in dezenas_reais for num in dez]
    contagem = Counter(todas_dezenas)

    # 🔝 Top 30 dezenas mais frequentes nos últimos concursos
    mais_frequentes = [d for d, _ in contagem.most_common(30)]

    # 🔄 Dezenas repetidas do último para o penúltimo concurso
    repetidas = []
    if len(dezenas_reais) >= 2:
        repetidas = list(set(dezenas_reais[-1]) & set(dezenas_reais[-2]))

    # 🎯 Base de dezenas preferidas
    base_preferida = list(set(mais_frequentes + repetidas))

    # Remove fixas da base para evitar repetição
    base_util = [d for d in base_preferida if d not in fixas]

    # Dezenas restantes disponíveis (fora da base e fixas)
    resto = list(set(range(1, 61)) - set(fixas) - set(base_util))

    cartoes = []
    for _ in range(qtd):
        dezenas = list(fixas)  # começa com fixas
        complemento = random.sample(base_util, k=min(6 - len(dezenas), len(base_util)))
        dezenas.extend(complemento)

        while len(dezenas) < 6:
            nova = random.choice(resto)
            if nova not in dezenas:
                dezenas.append(nova)

        cartoes.append(sorted(dezenas))

    return cartoes
