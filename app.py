import streamlit as st
import requests
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

def obter_ultimos_resultados_reais(qtd=10, concurso_inicial=2863):
    base_url = "https://loteriascaixa-api.litowl.com/api/v1/mega-sena"
    try:
        ultimos = []
        for i in range(qtd):
            concurso = concurso_inicial - i
            resposta = requests.get(f"{base_url}/{concurso}")
            if resposta.status_code == 200:
                dados = resposta.json()
                dezenas = list(map(int, dados['numeros']))
                ultimos.append((concurso, sorted(dezenas)))
            else:
                ultimos.append((concurso, f"Erro {resposta.status_code}"))
        return ultimos
    except Exception as e:
        return f"Erro na requisição: {str(e)}"

# Configuração da página
st.set_page_config(page_title="Mega-Sena Inteligente", layout="centered")
st.title("🎯 Gerador Inteligente de Cartões da Mega-Sena")

# Quantidade de cartões
quantidade = st.slider("Quantos cartões deseja gerar?", 1, 10, 1)

# Histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Botão para gerar cartões
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

# Exportar jogos
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

# Estatísticas
st.markdown("---")
st.subheader("📊 Estatísticas Inteligentes")

if st.session_state.historico:
    mais = dezenas_mais_sorteadas(st.session_state.historico)
    menos = dezenas_menos_sorteadas(st.session_state.historico)

    st.write("🔝 **Dezenas mais sorteadas nos seus jogos:**")
    st.write(", ".join(f"{dezena[0]} ({dezena[1]}x)" for dezena in mais))

    st.write("🔻 **Dezenas menos sorteadas nos seus jogos:**")
    st.write(", ".join(f"{dezena[0]} ({dezena[1]}x)" for dezena in menos))

    ultimo = ler_ultimo_resultado()
    if ultimo:
        st.write("⚖️ " + pares_impares(ultimo))
        st.write("➕ " + soma_dezenas(ultimo))
        st.write("📐 " + distribuicao_linha_coluna(ultimo))

    st.pyplot(graficos_estatisticos())
else:
    st.info("Gere alguns cartões para ver as estatísticas.")

# Últimos resultados reais
st.markdown("---")
st.subheader("🎲 Últimos 10 Resultados da Mega-Sena (Reais)")

resultados_reais = obter_ultimos_resultados_reais()

if isinstance(resultados_reais, list):
    for concurso, dezenas in resultados_reais:
        if isinstance(dezenas, list):
            st.markdown(f"**Concurso {concurso}:** {' - '.join(f'{d:02}' for d in dezenas)}")
        else:
            st.error(f"Concurso {concurso}: {dezenas}")
else:
    st.error(resultados_reais)
