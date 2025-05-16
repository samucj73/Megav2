import streamlit as st
from gerador_megasena import gerar_cartoes
from util import exportar_pdf, exportar_txt
from mega_estatisticas import calcular_estatisticas

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

    # Mostrar estatísticas
    st.subheader("📊 Estatísticas dos Números Gerados")
    stats = calcular_estatisticas(st.session_state.historico)
    st.write(stats)

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
