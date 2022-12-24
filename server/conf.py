'''
  Configuration of the Luncho server

  Author: HIRANO Satoshi
  Date: 2021/05/12
'''
import os
from typing import List, Dict, Tuple, Union, Any, Optional

# Configurable constants

Use_Fixer_For_Forex: bool = False          # True to use Fixer.io for exchange rates. Set api_keys.py.

Fixer_URL          = 'http://data.fixer.io/api/'
Free_Exchangerate_URL   = 'https://api.exchangerate.host/'
Exchangerate_URL   = Fixer_URL if Use_Fixer_For_Forex else Free_Exchangerate_URL

Dummy_Fixer_Exchange_File = 'data/dummy-fixer-exchange-2020-11-11.json'
Last_Fixer_Exchange_File  = 'data/exchange-last.json'

# Luncho client library languages
#  'language': 'option'
#
#  Set some from https://openapi-generator.tech/docs/generators
#
Gen_Openapi: Dict[str, str] = {
    # add library=asyncio if needed, otherwise it uses default (library=urllib3)
    'python': 'packageName=luncho_python,projectName=luncho_python',
    'typescript-fetch': 'supportsES6=true,npmName=luncho-typescript-fetch,withoutRuntimeChecks=true',
    #'typescript-aurelia': 'supportsES6=true,npmName=luncho_typescript-aurelia',
}


def Header_To_Fetch(lang: str) -> Dict:
    return {"Accept-Language": "".join([lang, ";"]), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}


# Unconfigurable constants

SDR_Per_Luncho: float     = 5.0/100.0      # 100 Luncho is 5 SDR.
API_V1_STR: str = "/v1"
Is_AppEngine   = os.environ.get('GAE_APPLICATION') is not None  # True if running on Google App Engine

Openapi_Schema_File = 'data/openapi_schema.json'
