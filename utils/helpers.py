import os
from datetime import datetime
from flask import flash

def allowed_file(filename):
    """
    Verifica se o arquivo tem uma extensão permitida.
    :param filename: Nome do arquivo a ser verificado.
    :return: True se a extensão é permitida, False caso contrário.
    """
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'ppt', 'pptx', 'mp4', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, upload_folder):
    """
    Salva o arquivo na pasta especificada.
    :param file: Arquivo a ser salvo.
    :param upload_folder: Pasta onde o arquivo será salvo.
    :return: Caminho do arquivo salvo.
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    else:
        flash("Arquivo não permitido ou inválido.")
        return None

def format_datetime(dt):
    """
    Formata um objeto datetime para uma string legível.
    :param dt: Objeto datetime a ser formatado.
    :return: String formatada.
    """
    return dt.strftime("%d/%m/%Y %H:%M")

def get_current_time():
    """
    Retorna a data e hora atual.
    :return: Objeto datetime atual.
    """
    return datetime.now()

# Exemplo de uso
if __name__ == "__main__":
    # Testando a função format_datetime
    now = get_current_time()
    print("Data e hora atual:", format_datetime(now))
