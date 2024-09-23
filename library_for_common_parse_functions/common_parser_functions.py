from selenium import webdriver
from selenium.webdriver.chrome.service import Service



def initialize_driver(chrome_driver_path):
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service)

def clear_file(filename):
    """Функция для очистки файла перед записью данных"""
    with open(filename, 'w', encoding='utf-8') as f:
        pass

def save_to_file(text, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text + '\n')