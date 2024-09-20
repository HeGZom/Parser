import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = "C:\\chromedriver\\chromedriver.exe"  # изменить путь на свой chromedriver
url = 'https://www.rsb.ru/credits/#tariffs'

name_of_info = [
    'Информация о кредите в Банке Русский стандарт',
]

def initialize_driver():
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service)

def save_to_file(text, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text + '\n')

def parse_bricks_info(driver, url, output_file):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".brick"))
        )

        brick_blocks = driver.find_elements(By.CSS_SELECTOR, ".brick .info-block")

        for block in brick_blocks:
            try:
                title_element = block.find_element(By.CSS_SELECTOR, ".h2_info__text")
                title = title_element.text if title_element else "Заголовок не найден"

                description_element = block.find_element(By.CSS_SELECTOR, ".info-block__note-under-title")
                description = description_element.text if description_element else "Описание не найдено"

                save_to_file(title, output_file)
                save_to_file(description, output_file)

            except Exception as e:
                pass

    except Exception as e:
        save_to_file(f"Ошибка при парсинге блоков brick: {e}", output_file)

def parse_info(driver, output_file):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".block_mb_60"))
        )

        headers = driver.find_elements(By.CSS_SELECTOR, ".h2.h2_font_50.h2_mb_0.text_xs_center")
        for header in headers:
            save_to_file(f"Заголовок: {header.text}", output_file)

        list_items = driver.find_elements(By.CSS_SELECTOR, ".list-marker__item-txt")
        for item in list_items:
            h4 = item.find_element(By.TAG_NAME, "h4").text
            save_to_file(f"\nРаздел: {h4}", output_file)
            ul = item.find_element(By.CSS_SELECTOR, "ul")
            li_elements = ul.find_elements(By.TAG_NAME, "li")
            for li in li_elements:
                save_to_file(f"- {li.text}", output_file)

        info_block = driver.find_element(By.CSS_SELECTOR, ".info-block__footnote")
        save_to_file(f"\nУсловия кредита: {info_block.text}", output_file)

    except Exception as e:
        save_to_file(f"Ошибка при загрузке или парсинге страницы: {e}", output_file)

def main():
    # Определение пути на два уровня выше текущего скрипта
    script_dir = os.path.dirname(__file__)  # Путь к директории, где находится скрипт
    parent_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))  # Два уровня выше
    output_dir = os.path.join(parent_dir, "collected_data")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "credit_info.txt")

    driver = initialize_driver()
    try:
        save_to_file(name_of_info[0], output_file)
        parse_bricks_info(driver, url, output_file)
        parse_info(driver, output_file)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
