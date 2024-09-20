from library_for_download_pdf_docs.pdf_docs_parse import download_pdf_docs
from config import local_path_chrome_driver,local_path_project
import os

download_directory = os.path.join(local_path_project, "parse_credit", "collected_data", "pdf_doc_for_credit")
driver_path= local_path_chrome_driver
url = "https://www.rsb.ru/credits/#tariffs"


download_pdf_docs(url, download_directory,driver_path)





