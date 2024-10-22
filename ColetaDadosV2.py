from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

# Configurar opções para o Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless=new")  # Use a nova versão do modo headless
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=10,10")

# Tente adicionar argumentos para fazer o navegador parecer menos um bot
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("enable-automation")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Definir o caminho para o ChromeDriver
service = Service('')

# Função para inicializar o navegador
def initialize_browser():
    browser = webdriver.Chrome(service=service, options=chrome_options)
    return browser

# Função para fazer a requisição POST usando JavaScript no navegador controlado pelo Selenium
def post_request(url, data, headers):
    browser = initialize_browser()

    # Criar um script JavaScript para fazer a requisição POST
    script = f"""
        return fetch('{url}', {{
            method: 'POST',
            headers: {json.dumps(headers)},
            body: {json.dumps(data)},
        }}).then(response => response.json());
    """

    # Executar o script no navegador
    response_data = browser.execute_script(script)
    browser.quit()

    return response_data


def get_request(url):
    browser = initialize_browser()
    browser.get(url)

    # Capturar o conteúdo HTML da página carregada
    page_content = browser.page_source
    browser.quit()

    return page_content

# Fazer a requisição POST
def post(url, data):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0',
    }
    print(data)
    response = post_request(url, data, headers)
    return response

