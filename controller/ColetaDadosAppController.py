import requests
import json as js
def coletaLinksCnpjs(query, headersPost):
    query = query
    headersPost = headersPost

    conteudo = requests.post("https://api.casadosdados.com.br/v2/public/cnpj/search", data=query,
                             headers=headersPost).content
    dados_json = js.loads(conteudo)

    # Acessando os CNPJs
    cnpjs = dados_json['data']['cnpj']

    # Exibindo os Links CNPJs
    linksCnpjs = []
    for cnpj in cnpjs:
        linksCnpjs.append("https://casadosdados.com.br/solucao/cnpj/" + cnpj['cnpj'])
        print("https://casadosdados.com.br/solucao/cnpj/" + cnpj['cnpj'])

    return linksCnpjs

def coletaDadosCnpj(linkCnpj, headersGet):

    linkCnpj = linkCnpj
    headersGet = headersGet

    conteudo = requests.get(linkCnpj, headers=headersGet).content
    return conteudo