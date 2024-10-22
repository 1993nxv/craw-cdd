

def coletaLinksCnpjs(response):

    dados_json = response

    # Acessando os CNPJs
    cnpjs = dados_json['data']['cnpj']

    # Exibindo os Links CNPJs
    linksCnpjs = []
    for cnpj in cnpjs:
        linksCnpjs.append("https://casadosdados.com.br/solucao/cnpj/" + cnpj['cnpj'])
        print("https://casadosdados.com.br/solucao/cnpj/" + cnpj['cnpj'])

    return linksCnpjs
