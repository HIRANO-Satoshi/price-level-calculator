'''
  Configuration of the Luncho server

  Author: HIRANO Satoshi
  Date: 2021/05/12
'''
from typing import List, Dict, Tuple, Union, Any, Optional

Openapi_Schema_File = 'data/openapi_schema.json'
Gen_Openapi = {
               'typescript-aurelia': 'supportsES6=true',
               'typescript-fetch': 'supportsES6=true',
               'python': ''
}

def Header_To_Fetch(lang: str) -> Dict:
    return {"Accept-Language": "".join([lang, ";"]), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}