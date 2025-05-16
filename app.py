import streamlit as st
import requests
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

def obter_ultimos_resultados_reais(qtd=10):
    url = f"https://loteriascaixa-api.herokuapp.com/api/megasena/ultimos/{qtd}"
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            return [sorted(map(int, concurso['dezenas'])) for concurso in dados]
        else:
            return f"Erro ao acessar API: {resposta.status_code}"
    except Exception as e:
        return f"Erro na requisição: {str(e)}"

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

# Estatísticas dos jogos gerados
if st.session_state.historico:
    st.markdown("---")
    st.subheader("📊 Estatísticas dos Jogos Gerados")

    estatisticas = calcular_estatisticas(st.session_state.historico)

    for titulo, valor in estatisticas.items():
        st.markdown(f"**{titulo}:**")
        if isinstance(valor, list):
            st.write(", ".join(str(v) for v in valor))
        else:
            st.write(valor)

# Exportação
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

# Últimos sorteios reais
st.markdown("---")
st.subheader("🎲 Últimos 10 Resultados da Mega-Sena (Reais)")

resultados_reais = obter_ultimos_resultados_reais()

if isinstance(resultados_reais, list):
    for i, dezenas in enumerate(resultados_reais, 1):
        st.markdown(f"**Concurso {i}:** {' - '.join(f'{d:02}' for d in dezenas)}")
else:
    st.error(resultados_reais)
