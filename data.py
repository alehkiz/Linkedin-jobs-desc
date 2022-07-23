from dataclasses import dataclass, field
from typing import Dict, List

@dataclass(eq=True)
class Job:
    url: str = None
    description : str = None
    company_url : str = None
    company_name : str = None
    time_post : str = None
    job_title : str = None
    experience_leve : str = None
    type_job : str = None
    function : str = None
    sector : str = None
    code:str = None



jobs_desc = {}