import os
from pathlib import Path
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Путь к основной директории
directory = Path(__file__).resolve().parents[0]

# Папка с исходными файлами и папка для сохранения PDF
dir_all_data = 'all_info_about_bank'
path_all_data = os.path.join(directory, dir_all_data)

if not os.path.exists(path_all_data):
    os.makedirs(path_all_data)

# Регистрация шрифта для поддержжки русского
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

def convert_txt_to_pdf(txt_file_path, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    c.setFont("Arial", 12)

    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        text_y = 750
        for line in txt_file:
            c.drawString(100, text_y, line.strip())
            text_y -= 15

    c.save()

for root, dirs, files in os.walk(directory):
    if root.split(os.sep)[-1] == 'credit_cards_tariffs':
        continue

    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith('.txt'):
            output_pdf_path = os.path.join(path_all_data, file.replace('.txt', '.pdf'))
            convert_txt_to_pdf(file_path, output_pdf_path)

        elif file.endswith('.pdf'):
            output_pdf_path = os.path.join(path_all_data, file)
            if file_path != output_pdf_path:
                shutil.copy(file_path, path_all_data)

