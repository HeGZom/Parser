from library_for_download_pdf_docs.pdf_docs_parse import download_pdf_docs


download_directory = "C:\\Users\\Глеб\\PycharmProjects\\parse\\parse_credit\\collected_data\\pdf_doc_for_credit"  # Убедитесь, что эта директория существует
driver_path='C:\\chromedriver\\chromedriver.exe'
url = "https://www.rsb.ru/credits/#tariffs"


download_pdf_docs(url, download_directory,driver_path)
