from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_path = "C:\\chromedriver\\chromedriver.exe"  # путь к chrome driver

urls = ['https://www.rsb.ru/cards/mir-130/#tariff',
        'https://www.rsb.ru/cards/mir/#tariff',
        'https://www.rsb.ru/cards/mc-platinum/#tariff',
        'https://www.rsb.ru/cards/mc-black/#tariff',
        'https://www.rsb.ru/cards/mir-supreme/#tariff',
        'https://www.rsb.ru/cards/union-pay/#tariff'
]

name_of_credit_card = [ '130 дней без %',
                        '\'Мир\'','Platinum',
                        'Black', 'Mir Supreme',
                        'Кредитная карта UnionPay'
]
def parsing_tariff(url):

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".tariff-cell"))
        )

        tariff_blocks = driver.find_elements(By.CSS_SELECTOR, ".tariff-cell_block")

        for block in tariff_blocks:
            title = block.find_element(By.CLASS_NAME, "header_line").text  # Заголовок блока
            print(f"Тарифы Карты {url.split('/')[4]}: {title}")

            # Находим финансовые условия и элементы с классом 'tariff-cell_row_no-border'
            conditions = block.find_elements(By.CSS_SELECTOR, ".tariff-cell_row, .tariff-cell_row_no-border, .font_18 block_mb_10 header_line, .row")

            for condition in conditions:

                try:
                    condition_title_elem = condition.find_element(By.CLASS_NAME, "col-sm-7")

                    condition_title = condition_title_elem.text
                    # if not condition_title:
                    #     condition_title = condition_title_elem.

                    condition_value_elem = condition.find_element(By.CLASS_NAME, "col-sm-4")
                    condition_value = condition_value_elem.text if condition_value_elem else "Нет значения"

                    print(f"{condition_title}: {condition_value}")

                except:
                    continue

    finally:
        driver.quit()

for name_credit, url in zip(name_of_credit_card, urls):
    print('-' * 25)
    print(f'Тарифы карты {name_credit}')
    parsing_tariff(url)