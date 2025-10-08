import os
import shutil
from pathlib import Path
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

def obter_categoria(extensao):
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
    
    pasta_destino.mkdir(parents=True, exist_ok=True, mode=0o755)

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
        logging.error(f"✗ Sem permissão para mover {origem.name}: {e}")
        return False
    except Exception as e:
        logging.error(f"✗ Erro ao mover {origem.name}: {e}")
        return False

def organizar_arquivos():
    #Função principal que organiza todos os arquivos da pasta monitorada

    pasta = config.PASTA_MONITORADA

    if not pasta.exists():
        logging.error(f"Pasta não encontrada: {pasta}")
        return
    
    #Verificar permissões de leitura
    if not os.access(pasta, os.R_OK):
        logging.error(f"Sem permisão de leitura em: {pasta}")
        return
    
    logging.info(f"Iniciando organização de: {pasta}")
    logging.info('=' * 50)

    arquivos_movidos = 0
    arquivos_ignorados = 0

    #Listar arquivos (não pastas)
    for item in pasta.iterdir():
        if item.is_file():
            #ignorar arquivos ocultos
            if item.name.startswith('.'):
                continue

            extensao = item.suffix

            if not extensao:
                logging.warning(f"Ignorado (sem extensão): {item.name}")
                arquivos_ignorados +=1
                continue
            #Determinar categoria e pasta de destino 
            categoria = obter_categoria(extensao)
            data = obter_data_modificacao(item) if config.ORGANIZADOR_POR_DATA else None
            pasta_destino = criar_pasta_destino(categoria, data)

            #Mover aquivo
            if mover_arquivo(item, pasta_destino):
                arquivos_movidos +=1
            else:
                arquivos_ignorados +=1

    #Resumo final
    logging.info("=" * 50)
    logging.info(f"Organização concluída!")
    logging.info(f"Arquivos movidos: {arquivos_movidos}")
    logging.info(f"Arquivos ignorados: {arquivos_ignorados}")


if __name__ == "__main__" :
#Ponto de entrada do script
    
    print("Organizador Automático de Arquivos - Ubuntu")
    print(f"Pasta: {config.PASTA_MONITORADA}")
    print("-" * 50)

try:
    organizar_arquivos()
except KeyboardInterrupt:
    print("\nOperação cancelada pelo usuário")
except Exception as e:
    logging.error(f"Erro inesperado: {e}")

print("-" * 50)
print("Processo finalizado! Verifique os logs para detalhes.")