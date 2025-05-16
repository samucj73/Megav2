
from fpdf import FPDF

def exportar_txt(cartoes, caminho='jogos_megasena.txt'):
    with open(caminho, 'w') as f:
        for i, cartao in enumerate(cartoes, start=1):
            linha = f"Cartão {i}: " + " - ".join(f"{n:02}" for n in cartao)
            f.write(linha + "\n")
    return caminho

def exportar_pdf(cartoes, caminho='jogos_megasena.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Jogos Mega-Sena Gerados", ln=True, align='C')
    pdf.ln(10)

    for i, cartao in enumerate(cartoes, start=1):
        linha = f"Cartão {i}: " + " - ".join(f"{n:02}" for n in cartao)
        pdf.cell(200, 10, txt=linha, ln=True)

    pdf.output(caminho)
    return caminho
