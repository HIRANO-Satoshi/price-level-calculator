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
class CountryMetadataType(TypedDict):
    code: CountryCode                 # AFG  (ISO 3 letter country code)
    long_name: str            # Islamic State of Afghanistan
    currency_code: CurrencyCode  # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    table_name: str           # Afghanistan
    coverage: Optional[str]   # Urban and Rural, Urban only, Rural only

Country_Metadata: Dict[CountryCode, CountryMetadataType] = {}   # country_code, CountryMetadataType

# IMF PPP data
#   {'AFG': {            1981: 17.4...
#   {'ALB': {1980: 24.4, 1981: 24.5...
class IMF_PPP_Country(TypedDict, total=False):
    year_ppp: Dict[int, float]  # { year: ppp }  Optional
    ppp: float                # PPP in local currency of currency_name
    currency_code: CurrencyCode # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    country_name: str           # Afghanistan

IMF_PPP_All: Dict[CountryCode, IMF_PPP_Country] = {}  # ,

class FixerExchangeRate(TypedDict):
    success: bool    # true if API success
    timestamp: int   # 1605081845
    base: str        # always "EUR"
    date: str        #"2020-11-11",
    rates: Dict[str, float]   # "AED": 4.337445

Fixer_Exchange_Rates: FixerExchangeRate = {}
Exchange_Rates: Dict[str, float] = {}



SDR_Per_Luncho = 5.0/100.0   # 100 Luncho is 5 SDR.
Doller_Per_SDR = 1.424900 # 1 SDR = $1.424900




@app.get("/convert-from-luncho/")
async def convert_from_luncho(country_code: CountryCode, luncho_value: float):

    dollar_per_luncho: float = 0
    local_currency_value: float = 0
    dollar_value: float = 0
    exchange_rate: Optional[float] = 0
    currency_code: Optional[CurrencyCode] = None

    IMF_PPP_this_country = IMF_PPP_All[country_code]
    currency_code = IMF_PPP_this_country['currency_code']
    year: int = datetime.datetime.today().year
    ppp: float = IMF_PPP_this_country['year_ppp'].get(year, None)  # country's ppp of this year
    if ppp:
        exchange_rate = Exchange_Rates.get(currency_code, None)
        if exchange_rate is not None:
            #breakpoint()
            dollar_per_luncho = Doller_Per_SDR * SDR_Per_Luncho
            local_currency_value = dollar_per_luncho * ppp * luncho_value
            dollar_value = local_currency_value / exchange_rate
        else:
            print('Exchange rate not found: ' + IMF_PPP_this_country['country_name'] + ' ' + IMF_PPP_this_country['currency_name'] + '(' + currency_code + ')')
    else:
        print('PPP not found: ' + IMF_PPP_this_country['country_name'] + ' ' + IMF_PPP_this_country['currency_name'] + '(' + currency_code + ')')


    return {"dollar_value": dollar_value,
            'local_currency_value': local_currency_value,
            'currency_code': currency_code,
            'country_code': country_code,
            'country_name': IMF_PPP_this_country['country_name'],
            'currency_name': IMF_PPP_this_country['currency_name'],
            'ppp': ppp,
            'dollar_per_luncho': dollar_per_luncho,
            'exchange_rate': exchange_rate
    }

@app.get("/convert-from-luncho-all")
async def convert_from_luncho_all(luncho_value: float) -> List[IMF_PPP_Country]:

    lunchos = []
    for country_code in IMF_PPP_All:  #type: CountryCode
        lunchos.append(await convert_from_luncho(country_code, luncho_value))
    return lunchos

@app.get("/countries")
async def countries() -> IMF_PPP_Country:
    IMF_PPP_All_copy: Dict[CountryCode, IMF_PPP_Country] = copy.deepcopy(IMF_PPP_All)

    for country_code in IMF_PPP_All_copy:  #type: CountryCode
        del IMF_PPP_All_copy[country_code]['year_ppp']
    return IMF_PPP_All_copy


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
    global Country_Metadata, IMF_PPP_All

    # CountryMetadataType into Country_Metadata
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

            Country_Metadata[data['code']] = dict(data)
        print(str(Country_Metadata))

    # build IMF_PPP_All: IMF_PPP_Country Implied PPP conversion rate (National currency per international dollar)
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
            for code, metadata in Country_Metadata.items(): #type: str, CountryMetadataType
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
            IMF_PPP_All[country_code] = { 'year_ppp': ppps,
                                      #'ppp': ppps[datetime.datetime.today().year],
                                      'currency_code': Country_Metadata[country_code]['currency_code'],
                                      'currency_name': Country_Metadata[country_code]['currency_name'],
                                      'country_name': Country_Metadata[country_code]['table_name']
            }

        print(str(IMF_PPP_All))

    with open('data/fixer-exchange-2020-11-11.json', newline='') as fixer_file:
        global Fixer_Exchange_Rates, Exchange_Rates
        Fixer_Exchange_Rates  = json.load(fixer_file)
        if Fixer_Exchange_Rates['success']:
            pass  # XXX
        usd: float = Fixer_Exchange_Rates['rates']['USD']  # USD per euro
        for currecy_code, euro_value in Fixer_Exchange_Rates['rates'].items():  #type: CurrencyCode, float
            Exchange_Rates[currecy_code] = euro_value / usd   # store in doller
        print(str(Exchange_Rates))

# initialize
init_data()
