from os import listdir
from os.path import isfile
import pickle
import time
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs


import config
from data import Job, jobs_desc

class Scrap():
    def __init__(self) -> None:
        self.driver = Scrap.load_driver()
        self.jobs = self.load_jobs_file()
    def load(self, keywords = "Ciência de Dados", location = "Sao Paulo, SP"):
        """Recupera os links de vagas de acordo com `keywords` e `location`

        Raises:
            Exception: 

        Returns:
            None: Salva os arquivos em `config.jobs_file`
        """
        search_params = config.url_search_params
        search_params['keywords'] = keywords
        search_params['location'] = location
        self.driver.get(self.change_query_string_on_url(config.url_search, search_params))
        y = 1000
        try:
            end = self.driver.find_element(By.XPATH, value="//*[contains(text(), 'Você viu todas as vagas para esta pesquisa')]")
            button_more = self.driver.find_element(By.CLASS_NAME, 'infinite-scroller__show-more-button')
        except NoSuchElementException as e:
            print("Não há mais vagas")
            end=True
        while True:
            self.driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 1000
            if end != True:
                if 'infinite-scroller__show-more-button--visible' in button_more.get_attribute('class'):
                    try:
                        button_more.click()
                    except ElementClickInterceptedException:
                        print('Erro no botão')
                        y = 1000
                        self.driver.execute_script("window.scrollTo(0, "+str(y)+")")
            else:
                print('Final')
                break
            if end.is_displayed():
                print('final')
                break
            time.sleep(1)
        jobs_results = self.driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
        jobs_li = jobs_results.find_elements(By.TAG_NAME, 'li')
        # jobs_li.find_element(By.CLASS_NAME, 'base-card__full-link')

        links = [_.find_element(By.TAG_NAME, 'a').get_attribute('href') for _ in jobs_li]

        job_links = dict.fromkeys(links, None)

        self.jobs = dict(self.jobs, **job_links)

        self.save_jobs_file()
        

    @property
    def check_user_logged(self) -> bool:
        self.driver.get(config.url_login)
        try:
            usernmame = self.driver.find_element(By.ID, 'username')
            if usernmame.tag_name == 'input':
                return False
        except Exception:
            return True
        return False

    
    
    def change_query_string_on_url(self, url : str, query_params: dict):
        """Add to a `url` the `query_params`

        Args:
            url (str): The new `url` with params
        """
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query = parse_qs(query_string)
        if 'pagina' in query.keys():
            query.pop('pagina')
        query = dict(**query, **query_params)
        query_encoded = urlencode(query, doseq=True)
        return urlunsplit((scheme, netloc, path, query_encoded, fragment))
    
    @staticmethod
    def load_driver(file_path: str = None) :
        driver = False
        if file_path is None:
            files = [x for x in listdir() if '.exe' in x]
            for file in files:
                try:
                    if 'gecko' in file:
                        webdriver = Firefox
                        options = FirefoxOptions()
                        options.add_argument('--log-level=3')
                        service = FirefoxService(file)
                        driver = webdriver(service=service, options=options)
                        break
                    elif 'chrome' in file:
                        webdriver = Chrome
                        options = ChromeOptions()
                        options.add_argument('--log-level=3')
                        service = ChromeService(file)
                        driver = webdriver(service=service, options=options)
                        break
                except Exception as e:
                    print('Houve um erro no carregamento do driver')
                    print(e)
        if driver is False:
            raise Exception('Não há nenhum driver instalado, acesse https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/ para detalhes sobre drivers do novegador, e baixa de acordo com o seu navegador.')
        return driver
    
    def save_jobs_file(self):

        _temp = self.jobs
        self.jobs = self.load_jobs_file()
        self.jobs = dict(self.jobs, **_temp)
        if not isfile(config.jobs_file):
            with open(config.jobs_file, 'w+') as f:
                ...
        with open(config.jobs_file, 'wb') as f:
            pickle.dump(self.jobs, f)

    def load_jobs_file(self):
        if not isfile(config.jobs_file):
            return jobs_desc
        with open(config.jobs_file, 'rb') as f:
            try: 
                return pickle.load(f)
            except EOFError as e:
                EOFError('Arquivo vazio', e)