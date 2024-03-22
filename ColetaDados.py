import requests
import pandas as pd
import json as js
from bs4 import BeautifulSoup

headersPost = {
            'Content-Type': 'application/json',
            'User-Agent': 'insomnia/8.6.1'
            }

headersGet = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'cookie': 'ga=GA1.1.1110691701.1711111577; cf_clearance=59kLswhLPg49akQ10MJBbUwFraU77ZhfrLMJKZa51gk-1711114232-1.0.1.1-cBOweooKa4.D6NxPgidgg4zF4oMTm47KkCVpu8.wcXSUDzc1_iL4dVzu7yq2cSp7S3ts2FubAlcNciHP9Sccw; FCNEC=%5B%5B%22AKsRol_VACe5cIxlBE1BhdvL4SiT8k9DhC3xCUUZ4dTH8SjHEwxSwAUfk86CTc4oR9YxF2ob0vrJEtTNWaZM7xr0NzFGRe6eHpWrcv9NM900QFk7kjSsUL8ibQsc87rMtYolD57Trz_nIKYMGSTeFz1V3TNgDbk8pg%3D%3D%22%5D%5D; _ga_06Q5WY4PHL=GS1.1.1711111576.1.1.1711114236.0.0.0'
            }

with open("query.json", "r") as query:
    query = query.read()

conteudo = requests.post("https://api.casadosdados.com.br/v2/public/cnpj/search", data=query, headers=headersPost).content

dados_json = js.loads(conteudo)

# Acessando os CNPJs
cnpjs = dados_json['data']['cnpj']

# Exibindo os CNPJs
linksCnpjs = []
for cnpj in cnpjs:
    linksCnpjs.append("https://casadosdados.com.br/solucao/cnpj/"+cnpj['cnpj'])
    print("https://casadosdados.com.br/solucao/cnpj/"+cnpj['cnpj'])

conteudo = requests.get(linksCnpjs[0], headers=headersGet).content

print(conteudo)

#query = query.replace(',"page":1}', ',"page":2}')
#conteudo = requests.post("https://api.casadosdados.com.br/v2/public/cnpj/search", data=query, headers=headers).content

