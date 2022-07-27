from urllib.request import Request
from scrap import Scrap
from data import *
import config
from rich.console import Console
import time
import re

if __name__ == '__main__':
    console = Console()
    scrap = Scrap()
    console.rule('[bold blue]Condigurando...')
    keywords = console.input('Informe o tipo de vaga, exemplo: [bold blue]Ciência de dados[/]\nSe nada for informado, usaremmos [i]Ciencia de Dados[/i] como padrão.\n')
    keywords = keywords if keywords.strip() != '' else 'Ciência de Dados'
    location = console.input('Informe o seu local, exemplo: [bold blue]São Paulo, SP[/]\nSe nada for informado, usaremos [i]São Paulo, SP[/i] como padrão.\n')
    location = location if location.strip() != '' else 'São Paulo, SP'
    limit = console.input('Qual a quantidade de links, limite de 500? [bold blue]Caso nenhum valor seja informado serão considerados 100\n')
    limit = ''.join(re.findall('\d', limit))
    limit = int(limit) if limit != '' else 500
    start_time = time.time()
    with console.status('Atualizando links'):
        scrap.load(keywords, location, limit)
    console.print(f'Links atualizados, tempo para carregar os links: [blue bold]{time.time() - start_time} segundos')
    console.rule('[bold blue]Carregando vagas')
    start_time_jobs = time.time()
    with console.status('Carregando vagas'):
        scrap.get_batch()
    console.print(f'Ótimo, está tudo [gray underline]atualizado[/], o tempo para carregar as vagas foi de: [blue bold]{time.time() - start_time_jobs} segundos')
    console.print(f'Tempo total do script: [blue bold]{time.time() - start_time} segundos')
    console.print('[bold blue]Saindo...')