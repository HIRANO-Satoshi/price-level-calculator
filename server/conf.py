'''
  Configuration of the Luncho server

  @author HIRANO Satoshi
  @since 2021/05/12
'''

from __future__ import annotations
import os

# Configurable constants
GCS_BUCKET: str | None = os.environ.get('GCS_BUCKET', None)
FIXER_API_KEY: str | None = os.environ.get('FIXER_API_KEY', None)

FIXER_URLS          = ['http://data.fixer.io/api/']
FREE_EXCHANGERATE_URLS = ['https://api-us.exchangerate.host/', 'https://api.exchangerate.host/', 'https://api-eu.exchangerate.host/']
EXCHANGERATE_URLS   = FIXER_URLS + FREE_EXCHANGERATE_URLS if FIXER_API_KEY else FREE_EXCHANGERATE_URLS

DUMMY_FIXER_EXCHANGE_FILE = 'data/dummy-fixer-exchange-2020-11-11.json'

# Luncho client library languages
#  'language': 'option'
#
#  Set some from https://openapi-generator.tech/docs/generators
#
Gen_Openapi: dict[str, str] = {
    # add library=asyncio if needed, otherwise it uses default (library=urllib3)
    'python': 'packageName=luncho_python,projectName=luncho_python',
    'typescript-fetch': 'supportsES6=true,npmName=luncho-typescript-fetch,withoutRuntimeChecks=true',
    #'typescript-aurelia': 'supportsES6=true,npmName=luncho_typescript-aurelia',
}


def Header_To_Fetch(lang: str) -> dict:
    return {"Accept-Language": "".join([lang, ";"]), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}


# Unconfigurable constants

SDR_PER_LUNCHO: float     = 5.0/100.0      # 100 Luncho is 5 SDR.
API_V1_STR: str = "/v1"
IS_APPENGINE   = os.environ.get('GAE_APPLICATION') is not None  # True if running on Google App Engine

Openapi_Schema_File = 'data/openapi_schema.json'
