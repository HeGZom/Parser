import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import os


download_directory = "C:\\Users\\Глеб\\PycharmProjects\\parse\\parse_credit\\pdf_doc_for_credit"  # Поменять на свою


chrome_options = webdriver.ChromeOptions()
chrome_service = Service(executable_path='C:\\chromedriver\\chromedriver.exe')


driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


driver.get("https://www.rsb.ru/credits/#tariffs")


content = driver.find_element(By.ID, "tariffs")
soup = BeautifulSoup(content.get_attribute("outerHTML"), "html.parser")


pdf_links = soup.find_all("a", class_="link link_doc")


def clean_filename(filename, max_length=100):
    # Заменить недопустимые символы на подчеркивания
    cleaned_name = re.sub(r'[<>:"/\\|?*«»]', '_', filename)
    return cleaned_name[:max_length]


for link in pdf_links:
    pdf_url = link.get("href")
    document_title = link.get_text(strip=True).replace(' ', '_')  # Убрать пробелы из названия
    document_title = document_title.replace('\xa0', '_')  # Убрать неразрывные пробелы

    document_name = clean_filename(f"{document_title}.pdf")

    # Полный URL
    if pdf_url.startswith('/'):
        pdf_url = 'https://tariffolds.rsb.ru' + pdf_url

    # Скачивание PDF-файла
    response = requests.get(pdf_url)

    # Сохранение файла с правильным именем
    with open(os.path.join(download_directory, document_name), 'wb') as file:
        file.write(response.content)

    print(f"Файл {document_name} успешно скачан с URL: {pdf_url}")

driver.quit()
