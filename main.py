from urllib.request import Request
from scrap import Scrap
from data import *
import config
from rich.console import Console
import time

if __name__ == '__main__':
    console = Console()
    scrap = Scrap()
    console.rule('[bold blue]Condigurando...')
    keywords = console.input('Informe o tipo de vaga, exemplo: [bold blue]Ciência de dados[/]\nSe nada for informado, usaremmos [i]Ciencia de Dados[/i] como padrão.')
    keywords = keywords if keywords.strip() != '' else 'Ciência de Dados'
    location = console.input('Informe o seu local, exemplo: [bold blue]São Paulo, SP[/]\nSe nada for informado, usaremos [i]São Paulo, SP[/i] como padrão.')
    location = location if location.strip() != '' else 'São Paulo, SP'
    # console.print('Atualizando links')
    start_time = time.time()
    with console.status('Atualizando links'):
        scrap.load(keywords, location)
    console.print(f'Links atualizados, tempo para carregar os links: [blue bold]{time.time() - start_time} segundos')
    console.rule('[bold blue]Carregando vagas')
    start_time_jobs = time.time()
    with console.status('Carregando vagas'):
        scrap.get_batch()
    console.print(f'Ótimo, está tudo [gray underline]atualizado[/], o tempo para carregar as vagas foi de: [blue bold]{time.time() - start_time_jobs} segundos')
    console.print(f'Tempo total do script: [blue bold]{time.time() - start_time} segundos')
    console.print('[bold blue]Saindo...')