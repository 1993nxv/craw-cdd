import pandas as pd
from bs4 import BeautifulSoup
from service.ColetaDadosAppService import coletaLinksCnpjs
import ColetaDadosV2
import time

def extrair_texto_por_label(label, soup):
    elemento = soup.find('label', string=label)
    if elemento:
        valor = elemento.find_next('p').text.strip()
        return valor
    return None

# Extração de outros campos que podem ter múltiplos elementos
def extrair_multiplos_campos(label, soup):
    elementos = soup.find_all('label', text=label)
    valores = [el.find_next('p').text.strip() for el in elementos]
    return ', '.join(valores) if valores else None

with open("query.json", "r") as query:
    query = query.read()

for i in range(11, 40):
    url = "https://api.casadosdados.com.br/v2/public/cnpj/search"

    query = query.replace(",\"page\":1", ',"page":' + str(i))
    print('Coletando dados page: ' + str(i))

    response = ColetaDadosV2.post(url, query)
    linksCnpjs = coletaLinksCnpjs(response)

    for link in linksCnpjs:

        respostaa = ColetaDadosV2.get_request(link)

        respostaa = BeautifulSoup(respostaa, 'html.parser')

        # # COLETANDO DADOS DA EMPRESA E INSERINDO NA PLANILHA
        # dadosEmpresa = respostaa.findAll('div', {"class": "p-3"})

        camposDataFrame = {
            "CNPJ": extrair_texto_por_label("CNPJ:", respostaa),
            "Razão Social": extrair_texto_por_label("Razão Social:", respostaa),
            "Tipo": extrair_texto_por_label("Matriz ou Filial:", respostaa),
            "Data Abertura": extrair_texto_por_label("Data de Abertura:", respostaa),
            "Situação Cadastral": extrair_texto_por_label("Situação Cadastral:", respostaa),
            "Data da Situação Cadastral": extrair_texto_por_label("Data da Situação:", respostaa),
            "Capital Social": extrair_texto_por_label("Capital Social:", respostaa),
            "Natureza Jurídica": extrair_texto_por_label("Natureza Jurídica:", respostaa),
            "Empresa MEI": extrair_texto_por_label("Empresa MEI:", respostaa),
            "Logradouro": extrair_texto_por_label("Logradouro:", respostaa),
            "Número": extrair_texto_por_label("Número:", respostaa),
            "Complemento": extrair_texto_por_label("Complemento:", respostaa),
            "CEP": extrair_texto_por_label("CEP:", respostaa),
            "Bairro": extrair_texto_por_label("Bairro:", respostaa),
            "Município": extrair_texto_por_label("Município:", respostaa),
            "UF": extrair_texto_por_label("UF:", respostaa),
            "Telefone": extrair_texto_por_label("Telefone:", respostaa),
            "E-MAIL": extrair_texto_por_label("E-MAIL:", respostaa),
            "Quadro Societário": extrair_texto_por_label("Quadro Societário:", respostaa),
            "Atividade Principal": extrair_texto_por_label("Atividade Principal:", respostaa),
            "Atividades Secundárias": extrair_texto_por_label("Atividades Secundárias:", respostaa),
            "Data da Consulta": extrair_texto_por_label("Ultima Atualização:", respostaa),
            "Nome Fantasia": extrair_texto_por_label("Nome Fantasia:", respostaa)
        }

        # Extrair telefone e formatar para WhatsApp
        telefone = extrair_texto_por_label("Telefone:", respostaa)
        if telefone:
            telefone = telefone.replace(' ', '').replace('-', '')
            camposDataFrame["Telefone"] = f'https://wa.me/+55{telefone}'

        # for c in dadosEmpresa:
        #     campos = c.find_all_next('p')
        #     campo = campos[0].text
        #     valor = campos[1].text
        #     if campo == 'Telefone':
        #         valor = valor.replace(' ', '')
        #         valor = valor.replace('-', '')
        #         valor = 'https://wa.me/+55' + valor
        #     camposDataFrame[campo] = valor

        # Criar o DataFrame
        df = pd.DataFrame(data=[camposDataFrame])

        # Carregar a planilha existente como DataFrame
        arquivo_excel = 'ContatosGo1.xlsx'

        try:
            existing_df = pd.read_excel(arquivo_excel)
            # Adicionar os valores do novo DataFrame em uma nova linha
            merged_df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            # Se o arquivo não existir, usar apenas o novo DataFrame
            merged_df = df

        # Salvar o DataFrame de volta no arquivo
        merged_df.to_excel(arquivo_excel, index=False)

        print(f"Dados adicionados em uma nova linha em {arquivo_excel} com sucesso.")

        time.sleep(3)
    with open("query.json", "r") as query:
        query = query.read()

time.sleep(3)