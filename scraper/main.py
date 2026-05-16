from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

URL_TO_SCRAPE = r"https://www.scrapethissite.com/pages/simple/"

response = requests.get(URL_TO_SCRAPE)

if response.status_code != 200:
    print("ocorreu um erro.")
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

# A tabela do scraping será uma lista de dicionários
# lista = ["a", "b", "c", "d"]
# dicionário = {chave : valor}

tabela = [] # <- lista vazia!


# div[class="col-md-4 country"]

# selecionar todas os containers com info de interesse

containers = soup.select('div[class="col-md-4 country"]') # CSS Selector

for container in containers:
    # esse loop analisa um container de cada vez
    linha = dict()
    
    # selecionar o nome
    nome_tag = container.select_one('h3[class="country-name"]')
    linha["nome"] = nome_tag.get_text(strip=True)

    capital_tag, populacao_tag, area_tag = container.select('span')

    linha["capital"] = capital_tag.get_text(strip=True)
    linha["populacao"] = int(populacao_tag.get_text(strip=True))
    linha["area"] = float(area_tag.get_text(strip=True))

    tabela.append(linha)


with open("dados.json", "w", encoding="utf-8") as file:
    json.dump(tabela, file, indent=4)

    
# converter para excel

# dataframe
df = pd.DataFrame(tabela)

df.to_csv("dados.csv", index=False)
df.to_excel("dados.xlsx", engine="openpyxl")
