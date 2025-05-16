from fpdf import FPDF
import os
import datetime

def exportar_txt(cartoes):
    nome_arquivo = f"megasena_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arquivo, "w") as f:
        for i, cartao in enumerate(cartoes, 1):
            f.write(f"Cartão {i}: {' - '.join(f'{n:02}' for n in cartao)}\n")
    return nome_arquivo

def exportar_pdf(cartoes):
    nome_arquivo = f"megasena_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Cartões Mega-Sena", ln=True, align="C")
    pdf.ln(10)
    for i, cartao in enumerate(cartoes, 1):
        linha = f"Cartão {i}: {' - '.join(f'{n:02}' for n in cartao)}"
        pdf.cell(200, 10, txt=linha, ln=True)
    pdf.output(nome_arquivo)
    return nome_arquivo
