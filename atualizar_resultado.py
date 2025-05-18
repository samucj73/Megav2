import requests

def obter_ultimo_resultado():
    url = 'https://api.guidi.dev.br/loteria/megasena/ultimo'
    response = requests.get(url)
    response.raise_for_status()

    dados = response.json()
    dezenas = dados.get('listaDezenas', [])
    numeros = [int(dezena) for dezena in dezenas]
    return numeros

def salvar_resultado():
    numeros = obter_ultimo_resultado()
    with open('resultados.txt', 'w') as f:
        f.write(' '.join(map(str, numeros)))

if __name__ == '__main__':
    salvar_resultado()
