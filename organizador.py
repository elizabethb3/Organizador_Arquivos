import os
import shutil
from pathlib import path
from datetime import datetime
import logging
import config


#Configurar sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/organizador.log', encoding='utf-8'),
        logging.StreamHandler() #Mostra logs no console também
    ]
)

def obter_categoria(extesao):
    #Determina a categoria de um arquivo baseado em sua extensão

    extensao = extensao.lower()

    for categoria, extensoes in config.CATEGORIAS.items():
        if extensao in extensoes:
            return categoria
        
    return config.PASTA_OUTROS

def obter_data_modificacao(caminho_arquivo):
    #Obtem a data de modificação de um arquivo

    try:
        timestamp = caminho_arquivo.stat().st_mtime
        data = datetime.fromtimestamp(timestamp)
        return f"{data.year}/{data.month:02d}" #Formato: 2024/03
    except Exception as e:
        logging.error(f"Erro aos obter data de {caminho_arquivo}:{e}")
        return None
    

def criar_pasta_destino(categoria, data=None):
    #Cria a estrutura d pastas para organização

    pasta_base = config.PASTA_MONITORADA /  categoria

    if config.ORGANIZADOR_POR_DATA and data:
        pasta_destino = pasta_base / data
    else:
        pasta_destino = pasta_base
    
    pasta_destino.mkdir(parents=True, mode=0o755)

    return pasta_destino


def mover_arquivo(origem, destino):
    #Move arquivo para pasta destino, evitando sobrescrever

    try:
        arquivo_destino = destino/ origem.name

        #Se arquivo já existe, adiciona número ao nome
        if arquivo_destino.exists():
            contador = 1
            nome_base = origem.stem #Nome sem extensão
            extensao = origem.suffix #Extensão

            while arquivo_destino.exists():
                novo_nome = f"{nome_base}_{contador}{extensao}"
                arquivo_destino = destino / novo_nome
                contador += 1
        shutil.move(str(origem), str(arquivo_destino))
        logging.info(f"✓ Movido: {origem.name} → {arquivo_destino}")
        return True
    except PermissionError as e:
        logging.error("✗ Sem permissão para mover {origem.name}: {e}")
        return False
    except Exception as e:
        logging.error(f"✗ Erro ao mover {origem.name}: {e}")
        return False
