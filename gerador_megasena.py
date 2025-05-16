import random

def gerar_cartao():
    return sorted(random.sample(range(1, 61), 6))

def gerar_cartoes(qtd):
    return [gerar_cartao() for _ in range(qtd)]
