import requests
import pandas as pd
import json as js
from bs4 import BeautifulSoup
from controller.ColetaDadosAppController import coletaLinksCnpjs
from controller.ColetaDadosAppController import coletaDadosCnpj
import time

headersPost = {
                'Content-Type': 'application/json',
                'User-Agent': 'insomnia/8.6.1'
              }

headersGet =  {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'cookie': '_ga=GA1.1.1110691701.1711111577; cf_clearance=zZr1dDgkk2DkbeRQQuMLSCycK4wAi4PBqc0zkz5PFGg-1711456960-1.0.1.1-NrDkRXgR_FgIjafOIXOs2Bz6E9ebXjT8D.vnXuorHxYBEzG85LxJkf6L9fC7Wgk4UJmKTvF3nrmZOsWp0lg4KA; FCNEC=%5B%5B%22AKsRol84RgxD67pmjMfgt-tC0Iwyn2R_nS8liw6iWzA4ZChp3Ejt8jUrmBXuLak0MvzUonDA4CtvnSHDs1jFlSo-KSO-fZ6ARZMTRPGKLFsMlPan0hnWHKdx-rFxcyQbdoV2dbMGwwSZru4g0P-CjWyZylJgn7mjHQ%3D%3D%22%5D%5D; _ga_06Q5WY4PHL=GS1.1.1711456959.10.0.1711456964.0.0.0'
              }

with open("query.json", "r") as query:
    query = query.read()

for i in range(30,51):
    query = query.replace(',"page":1',',"page":' + str(i))
    print('Coletando dados page: ' + str(i))

    linksCnpjs = coletaLinksCnpjs(query = query, headersPost = headersPost)


    for link in linksCnpjs:
        respostaa = requests.get(link, headers=headersGet).content
        respostaa = BeautifulSoup(respostaa, 'html.parser')

        # COLETANDO DADOS DA EMPRESA E INSERINDO NA PLANILHA
        dadosEmpresa = respostaa.findAll('div', {"class": "column is-narrow"})

        camposDataFrame = {}
        for c in dadosEmpresa:
            campos = c.find_all_next('p')
            campo = campos[0].text
            valor = campos[1].text
            if campo == 'Telefone':
                valor = valor.replace(' ', '')
                valor = valor.replace('-', '')
                valor = 'https://wa.me/+55' + valor
            camposDataFrame[campo] = valor

        # Criar o DataFrame
        df = pd.DataFrame(data=[camposDataFrame])

        # Carregar a planilha existente como DataFrame
        arquivo_excel = 'ContatosApGoiania.xlsx'
        existing_df = pd.read_excel(arquivo_excel)

        # Adicionar os valores do novo DataFrame em uma nova linha
        merged_df = pd.concat([existing_df, df], ignore_index=True)

        # Salvar o DataFrame de volta no arquivo Excel
        merged_df.to_excel(arquivo_excel, index=False)

        print(f'Dados adicionados em uma nova linha em {arquivo_excel} com sucesso.')

        time.sleep(5)

time.sleep(10)



#query = query.replace(',"page":1}', ',"page":2}')
#conteudo = requests.post("https://api.casadosdados.com.br/v2/public/cnpj/search", data=query, headers=headers).content

"""
    # BUSCA ELEMENTOS QUE CONTÉM OS DADOS
    title = respostaa.find('title').text
    divco = respostaa.find('div', {"class": "column is-9"})

    # TRATAMENTO NOME E CNPJ
    title = title.split('-')

    nome = title[0]
    print("Nome:" + nome)

    cnpj = title[1].replace(' CNPJ', '')
    print("CNPJ:" + cnpj)

    # TRATAMENTO TELEFONE E EMAIL
    divco = divco.findAll('a')
    whatsapp = "https://wa.me/+55" + divco[3].get('href').replace('tel:', '').replace(' ', '')
    print("WhatsApp: " + whatsapp)
    contatoSecundario = divco[4].get('href').replace('tel:', '').replace(' ', '')
    print("Contato Secudário: " + contatoSecundario)

    arquivoXlsx = 'ContatosGoiania.xlsx'
    df = pd.read_excel(arquivoXlsx)

    new_data = pd.DataFrame([
        {'Nome': nome, 'CNPJ': cnpj, 'WhatsApp': whatsapp, 'Contato Secundário': contatoSecundario}
    ])

    # Adicionar novas linhas ao DataFrame
    df = pd.concat([df, new_data], ignore_index=True)

    # Salvar o DataFrame atualizado de volta ao arquivo Excel
    df.to_excel(arquivoXlsx, index=False)
"""
