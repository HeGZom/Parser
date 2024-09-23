#local_path_chrome_driver = "C:\\chromedriver\\chromedriver.exe" #Поменять на свою локальную папку на chromedriver
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_driver_path():
    # ChromeDriverManager автоматически загружает и возвращает путь к chromedriver
    driver_path = ChromeDriverManager().install()
    return driver_path

local_path_chrome_driver = get_chrome_driver_path()



#print(local_path_chrome_driver)


# def get_chrome_driver_path():
#     # ChromeDriverManager автоматически загружает и возвращает путь к chromedriver
#     driver_path = ChromeDriverManager().install()
#     return driver_path
#
# # Пример использования функции:
# chrome_driver_path = get_chrome_driver_path()
# print("Путь к ChromeDriver:", chrome_driver_path)