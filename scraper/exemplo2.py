from bs4 import BeautifulSoup
import requests
from pystringtoolkit import to_kebab_case
import os
import pandas as pd

# perguntar ao usuário o que pesquisar
pesquisa = to_kebab_case(input("O quê pesquisar? "))
base_url = r"https://lista.mercadolivre.com.br/"
url = os.path.join(base_url, pesquisa)
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("temp.html", "w", encoding="utf-8") as f:
        f.write(response.text)
        print("file written.")
else:
    raise Exception("Error: Status code=",response.status_code)

# create soup
soup = BeautifulSoup(response.text, "html.parser")

# get all items
item_tags = soup.select("div[class*='andes-card poly-card']")

tabela = []

for item_tag in item_tags:
    line = dict()
    # get img source
    img_tag = item_tag.select_one("img")

    # save src
    line["imgsrc"] = img_tag.get("src")

    # get title
    titulo_tag = item_tag.select_one("a[class='poly-component__title']")
    line["titulo"] = titulo_tag.get_text(strip=True)

    # get link
    line["link"] = titulo_tag.get("href","")

    # get nota
    # aqui, há como não existir o elemento, e que vários elementos sejam encontrados
    # vamos tentar converter para número, se for bem sucedido, é uma nota

    nota_tag = item_tag.select_one("span[class='poly-phrase-label']")
    # se não for encontrado nada, nota_tag será "None"
    if nota_tag is not None:
        try:
            line["nota"] = float(nota_tag.get_text(strip=True))
        except ValueError: # Se o texto não puder virar número, esse 'except' impede o código de dar erro
            line["nota"] = ""
    else: # se for nulo
        line["nota"] = ""
    
    # preço
    preco_tag = item_tag.select_one("span[class='andes-money-amount andes-money-amount--cents-superscript']")
    preco_text = preco_tag.get_text(strip=True)

    # precisamos tratar esse preço
    preco_text = preco_text.replace("R$", "")
    preco_text = preco_text.replace(".", "")
    preco_text = preco_text.replace(",", ".")
    preco = float(preco_text)

    line["preço (R$)"] = preco

    # frete
    frete_tag = item_tag.select_one("div[class='poly-component__shipping']")
    line["frete"] = frete_tag.get_text(strip=True) if frete_tag else ""

    # é internacional
    international_tag = item_tag.select_one("span[class='poly-component__cbt']")
    line["internacional"] = "Sim" if international_tag else "Não"


    tabela.append(line)

df = pd.DataFrame(tabela)
df.to_excel(f"{pesquisa}.xlsx", engine="openpyxl")