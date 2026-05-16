from bs4 import BeautifulSoup
import requests

URL = r"https://www.amazon.com.br/Notebook-Gamer-Intel%C2%AE-CoreTM-i5-13420H/dp/B0FYJ67V77/?_encoding=UTF8&pd_rd_w=rJdJ1&content-id=amzn1.sym.15743f4a-c561-497f-bfe3-7bd76c77c6dc%3Aamzn1.symc.f98aa93d-7637-4d44-9ae2-49d76e4b7ac8&pf_rd_p=15743f4a-c561-497f-bfe3-7bd76c77c6dc&pf_rd_r=SBCSA72JE02P306BC325&pd_rd_wg=HB4ck&pd_rd_r=8cdd7128-df98-423c-ade9-a588a5916971"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(URL, headers=headers)

if response.status_code != 200:
    exit(1)

with open("temp.html", "w", encoding="utf-8") as f:
    f.write(response.text)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

item_tags = soup.select('li[class="a-carousel-card"]')

tabela = []

for item_tag in item_tags:
    linha = dict()
    nome_tag = item_tag.select_one("div[class*='_cDEzb_p13n']")
    nome = nome_tag.get_text(strip=True)
    linha["produto"] = nome

    preco_tag = item_tag.select_one("span[class='a-price-whole']")
    preco = preco_tag.get_text(strip=True)
    preco = preco.replace(",", "").replace(".", "")
    linha["preco"] = int(preco) + 1

    imagem_tag = item_tag.select_one("img")

    link_imagem = imagem_tag.get("src")
    
    nome_arquivo = nome[:26] + ".jpg"
    img_response = requests.get(link_imagem)
    if img_response.status_code == 200:
        with open(nome_arquivo, "wb") as img:
            img.write(img_response.content)

    linha["imgpath"] = nome_arquivo

    linha["img"] = link_imagem


    tabela.append(linha)

import pandas as pd

df = pd.DataFrame(tabela)
df.to_excel("pcs.xlsx")

