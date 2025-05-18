import streamlit as st
import requests
from collections import Counter
import matplotlib.pyplot as plt
import random

from gerador_megasena import gerar_cartoes
from util import exportar_pdf, exportar_txt
from mega_estatisticas import (
    dezenas_mais_sorteadas, dezenas_menos_sorteadas,
    pares_impares, soma_total, primos, fibonacci,
    quadrados_perfeitos, repetidas_concurso_anterior,
    distribuicao_linhas_colunas, encontrar_sequencias,
    contar_duplas_triplas
)

st.set_page_config(page_title="Mega-Sena Inteligente", layout="centered")

def ler_ultimo_resultado():
    try:
        url = 'https://api.guidi.dev.br/loteria/megasena/ultimo'
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        dezenas = dados.get('listaDezenas', [])
        return sorted([int(d) for d in dezenas])
    except:
        return []

def carregar_ultimos_concursos(qtd=10):
    concursos = []
    try:
        url_base = 'https://api.guidi.dev.br/loteria/megasena/'
        response = requests.get(url_base + 'ultimo')
        response.raise_for_status()
        ultimo = response.json().get('numero')

        for numero in range(ultimo, ultimo - qtd, -1):
            r = requests.get(f'{url_base}{numero}')
            r.raise_for_status()
            dados = r.json()
            dezenas = [int(d) for d in dados.get('listaDezenas', [])]
            concursos.append((numero, dezenas))
    except Exception as e:
        st.error(f"Erro ao carregar concursos: {e}")
    return concursos

def comparar_com_ultimo(cartao, resultado):
    acertos = set(cartao) & set(resultado)
    return sorted(acertos), len(acertos)

st.markdown("<h1 style='text-align: center;'>🎯 Mega-Sena Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Gerador de cartões, estatísticas e probabilidade com base em dados reais</p>", unsafe_allow_html=True)

quantidade = st.slider("🎫 Quantos cartões deseja gerar?", 1, 10, 1)
escolhas_usuario = st.multiselect("🔢 Escolha suas dezenas fixas (opcional):", list(range(1, 61)))

ultimos_resultados = carregar_ultimos_concursos()

if "historico" not in st.session_state:
    st.session_state.historico = []

def gerar_cartoes_com_base(escolhas_usuario, qtd):
    dezenas_reais = [dez for _, dez in ultimos_resultados]
    todas = [n for sub in dezenas_reais for n in sub]
    contagem = Counter(todas)
    mais_frequentes = [d for d, _ in contagem.most_common(30)]

    restantes = [d for d in mais_frequentes if d not in escolhas_usuario]
    todos_disponiveis = list(set(range(1, 61)) - set(escolhas_usuario))

    cartoes = []
    for _ in range(qtd):
        complemento_pool = [n for n in restantes if n not in escolhas_usuario]
        complemento = random.sample(complemento_pool, k=6 - len(escolhas_usuario)) if complemento_pool else []
        cartao = sorted(set(escolhas_usuario + complemento))

        while len(cartao) < 6:
            dez_aleatoria = random.choice([n for n in todos_disponiveis if n not in cartao])
            cartao.append(dez_aleatoria)
            cartao = sorted(cartao)

        cartoes.append(cartao)

    return cartoes

if st.button("🎰 Gerar Cartões"):
    if escolhas_usuario and len(escolhas_usuario) > 5:
        st.warning("Você pode escolher no máximo 5 dezenas fixas.")
    else:
        cartoes = gerar_cartoes_com_base(escolhas_usuario, quantidade)
        st.session_state.historico.extend(cartoes)

        resultado = ler_ultimo_resultado()

        for i, cartao in enumerate(cartoes, start=1):
            texto = f"Cartão {i}: {' - '.join(f'{n:02}' for n in cartao)}"
            if resultado:
                acertos, qtd = comparar_com_ultimo(cartao, resultado)
                texto += f" | 🎯 {qtd} acertos: {', '.join(map(str, acertos)) if acertos else 'nenhum'}"
            st.success(texto)

st.markdown("---")
st.subheader("🎲 Últimos 10 Resultados da Mega-Sena (Reais)")

for concurso, dezenas in ultimos_resultados:
    st.markdown(f"**Concurso {concurso}:** {' - '.join(f'{d:02}' for d in dezenas)}")

st.markdown("---")
st.subheader("📊 Estatísticas com Base nos Últimos 10 Concursos Reais")

dezenas_reais = [dezenas for _, dezenas in ultimos_resultados]
todas_dezenas = [num for dezenas in dezenas_reais for num in dezenas]

mais_sorteadas = dezenas_mais_sorteadas(dezenas_reais)
menos_sorteadas = dezenas_menos_sorteadas(dezenas_reais)

st.write("🔝 Dezenas mais sorteadas:")
for dezena, freq in mais_sorteadas:
    st.write(f"Dezena {dezena:02} apareceu {freq} vezes.")

st.write("🔻 Dezenas menos sorteadas:")
for dezena, freq in menos_sorteadas:
    st.write(f"Dezena {dezena:02} apareceu {freq} vezes.")

contagem = Counter(todas_dezenas)
dezenas_ordenadas = sorted(contagem.keys())
frequencias = [contagem[d] for d in dezenas_ordenadas]

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(dezenas_ordenadas, frequencias, color='green')
ax.set_title("Frequência das Dezenas - Últimos 10 Concursos")
ax.set_xlabel("Dezenas")
ax.set_ylabel("Frequência")
st.pyplot(fig)

st.markdown("---")
st.subheader("📈 Estatísticas Avançadas")

if len(ultimos_resultados) >= 2:
    dezenas_reais = [dezenas for _, dezenas in ultimos_resultados]
    todas_dezenas = [num for dezenas in dezenas_reais for num in dezenas]

    pares, impares = pares_impares(todas_dezenas)
    soma = soma_total(todas_dezenas)
    primos_list = primos(todas_dezenas)
    fib_list = fibonacci(todas_dezenas)
    quad_perfeitos = quadrados_perfeitos(todas_dezenas)

    ultimo = ultimos_resultados[-1][1]
    penultimo = ultimos_resultados[-2][1]
    repetidas = repetidas_concurso_anterior(ultimo, penultimo)

    linhas, colunas = distribuicao_linhas_colunas(todas_dezenas)
    sequencias = encontrar_sequencias(todas_dezenas)
    duplas, triplas = contar_duplas_triplas(todas_dezenas)

    st.write(f"🔢 Pares: {pares} | Ímpares: {impares}")
    st.write(f"➕ Soma total das dezenas: {soma}")
    st.write(f"⭐ Dezenas Primas: {', '.join(map(str, primos_list))}")
    st.write(f"🔮 Dezenas Fibonacci: {', '.join(map(str, fib_list))}")
    st.write(f"🔲 Quadrados Perfeitos: {', '.join(map(str, quad_perfeitos))}")
    st.write(f"🔄 Dezenas repetidas do último para o penúltimo concurso: {', '.join(map(str, repetidas))}")
    st.write(f"📊 Distribuição por linhas: {linhas}")
    st.write(f"📊 Distribuição por colunas: {colunas}")
    st.write(f"🔗 Sequências encontradas: {sequencias}")
    st.write(f"📈 Duplas: {duplas} | Triplas: {triplas}")
else:
    st.info("Não há resultados suficientes para análises avançadas.")

st.markdown("---")
st.subheader("📥 Exportar Jogos")

if st.session_state.historico:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬇️ Exportar .TXT"):
            caminho = exportar_txt(st.session_state.historico)
            st.success(f"Arquivo salvo como: {caminho}")
    with col2:
        if st.button("⬇️ Exportar .PDF"):
            caminho = exportar_pdf(st.session_state.historico)
            st.success(f"Arquivo salvo como: {caminho}")
else:
    st.info("Gere pelo menos um cartão para exportar.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Desenvolvido por <strong>SAMUCJ TECHNOLOGY</strong> 💡</p>", unsafe_allow_html=True)
