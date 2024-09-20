from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Указываем путь к драйверу
chrome_driver_path = "C:\\chromedriver\\chromedriver.exe"  # путь к chrome driver

# Настраиваем опции Chrome
#chrome_options = Options()
#chrome_options.add_argument("--headless")  # Запуск без открытия окна браузера (если нужно)

# Создаем экземпляр драйвера
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service) #, options=chrome_options


url = 'https://www.rsb.ru/cards/credit/'
driver.get(url)


# Пример поиска элемента по классу
cards = driver.find_elements(By.CLASS_NAME, "cards")

for card in cards:
    title = card.find_element(By.TAG_NAME, "h3").text  # Пример поиска заголовка
    description = card.find_element(By.CLASS_NAME, "description").text  # Пример поиска описания
    print(f"Название: {title}, Описание: {description}")
driver.quit()