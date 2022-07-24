from os import link, listdir
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
from datetime import datetime
from rich.console import Console

from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs


import config
from data import Job, jobs_desc

class Scrap():
    def __init__(self) -> None:
        self.driver = Scrap.load_driver()
        self.jobs = self.load_jobs_file()
        self.console = Console()
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
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 1000
            if end != True:
                if ('infinite-scroller__show-more-button--visible' in button_more.get_attribute('class')) and last_height >= y:
                    try:
                        button_more.click()
                    except ElementClickInterceptedException:
                        y = 1000
                        self.driver.execute_script("window.scrollTo(0, "+str(y)+")")
            else:
                break
            if end.is_displayed():
                break
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                self.driver.execute_script("window.scrollTo(0, "+str(0)+")")
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, "+str(new_height)+")")
            time.sleep(1)
        jobs_results = self.driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
        jobs_li = jobs_results.find_elements(By.TAG_NAME, 'li')
        links = [_.find_element(By.TAG_NAME, 'a').get_attribute('href') for _ in jobs_li]
        job_links = dict.fromkeys(links, None)
        self.jobs = dict(self.jobs, **job_links)
        self.save_jobs_file()

    def get_batch(self, links = None):
        if links is None:
            links = [x for x, _ in self.jobs.items() if _ == None]
        for link in links:
            if self.jobs[link] != None:
                continue
            self.get_info(link)

    def get_info(self, url : str):
        self.driver.get(url)
        time.sleep(2)
        while self.check_is_login_page:
            self.driver.get(url)
            time.sleep(1)
        self.jobs[url] = self.get_job_info()

    def get_job_info(self) -> Job:
        job = Job()
        job.datetime = datetime.now()
        job.url = self.driver.current_url
        job.job_title = self.get_element(By.CLASS_NAME, 'top-card-layout__title', 'text')
        elm_company = self.get_element(By.CLASS_NAME, 'topcard__org-name-link')
        if elm_company is None:
            job.company_name = None
            job.company_url = None
        else:
            job.company_name = elm_company.text
            job.company_url = elm_company.get_attribute('href')
        job.time_post = self.get_element(By.CLASS_NAME, 'posted-time-ago__text', 'text')
        elm_criteria = self.get_element(By.CLASS_NAME, 'description__job-criteria-list')
        elm_experience = self.get_element(By.XPATH, "//*[contains(text(), 'Nível de experiência')]",False, elm_criteria)
        job.experience_level = self.get_sibling(elm_experience, 'span', 'text')
        elm_type = self.get_element(By.XPATH, "//*[contains(text(), 'Tipo de emprego')]")
        job.type_job = self.get_sibling(elm_type, 'span', 'text')
        elm_func = self.get_element(By.XPATH, "//*[contains(text(), 'Função')]")
        job.function = self.get_sibling(elm_func, 'span', 'text')
        elm_sector = self.get_element(By.XPATH, "//*[contains(text(), 'Setores')]")
        job.sector = self.get_sibling(elm_sector, 'span', 'text')
        desc = self.get_element(By.CLASS_NAME, 'description__text')
        if desc is None:
            job.description = None
        else:
            job.description = desc.get_attribute('innerHTML')
        return job



    
    def get_sibling(self, element, sibling_tag, get_=False):
        return self.get_element(By.XPATH, f'./following-sibling::{sibling_tag}', get_, element, True)


    def get_element(self, by, element_text, get_ = False, element = False, single=True):
        if element is False:
            element = self.driver
        try:
            if single is True:
                elm = element.find_element(by, element_text)
            else:
                elm = element.find_elements(by, element_text)
        except Exception as e:
            self.console.log(f'Erro no elemento [bold red]{element_text}')
            return None
        else:
            if get_ is False:
                return elm
            return getattr(elm, get_)
    @property
    def check_is_login_page(self) -> bool:
        try:
            div_login = self.driver.find_element(By.CLASS_NAME, 'join-form__form-input-container')
            div_login.find_element(By.CLASS_NAME, 'input__input')
            return True
        except Exception:
            return False
        return True

    @property
    def check_user_not_logged(self) -> bool:
        self.driver.get(config.url_login)
        return self.check_is_login_page
    
    
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