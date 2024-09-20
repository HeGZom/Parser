from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Указываем путь к драйверу
chrome_driver_path = "C:\\chromedriver\\chromedriver.exe"  # путь к chrome driver

# Создаем экземпляр драйвера
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

#url = 'https://www.rsb.ru/cards/mir-130/#tariff'
url = 'https://www.rsb.ru/cards/mir/#tariff'
driver.get(url)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tariff-cell"))
    )

    tariff_blocks = driver.find_elements(By.CLASS_NAME, "tariff-cell_block")

    additional_tariff_blocks = driver.find_elements(By.CLASS_NAME, "tariff-cell_block block_mb_60")

    for block in tariff_blocks:
        title = block.find_element(By.CLASS_NAME, "header_line").text  # Заголовок блока
        print(f"Заголовок: {title}")

        conditions = block.find_elements(By.CLASS_NAME, "tariff-cell_row")


        for condition in conditions:

            condition_title_elem = condition.find_element(By.CLASS_NAME, "color-gray")
            if condition_title_elem:
                condition_title = condition_title_elem.text

                condition_values = condition.find_elements(By.TAG_NAME, "span")
                if not condition_values:
                    condition_values = condition.find_elements(By.TAG_NAME, "sapn")
                condition_value = " ".join(
                    [value.text for value in condition_values]) if condition_values else "Нет значения"

                print(f"{condition_title}: {condition_value}")

    for block in additional_tariff_blocks:
        title = block.find_element(By.CLASS_NAME, "header_line").text #ищем заголовок

        print(f'Заголовок: {title}')

        conditions = block.find_element(By.CLASS_NAME, "tariff-cell_row_no-border")


finally:
    driver.quit()
