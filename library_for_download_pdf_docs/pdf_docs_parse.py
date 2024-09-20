from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def download_pdf_docs(url, download_dir,driver_path):
    """
        Скачивает PDF-документ по указанному URL в заданную директорию.

        :param url: URL документа для скачивания
        :param download_dir: Путь к директории, куда будет сохранен файл
        :param driver_path: Путь к google driver
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "plugins.always_open_pdf_externally": True   #для того чтобы скачивать не только doc файлы но и пдф
    })

    chrome_service = Service(executable_path=driver_path)

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.get(url)

    pdf_links = driver.find_elements(By.CSS_SELECTOR, "a.link.link_doc")

    pdf_urls = [link.get_attribute("href") for link in pdf_links]


    for pdf_url in pdf_urls:
        driver.get(pdf_url)
        print(f"Файл успешно скачан с URL: {pdf_url}")

    driver.quit()
