'''
Luncho server

@author HIRANO Satoshi
@date  2020/02/28
'''

import copy
import csv
import json
import pdb
import re
import datetime
from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast
from mypy_extensions import TypedDict


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*", # "http://localhost:8082",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CountryCode = str
CurrencyCode = str

class Country(TypedDict):
    ppp: float                # PPP in local currency of currency_name
    currency_code: CurrencyCode # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    country_name: str           # Afghanistan


# ICP country metadata
#   {'AFG': { 'Code': 'AFG', 'Long NameError(Islamic State of Afghanistan,AFN: Afghani,Afghanistan,
#   {'ALB': {1980: 24.4, 1981: 24.5...
class CountryMetadata(TypedDict):
    code: CountryCode                 # AFG  (ISO 3 letter country code)
    long_name: str            # Islamic State of Afghanistan
    currency_code: CurrencyCode  # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    table_name: str           # Afghanistan
    coverage: Optional[str]   # Urban and Rural, Urban only, Rural only

country_metadata: Dict[CountryCode, CountryMetadata] = {}   # country_code, CountryMetadata

# IMF PPP data
#   {'AFG': {            1981: 17.4...
#   {'ALB': {1980: 24.4, 1981: 24.5...
class Country_IMF_PPP(TypedDict, total=False):
    year_ppp: Dict[int, float]  # { year: ppp }  Optional
    ppp: float                # PPP in local currency of currency_name
    currency_code: CurrencyCode # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    country_name: str           # Afghanistan

imf_ppp: Dict[CountryCode, Country_IMF_PPP] = {}  # ,

class FixerExchangeRate(TypedDict):
    success: bool    # true if API success
    timestamp: int   # 1605081845
    base: str        # always "EUR"
    date: str        #"2020-11-11",
    rates: Dict[str, float]   # "AED": 4.337445

fixer_exchange_rates: FixerExchangeRate = {}
exchange_rates: Dict[str, float] = {}



sdr_per_luncho = 5.0/100.0   # 100 Luncho is 5 SDR.
doller_per_sdr = 1.424900 # 1 SDR = $1.424900




@app.get("/convert-from-luncho/")
async def convert_from_luncho(country_code: CountryCode, luncho_value: float):

    in_dollar: float = 0
    local_currency_value: float = 0
    dollar_value: float = 0
    currency_code: Optional[CurrencyCode] = None

    country_imf_ppp = imf_ppp[country_code]
    currency_code = country_imf_ppp['currency_code']
    year: int = datetime.datetime.today().year
    ppp: float = country_imf_ppp['year_ppp'].get(year, None)  # country's ppp of this year
    if ppp:
        rate: Optional[float] = exchange_rates.get(currency_code, None)
        if rate is not None:
            in_dollar = luncho_value * doller_per_sdr
            local_currency_value = in_dollar * rate * ppp
            dollar_value = local_currency_value / rate
        else:
            print('Exchange rate not found: ' + country_imf_ppp['country_name'] + ' ' + country_imf_ppp['currency_name'] + '(' + currency_code + ')')
    else:
        print('PPP not found: ' + country_imf_ppp['country_name'] + ' ' + country_imf_ppp['currency_name'] + '(' + currency_code + ')')


    return {"dollar_value": local_currency_value,
            'local_currency_value': local_currency_value,
            'currency_code': currency_code,
            'country_code': country_code,
            'country_name': country_imf_ppp['country_name'],
            'currency_name': country_imf_ppp['currency_name']
    }

@app.get("/convert-from-luncho-all")
async def convert_from_luncho_all(luncho_value: float) -> List[Country_IMF_PPP]:

    lunchos = []
    for country_code in imf_ppp:  #type: CountryCode
        lunchos.append(await convert_from_luncho(country_code, luncho_value))
    return lunchos

@app.get("/countries")
async def countries() -> Country_IMF_PPP:
    imf_ppp_copy: Country_IMF_PPP = copy.deepcopy(imf_ppp)

    for country_code in imf_ppp_copy:  #type: CountryCode
        del imf_ppp_copy[country_code]['year_ppp']
    return imf_ppp_copy


@app.get("/convert-from-luncho-dummy/")
async def convert_from_luncho_dummy(currency_code: CurrencyCode, luncho_value: float) -> Dict[str, float]:
    ppp = 1.0
    if currency_code == 'USD':
        ppp = 4.81
    elif currency_code == 'JPY':
        ppp = 530
    elif currency_code == 'EURO':
        ppp = 4.40
    elif currency_code == 'CNY':
        ppp = 33.92

    return {"currency_value": luncho_value * ppp}

def init_data() -> None:
    global country_metadata, imf_ppp

    # CountryMetadata into country_metadata
    with open('data/Data_Extract_From_ICP_2017_Metadata.csv', newline='', encoding="utf_8_sig") as metadata_file:
        metadata_reader  = csv.DictReader(metadata_file)
        for data in metadata_reader:
            data['code'] = data['Code']
            del data['Code']
            data['long_name'] = data['Long Name']
            del data['Long Name']
            # decompose Currency Unit           AFN: Afghani (2011)
            currency_unit: Optional[str] = data['Currency Unit']
            data['currency_code'] = currency_unit[0:3]
            data['currency_name'] = re.sub(' \(.*?\)', '', currency_unit[5:])
            del data['Currency Unit']

            data['table_name'] = data['Table Name']
            if data['table_name'] == 'Taiwan, China':
                data['table_name'] = 'Taiwan'
            del data['Table Name']
            # coverage
            coverage: Optional[str] = data.get('Household consumption price survey: Geographical coverage')
            del data['Household consumption price survey: Geographical coverage']
            if coverage:
                data['coverage'] = coverage

            country_metadata[data['code']] = dict(data)
        print(str(country_metadata))

    # build imf_ppp: Country_IMF_PPP Implied PPP conversion rate (National currency per international dollar)
    mapping = {
        "China, People's Republic of": 'China',
        "Congo, Dem. Rep. of the": 'Congo, Dem. Rep.',
        "Congo, Republic of ": 'Congo, Rep.',
        "Egypt": 'Egypt, Arab Rep.',
        "Hong Kong SAR": 'Hong Kong SAR, China',
        "Iran": 'Iran, Islamic Rep.',
        "Korea, Republic of": 'Korea, Rep.',
        "Lao P.D.R.": 'Lao PDR',
        "Macao SAR": 'Macao SAR, China',
        "Micronesia, Fed. States of": "Micronesia, Fed. Sts.",
        "North Macedonia ": "North Macedonia",
        "Saint Kitts and Nevis": "St. Kitts and Nevis",
        "Saint Lucia": "St. Lucia",
        "Saint Vincent and the Grenadines": "St. Vincent and the Grenadines",
        "South Sudan, Republic of": "South Sudan",
        "Syria": "Syrian Arab Republic",
        "São Tomé and Príncipe": "São Tomé and Principe",
        "Taiwan Province of China": "Taiwan",
        "Venezuela": "Venezuela, RB",
        "Yemen": "Yemen, Rep.",

    }
    with open('data/imf-dm-export-20201110.csv', newline='', encoding="utf_8_sig") as imf_file:
        imf_reader  = csv.DictReader(imf_file)
        for data in imf_reader:
            table_name: str = data.get('Implied PPP conversion rate (National currency per international dollar)')
            if not table_name or not data.get('2020'):
                continue
            table_name = mapping.get(table_name, table_name)
            #pdb.set_trace()
            country_code: Optional[str] = None
            for code, metadata in country_metadata.items(): #type: str, CountryMetadata
                # print('code=' + code)
                # print('metadata = ' + str(metadata))
                if metadata['table_name'] == table_name:
                    country_code = code
            assert country_code, 'country code for ' + table_name
            ppps = {}
            for year in range(1980, 2100):
                ppp = data.get(str(year))
                if ppp is None or ppp == 'no data':
                    continue
                ppps[year] = float(ppp)
            # print(str(ppps))
            imf_ppp[country_code] = { 'year_ppp': ppps,
                                      #'ppp': ppps[datetime.datetime.today().year],
                                      'currency_code': country_metadata[country_code]['currency_code'],
                                      'currency_name': country_metadata[country_code]['currency_name'],
                                      'country_name': country_metadata[country_code]['table_name']
            }

        print(str(imf_ppp))

    with open('data/fixer-exchange-2020-11-11.json', newline='') as fixer_file:
        global fixer_exchange_rates, exchange_rates
        fixer_exchange_rates  = json.load(fixer_file)
        if fixer_exchange_rates['success']:
            pass  # XXX
        usd: float = fixer_exchange_rates['rates']['USD']  # USD per euro
        for currecy_code, euro_value in fixer_exchange_rates['rates'].items():  #type: CurrencyCode, float
            exchange_rates[currecy_code] = euro_value / usd   # store in doller
        print(str(exchange_rates))

# initialize
init_data()
