import os

class Config:
    # Chave secreta para segurança da sessão e de formulários
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')

    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pasta para armazenamento de uploads
    UPLOAD_FOLDER = os.path.join('static', 'uploads')

    # Tamanho máximo do arquivo de upload (exemplo: 16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Configurações adicionais
    SESSION_COOKIE_SECURE = True  # Recomendado para produção (SSL habilitado)
    REMEMBER_COOKIE_DURATION = 7 * 24 * 60 * 60  # Lembrar sessão por 7 dias

# Exportar a classe Config para ser usada pela aplicação Flask
config = Config()
