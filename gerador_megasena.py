
import random

def gerar_cartoes(qtd):
    cartoes = []
    while len(cartoes) < qtd:
        cartao = sorted(random.sample(range(1, 61), 6))
        if cartao not in cartoes:
            cartoes.append(cartao)
    return cartoes
