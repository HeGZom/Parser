from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
download_directory = "C:\\Users\\Глеб\\PycharmProjects\\parse\\parse_credit\\pdf_doc_for_credit"  # Убедитесь, что эта директория существует




chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "plugins.always_open_pdf_externally": True   #для того чтобы скачивать не только doc файлы но и пдф
})

chrome_service = Service(executable_path='C:\\chromedriver\\chromedriver.exe')

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get("https://www.rsb.ru/credits/#tariffs")

# Найти все ссылки на PDF-документы
pdf_links = driver.find_elements(By.CSS_SELECTOR, "a.link.link_doc")

# Сохранение URL-ов PDF-документов
pdf_urls = [link.get_attribute("href") for link in pdf_links]


for pdf_url in pdf_urls:
    driver.get(pdf_url)
    print(f"Файл успешно скачан с URL: {pdf_url}")

driver.quit()
