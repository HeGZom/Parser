import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = "C:\\chromedriver\\chromedriver.exe"  # изменить путь на свой chromedriver
url = 'https://www.rsb.ru/potrebitelskiy-kredit/#descripion'


def initialize_driver():
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service)


def save_to_file(text, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text + '\n')


def parse_credit_info(driver, url, output_file):
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)

        header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".h2.h2_mb_20"))).text
        save_to_file(f"Заголовок: {header}", output_file)

        description = driver.find_element(By.CSS_SELECTOR, ".color-gray.block_mb_30").text
        save_to_file(f"Описание: {description}\n", output_file)

        # Парсим Быстро, Гибко и прозрачно, Удобно
        save_to_file("Преимущества кредита:", output_file)
        benefit_blocks = driver.find_elements(By.CSS_SELECTOR, ".info-round_credit")
        for benefit_block in benefit_blocks:
            title = benefit_block.find_element(By.CSS_SELECTOR, "h3").text
            desc = benefit_block.find_element(By.CSS_SELECTOR, "p").text
            if title and desc:
                save_to_file(f"{title}: {desc}\n", output_file)

    except Exception as e:
        save_to_file(f"Ошибка при парсинге страницы: {e}", output_file)


def parse_service_info(driver, url, output_file):
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)

        # Уточняем, что ищем блоки услуг по классу .brick, чтобы не зацепить другие .row
        services_row = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".brick")))

        service_columns = driver.find_elements(By.CSS_SELECTOR, ".col-sm-4 .info-block")

        for service_block in service_columns:
            try:
                service_title_element = service_block.find_element(By.CSS_SELECTOR, "h2")
                service_title = service_title_element.text.strip()

                service_desc_element = service_block.find_element(By.CSS_SELECTOR, ".gray-text-small")
                service_desc = service_desc_element.text.strip()

                save_to_file(f"{service_title}:\n{service_desc}\n", output_file)

            except Exception as e:
                save_to_file(f"Ошибка при парсинге блока услуги: {e}", output_file)

    except Exception as e:
        save_to_file(f"Ошибка при парсинге страницы: {e}", output_file)


def main():
    # Определение пути на два уровня выше текущего скрипта
    script_dir = os.path.dirname(__file__)  # Путь к директории, где находится скрипт
    parent_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))  # Два уровня выше
    output_dir = os.path.join(parent_dir, "collected_data")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "potreb_credit_info.txt")

    driver = initialize_driver()
    try:
        parse_credit_info(driver, url, output_file)
        parse_service_info(driver, url, output_file)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
