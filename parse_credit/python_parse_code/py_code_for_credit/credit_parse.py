import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
from library_for_common_parse_functions.common_parser_functions import initialize_driver,clear_file, save_to_file
chrome_driver_path = local_path_chrome_driver # изменить путь на свой chromedriver

url = 'https://www.rsb.ru/credits/#tariffs'

name_of_info = [
    'Информация о кредите в Банке Русский стандарт',
]

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

def parse_repayment_info(driver, url, output_file):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".list.block_pl_0"))
        )

        repayment_options = driver.find_elements(By.CSS_SELECTOR, ".list.block_pl_0 li")
        save_to_file("\nСпособы погашения кредита:", output_file)

        for option in repayment_options:
            save_to_file(f"- {option.text}", output_file)

    except Exception as e:
        save_to_file(f"Ошибка при парсинге способов погашения кредита: {e}", output_file)

def main():
    # Определение пути на два уровня выше текущего скрипта
    script_dir = os.path.dirname(__file__)  # Путь к директории, где находится скрипт
    parent_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))  # Два уровня выше
    output_dir = os.path.join(parent_dir, "collected_data")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "credit_info.txt")

    clear_file(output_file) #очищаем файл от информации в нем

    driver = initialize_driver(chrome_driver_path)
    try:
        save_to_file(name_of_info[0], output_file)
        parse_bricks_info(driver, url, output_file)
        parse_info(driver, output_file)

        repayment_url = 'https://www.rsb.ru/credits/#repay'
        parse_repayment_info(driver, repayment_url, output_file)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
