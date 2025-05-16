import streamlit as st
from gerador_megasena import gerar_cartoes
from util import exportar_pdf, exportar_txt
from mega_estatisticas import (
    dezenas_mais_sorteadas,
    dezenas_menos_sorteadas,
)
import matplotlib.pyplot as plt
from collections import Counter

def ler_ultimo_resultado():
    try:
        with open("resultados.txt", "r") as f:
            return sorted([int(x) for x in f.read().strip().split()])
    except:
        return []

def comparar_com_ultimo(cartao, resultado):
    acertos = set(cartao) & set(resultado)
    return sorted(acertos), len(acertos)

st.set_page_config(page_title="Mega-Sena Inteligente", layout="centered")
st.title("🎯 Gerador Inteligente de Cartões da Mega-Sena")

quantidade = st.slider("Quantos cartões deseja gerar?", 1, 10, 1)

if "historico" not in st.session_state:
    st.session_state.historico = []

if st.button("🎰 Gerar Cartões"):
    cartoes = gerar_cartoes(quantidade)
    st.session_state.historico.extend(cartoes)

    resultado = ler_ultimo_resultado()

    for i, cartao in enumerate(cartoes, start=1):
        texto = f"Cartão {i}: {' - '.join(f'{n:02}' for n in cartao)}"
        if resultado:
            acertos, qtd = comparar_com_ultimo(cartao, resultado)
            texto += f" | 🎯 {qtd} acertos: {', '.join(map(str, acertos)) if acertos else 'nenhum'}"
        st.success(texto)

# 🔟 Últimos 10 resultados reais da Mega-Sena
st.markdown("---")
st.subheader("🎲 Últimos 10 Resultados da Mega-Sena (Reais)")

ultimos_resultados = [
    (2863, [5, 23, 32, 34, 47, 56]),
    (2862, [2, 4, 14, 18, 22, 44]),
    (2861, [2, 21, 27, 46, 51, 53]),
    (2860, [2, 5, 17, 24, 38, 57]),
    (2859, [7, 8, 15, 17, 20, 51]),
    (2858, [8, 18, 27, 28, 48, 52]),
    (2857, [2, 18, 28, 38, 41, 50]),
    (2856, [3, 5, 10, 27, 38, 48]),
    (2855, [12, 16, 24, 31, 51, 55]),
    (2854, [2, 13, 16, 31, 44, 55]),
]

for concurso, dezenas in ultimos_resultados:
    st.markdown(f"**Concurso {concurso}:** {' - '.join(f'{d:02}' for d in dezenas)}")

# 📊 Estatísticas com base nos últimos concursos reais
st.markdown("---")
st.subheader("📊 Estatísticas com Base nos Últimos 10 Concursos Reais")

# Extrai dezenas dos concursos
dezenas_reais = [dezenas for _, dezenas in ultimos_resultados]
todas_dezenas = [num for dezenas in dezenas_reais for num in dezenas]

# Estatísticas
mais_sorteadas = dezenas_mais_sorteadas(dezenas_reais)
menos_sorteadas = dezenas_menos_sorteadas(dezenas_reais)

st.write("🔝 Dezenas mais sorteadas nos últimos 10 concursos:")
for dezena, freq in mais_sorteadas:
    st.write(f"Dezena {dezena:02} apareceu {freq} vezes.")

st.write("🔻 Dezenas menos sorteadas nos últimos 10 concursos:")
for dezena, freq in menos_sorteadas:
    st.write(f"Dezena {dezena:02} apareceu {freq} vezes.")

# Gráfico de frequência
contagem = Counter(todas_dezenas)
dezenas_ordenadas = sorted(contagem.keys())
frequencias = [contagem[d] for d in dezenas_ordenadas]

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(dezenas_ordenadas, frequencias, color='darkgreen')
ax.set_title("Frequência das Dezenas - Últimos 10 Concursos")
ax.set_xlabel("Dezena")
ax.set_ylabel("Frequência")
st.pyplot(fig)

# 📥 Exportação
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
