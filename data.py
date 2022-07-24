from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from bs4 import BeautifulSoup as BS

@dataclass(eq=True, repr=False)
class Job:
    url: str = None
    _description : str = None
    company_url : str = None
    company_name : str = None
    time_post : str = None
    job_title : str = None
    experience_level : str = None
    type_job : str = None
    function : str = None
    sector : str = None
    code:str = None
    datetime:datetime = None
    
    def __repr__(self) -> str:
        return f'{self.__class__.__qualname__}({self.job_title})'
    
    @property
    def description(self):
        _soup = BS(self._description, 'html.parser')
        return _soup.text
    @description.setter
    def description(self, value):
        self._description = value
    @description.deleter
    def description(self):
        del self._description

    def check_all_none(self):
        return all([getattr(self, x) == None for x in self.__annotations__.keys()])


jobs_desc = {}