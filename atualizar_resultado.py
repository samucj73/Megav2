
import requests
from bs4 import BeautifulSoup

def obter_ultimo_resultado():
    url = 'https://www.megasena.com.br/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    # Busca os números da mega
    numeros_div = soup.find_all('li', class_='resultado-loteria__numero')
    if not numeros_div:
        # alternativa se mudar o site
        numeros_div = soup.select('div.resultados > ul > li')
    numeros = [int(n.get_text(strip=True)) for n in numeros_div]
    return numeros

def salvar_resultado():
    numeros = obter_ultimo_resultado()
    with open('resultados.txt', 'w') as f:
        f.write(' '.join(map(str, numeros)))

if __name__ == '__main__':
    salvar_resultado()
