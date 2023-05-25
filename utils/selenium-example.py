import time
import random
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from proxy_functions import get_valid_proxies, get_random_proxy


# Configuración
QUERY = "Luján"  # Ingresa tu búsqueda
encoded_query = urllib.parse.quote(QUERY)

# Encabezados de usuario aleatorios
USER_AGENT = UserAgent()
HEADERS = {"User-Agent": USER_AGENT.random}
# Precargar proxies válidos

CHROME_DRIVER_PATH = "C:/Users/Juan/Documents/GitHub/pimei-2023/chromedriver"  # Ruta constante del controlador de Chrome

def initialize_driver(proxy):
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"user-agent={USER_AGENT.random}")
    options.add_argument(f"--proxy-server={proxy}")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_google_scholar(query, proxies_list):
    results = []
    proxy = get_random_proxy(proxies_list)
    print(f'Se escoge aleatoriamente el proxy {proxy}')
    driver = initialize_driver(proxy)
    try:
        for i in range(5):
            url = f"https://scholar.google.com/scholar?q={query}&hl=en&as_sdt=0%2C5&page={i+1}"
            driver.get(url)
            time.sleep(2)
            html = driver.page_source
            if is_blocked(html):
                print("¡Google Scholar ha bloqueado tu solicitud!")
                break
            soup = BeautifulSoup(html, 'html.parser')
            page_results = parse_results(soup)
            results.extend(page_results)
            time.sleep(random.uniform(1, 5))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
    return results


def is_blocked(html):
    soup = BeautifulSoup(html, 'html.parser')
    captcha_div = soup.find('div', class_='g-recaptcha')
    if captcha_div:
        return True
    return False


def parse_results(soup):
    results = []
    for j, result in enumerate(soup.find_all('div', class_='gs_ri')):
        title = result.find('h3', class_='gs_rt').text
        authors = result.find('div', class_='gs_a').text
        description = result.find('div', class_='gs_rs').text
        pdf_link = get_pdf_link(result)
        results.append({
            "Title": title,
            "Authors": authors,
            "Description": description,
            "PDF Link": pdf_link
        })
    return results


def get_pdf_link(result):
    pdf_link = ""
    pdf_div = result.find('div', class_='gs_ggs gs_fl')
    if pdf_div:
        pdf_link_element = pdf_div.find('a')
        if pdf_link_element:
            pdf_link = pdf_link_element['href']
    return pdf_link


def main():
    # Se recopilan proxies válidos
    N_proxies = 5
    proxies = get_valid_proxies(N_proxies)
    print(f'\nSe encontraron {len(proxies)} proxies válidos.')
    
    # Se trabaja en el scraping
    results = scrape_google_scholar(encoded_query, proxies)
    for i, result in enumerate(results, 1):
        print(f"Result {i}")
        print("Title:", result["Title"])
        print("Authors:", result["Authors"])
        print("Description:", result["Description"])
        print("PDF Link:", result["PDF Link"])
        print()

if __name__ == "__main__":
    main()
