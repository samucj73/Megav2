import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
from gerador_megasena import gerar_cartoes
from util import exportar_pdf, exportar_txt
from mega_estatisticas import (
    dezenas_mais_sorteadas,
    dezenas_menos_sorteadas,
    pares_impares,
    soma_dezenas,
    distribuicao_linha_coluna
)

# Funções auxiliares
def ler_ultimo_resultado():
    try:
        with open("resultados.txt", "r") as f:
            return sorted([int(x) for x in f.read().strip().split()])
    except:
        return []

def comparar_com_ultimo(cartao, resultado):
    acertos = set(cartao) & set(resultado)
    return sorted(acertos), len(acertos)

# Configuração inicial
st.set_page_config(page_title="Mega-Sena Inteligente", layout="centered")
st.markdown("<h1 style='text-align: center;'>🎯 Mega-Sena Inteligente</h1>", unsafe_allow_html=True)

# Controle de cartões
quantidade = st.slider("Quantos cartões deseja gerar?", 1, 10, 1)

if "historico" not in st.session_state:
    st.session_state.historico = []

# Geração de cartões
if st.button("🎰 Gerar Cartões"):
    cartoes = gerar_cartoes(quantidade)
    st.session_state.historico.extend(cartoes)

    resultado = ler_ultimo_resultado()

    st.markdown("---")
    st.subheader("🃏 Cartões Gerados")
    for i, cartao in enumerate(cartoes, start=1):
        texto = f"Cartão {i}: {' - '.join(f'{n:02}' for n in cartao)}"
        if resultado:
            acertos, qtd = comparar_com_ultimo(cartao, resultado)
            texto += f" | 🎯 {qtd} acertos: {', '.join(map(str, acertos)) if acertos else 'nenhum'}"
        st.success(texto)

# Últimos concursos reais
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>🎲 Últimos 10 Resultados da Mega-Sena</h3>", unsafe_allow_html=True)

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

# Estatísticas reais
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>📊 Estatísticas - Últimos 10 Concursos</h3>", unsafe_allow_html=True)

dezenas_reais = [dez for _, dez in ultimos_resultados]
todas = [n for sub in dezenas_reais for n in sub]

mais = dezenas_mais_sorteadas(dezenas_reais)
menos = dezenas_menos_sorteadas(dezenas_reais)

st.write("🔝 Dezenas mais sorteadas:")
for d, f in mais:
    st.write(f"Dezena {d:02} apareceu {f} vezes.")

st.write("🔻 Dezenas menos sorteadas:")
for d, f in menos:
    st.write(f"Dezena {d:02} apareceu {f} vezes.")

# Gráfico
contagem = Counter(todas)
labels = sorted(contagem.keys())
valores = [contagem[d] for d in labels]

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(labels, valores, color="darkgreen")
ax.set_title("Frequência das Dezenas")
ax.set_xlabel("Dezena")
ax.set_ylabel("Frequência")
st.pyplot(fig)

# Estatísticas adicionais
st.markdown("### 📈 Estatísticas Adicionais")
pares_txt = pares_impares(todas)
soma_txt = soma_dezenas(todas)
dist_txt = distribuicao_linha_coluna(todas)

st.info(pares_txt)
st.info(soma_txt)
st.info(dist_txt)

# Probabilidades
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>🧮 Probabilidades</h3>", unsafe_allow_html=True)
st.markdown("""
- **Sena (6 acertos):** 1 em 50.063.860  
- **Quina (5 acertos):** 1 em 154.518  
- **Quadra (4 acertos):** 1 em 2.332  
- **Probabilidade de acertar 3 dezenas:** ~1 em 74  
""")

# Exportar
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>📥 Exportar Jogos</h3>", unsafe_allow_html=True)

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

# Rodapé
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🔧 Desenvolvido por <b>SAMUCJ TECHNOLOGY</b></p>", unsafe_allow_html=True)
