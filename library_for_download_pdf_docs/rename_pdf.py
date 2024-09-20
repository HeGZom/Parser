import os
import re

def rename_pdf(dir_path,documents):
    """
        Переименовывает PDF-документы в указанной директории на основании предоставленного словаря.

        :param dir_path: Путь к директории, содержащей PDF-документы для переименования.
        :param documents: Словарь, где ключи — это старые имена файлов, а значения — новые имена файлов.
                          Имена файлов будут очищены от запрещённых символов и пробелов.
        """
    invalid_chars = r'[<>:"/\\|?*]'  # Запрещённые символы для файлового пути

    def clean_filename(filename):
        filename = re.sub(invalid_chars, '', filename)
        filename = filename.replace(' ', '_')
        return filename

    def delete_tmp_files(dir_path, file):
            try:
                os.remove(os.path.join(dir_path, file))
                print(f"Удален временный файл: {file}")
            except OSError as e:
                print(f"Ошибка при удалении файла {file}: {e}")

    documents = {clean_filename(key): clean_filename(value) for key, value in documents.items()}

    for file in os.listdir(dir_path):
        try:
            format_file = file.split(".")[1]
            os.rename(os.path.join(dir_path, file), os.path.join(dir_path, f'{documents[file]}.{format_file}'))

        except Exception as e:
            print('Нашелся временный файл')
            delete_tmp_files(dir_path,file)
