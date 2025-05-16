import streamlit as st
from gerador_megasena import gerar_cartoes
from util import exportar_pdf, exportar_txt
from mega_estatisticas import (
    dezenas_mais_sorteadas,
    dezenas_menos_sorteadas,
    pares_impares,
    soma_dezenas,
    distribuicao_linha_coluna,
    graficos_estatisticos
)

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

st.markdown("---")
st.subheader("📊 Estatísticas dos Cartões Gerados")

if st.session_state.historico:
    mais_sorteadas = dezenas_mais_sorteadas(st.session_state.historico)
    menos_sorteadas = dezenas_menos_sorteadas(st.session_state.historico)

    st.write("🔝 Dezenas mais sorteadas:")
    for dezena, freq in mais_sorteadas:
        st.write(f"Dezena {dezena:02} apareceu {freq} vezes.")

    st.write("🔻 Dezenas menos sorteadas:")
    for dezena, freq in menos_sorteadas:
        st.write(f"Dezena {dezena:02} apareceu {freq} vezes.")

    fig = graficos_estatisticos()
    st.pyplot(fig)

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

# 🔟 Últimos 10 resultados da Mega-Sena (dados reais manualmente adicionados)
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
