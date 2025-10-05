import os
from pathlib import Path


PASTA_MONITORADA = Path.home() / "Downloads"
CATEGORIAS = {
    'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
    'Documentos': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.odt', '.ods'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
    'Musicas': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
    'Compactados': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.deb'],
    'Programas': ['.deb', '.rpm', '.appimage', '.snap'],
    'Scripts': ['.py', '.sh', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h'] 
}

PASTA_OUTROS = 'Outros'
ORGANIZADOR_POR_DATA = True
