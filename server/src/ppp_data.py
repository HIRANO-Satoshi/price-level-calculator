'''
  Luncho PPP data

  @author HIRANO Satoshi
  @date  2021/05/13
'''

import csv
import re
from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast
from typing_extensions import TypedDict

from src import exchange_rate
from src.types import Currency, CurrencyCode, C1000, Country, CountryCode, LunchoResult, IMF_PPP_Country

IMF_PPP_All: Dict[CountryCode, IMF_PPP_Country] = {}  # ,

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

def init() -> None:
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
        #print(str(Country_Metadata))

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

        #print(str(IMF_PPP_All))

    exchange_rate.load_exchange_rates()