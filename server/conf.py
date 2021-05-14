'''
  Configuration of the Luncho server

  Author: HIRANO Satoshi
  Date: 2021/05/12
'''
from typing import List, Dict, Tuple, Union, Any, Optional

# Luncho client library languages
#  'language': 'option'
#
#  Set some from https://openapi-generator.tech/docs/generators
#
#  'typescript-aurelia' is always generated as well.
Gen_Openapi: Dict[str, str] = {
    'python': '',
    #'typescript-aurelia': 'supportsES6=true,npmName=luncho',
    'typescript-aurelia': 'supportsES6=true,npmName=luncho-typescript-aurelia',
    'typescript-fetch': 'supportsES6=true,npmName=luncho-typescript-fetch',
}

Openapi_Schema_File = 'data/openapi_schema.json'

def Header_To_Fetch(lang: str) -> Dict:
    return {"Accept-Language": "".join([lang, ";"]), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
