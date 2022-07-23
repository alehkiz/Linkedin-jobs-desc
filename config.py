url = 'https://www.linkedin.com'

url_search = 'https://www.linkedin.com/jobs/search/?'

url_search_params = {'keywords':'', 'location':''}

work_format = {'f_WT':''}
'''
    f_WT -> Formato de trabalho;
        1 == Presencial
        2 == Remoto
        3 == Hibrido
        '''
url_login = 'https://www.linkedin.com/login/'


jobs_file = 'data/jobs.pkl' # O arquivo deve ser um dicionário com o seguinte formato: {url: Job}
