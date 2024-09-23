import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
from library_for_common_parse_functions.common_parser_functions import initialize_driver,clear_file, save_to_file

chrome_driver_path = local_path_chrome_driver
url = 'https://www.rsb.ru/credits/otkaz-po-kreditu/'

name_of_info = [
    'Информация о отказе по заявке на кредитный продукт',
]

def parse_credit_rejection_info(driver, url, output_file):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.h1_title"))
        )

        # Заголовок страницы
        title_element = driver.find_element(By.CSS_SELECTOR, "h1.h1_title")
        save_to_file(f"Заголовок страницы: {title_element.text}", output_file)

        # Секция с текстом под заголовком страницы
        intro_paragraph = driver.find_element(By.CSS_SELECTOR, ".row.text-center .h2")
        save_to_file(f"{intro_paragraph.text}\n", output_file)

        # Парсинг каждой секции
        info_sections = driver.find_elements(By.CSS_SELECTOR, ".brick, .info-round")
        for section in info_sections:
            # Заголовки секций и описание
            h2_elements = section.find_elements(By.CSS_SELECTOR, "h2, h3")
            content_buffer = ""

            for h2 in h2_elements:
                if content_buffer:
                    save_to_file(content_buffer.strip(), output_file)
                    content_buffer = ""
                save_to_file(f"\n{h2.text}", output_file)

            # Парсинг текста секции
            paragraphs = section.find_elements(By.CSS_SELECTOR, "p")
            for paragraph in paragraphs:
                content_buffer += f"{paragraph.text}\n"

            # Парсинг списков в секции
            ul_elements = section.find_elements(By.CSS_SELECTOR, "ul")
            for ul in ul_elements:
                li_elements = ul.find_elements(By.TAG_NAME, "li")
                for li in li_elements:
                    content_buffer += f"- {li.text}\n"

            if content_buffer:
                save_to_file(content_buffer.strip(), output_file)

    except Exception as e:
        save_to_file(f"Ошибка при парсинге страницы отказа по кредиту: {e}", output_file)

def main():
    # Определение пути на два уровня выше текущего скрипта
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
    output_dir = os.path.join(parent_dir, "collected_data")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "otkaz_po_credit_info.txt")

    clear_file(output_file)
    driver = initialize_driver(chrome_driver_path)
    try:
        save_to_file(name_of_info[0], output_file)
        parse_credit_rejection_info(driver, url, output_file)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
