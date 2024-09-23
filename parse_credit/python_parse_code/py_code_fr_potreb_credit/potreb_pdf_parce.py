from library_for_download_pdf_docs.pdf_docs_parse import download_pdf_docs
from config import local_path_chrome_driver
import os
from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]

download_directory = os.path.join(project_dir, "collected_data", "pdf_doc_for_potreb_credit")
driver_path= local_path_chrome_driver
url = "https://www.rsb.ru/potrebitelskiy-kredit/#documents"

download_pdf_docs(url, download_directory,driver_path)





