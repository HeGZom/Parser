import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import local_path_chrome_driver

chrome_driver_path = local_path_chrome_driver # Измените на путь к вашему chromedriver

urls = [
    'https://www.rsb.ru/cards/mir-130/#tariff',
    'https://www.rsb.ru/cards/mir/#tariff',
    'https://www.rsb.ru/cards/mc-platinum/#tariff',
    # 'https://www.rsb.ru/cards/supreme-premium/#tariff',
    'https://www.rsb.ru/cards/mc-black/#tariff',
    'https://www.rsb.ru/cards/mir-supreme/#tariff',
    'https://www.rsb.ru/cards/union-pay/#tariff'
]

name_of_credit_card = [
    '130 дней без %',
    'Мир',
    'Platinum',
    # 'Mir Supreme Premium'
    'Black',
    'Mir Supreme',
    'Кредитная карта UnionPay'
]


def initialize_driver():
    service = Service(chrome_driver_path)
    return webdriver.Chrome(service=service)


def parse_tariff(driver, url, file):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".tariff-cell"))
        )

        tariff_blocks = driver.find_elements(By.CSS_SELECTOR, ".tariff-cell_block")

        for block in tariff_blocks:
            title = block.find_element(By.CLASS_NAME, "header_line").text
            file.write(f"Тарифы карты {url.split('/')[4]}: {title}\n")

            conditions = block.find_elements(By.CSS_SELECTOR,
                                             ".tariff-cell_row, .tariff-cell_row_no-border, .font_18 block_mb_10 header_line, .row")

            for condition in conditions:
                try:
                    condition_title_elem = condition.find_element(By.CLASS_NAME, "col-sm-7")
                    condition_value_elem = condition.find_element(By.CLASS_NAME, "col-sm-4")

                    condition_title = condition_title_elem.text
                    condition_value = condition_value_elem.text if condition_value_elem else "Нет значения"

                    file.write(f"{condition_title}: {condition_value}\n")

                except Exception as e:
                    file.write(f"Ошибка при получении данных: {e}\n")

    except Exception as e:
        file.write(f"Ошибка при загрузке страницы: {e}\n")


def main():
    # Определение пути на два уровня выше текущего скрипта
    script_dir = os.path.dirname(__file__)  # Путь к директории, где находится скрипт
    parent_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))  # Два уровня выше
    output_dir = os.path.join(parent_dir, "collected_data", "credit_cards_tariffs")
    os.makedirs(output_dir, exist_ok=True)

    driver = initialize_driver()
    try:
        for name_credit, url in zip(name_of_credit_card, urls):
            # Создание имени файла для сохранения информации о тарифе
            safe_name = name_credit.replace(' ', '_').replace('%', 'percent')
            file_path = os.path.join(output_dir, f"{safe_name}.txt")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f'Тарифы карты {name_credit}\n')
                parse_tariff(driver, url, file)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
