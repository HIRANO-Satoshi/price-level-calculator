'''
  Luncho PPP data

  @author HIRANO Satoshi
  @date  2021/05/13
'''

import csv
import logging
import os
import re
import datetime
from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast
from typing_extensions import TypedDict
import pycountry
import pycountry_convert

from conf import SDR_Per_Luncho
#from src import exchange_rate
from src.types import Currency, CurrencyCode, C1000, CountryCode, LunchoData, Country
from src.utils import error

Countries: Dict[CountryCode, Country] = {}      # A map of country data
CountryCode_Names: Dict[CountryCode, str] = {}  # A map of country code and name

# ICP country metadata
#   {'AFG': { 'Code': 'AFG', 'Long NameError(Islamic State of Afghanistan,AFN: Afghani,Afghanistan,
#   {'ALB': {1980: 24.4, 1981: 24.5...
class CountryMetadataType(TypedDict):
    code: CountryCode         # AF  (ISO 2 letter country code)
    name: str                 # Afghanistan (common name in pycountry)
    long_name: str            # Islamic State of Afghanistan (not used)
    currency_code: CurrencyCode  # AFN  (ISO 3 letter currency code)
    currency_name: str        # Afghani
    table_name: str           # Afghanistan
    coverage: Optional[str]   # Urban and Rural, Urban only, Rural only

Country_Metadata: Dict[CountryCode, CountryMetadataType] = {}   # country_code, CountryMetadataType

kosovo = pycountry.db.Data()
kosovo.alpha_2 = "XK"
kosovo.alpha_3 = "KSV"
kosovo.name = "Kosovo"
kosovo.numeric = "383"
kosovo.official_name = "Kosovo"

def init(use_dummy_data: bool) -> None:
    global Country_Metadata, Countries, CountryCode_Names

    if not os.getcwd().endswith('server') and not os.environ.get('GAE_APPLICATION'):
        os.chdir("server");

    # read country metadata to build Country_Metadata map
    with open('data/Data_Extract_From_ICP_2017_Metadata.csv', newline='', encoding="utf_8_sig") as metadata_file:
        metadata_reader  = csv.DictReader(metadata_file)
        country_data: Any

        # 215 countries and regions in the file
        for data in metadata_reader:
            country_code3 = data['Code']     # ISO 3 letter code
            del data['Code']
            if country_code3 == 'BON': # bonaire, but not found in IMF PPP data
                country_code3 = 'BES';
            if country_code3 == 'KSV': # Kosovo is not found in pycountry but in IMF PPP data
                country_data = kosovo
            else:
                country_data: Any = pycountry.countries.get(alpha_3=country_code3)
                if not country_data:
                    print("No location information on IP address: " + country_code3)
                    #error(country_code3, "No location information on IP address")
                    continue
            try:
                a = country_data.alpha_2
            except:
                import pdb; pdb.set_trace()
            country_code = data['country_code'] = country_data.alpha_2
            data['name'] = getattr(country_data, 'common_name', country_data.name)
            del data['Long Name']

            # decompose Currency Unit           AFN: Afghani (2011)
            currency_unit: Optional[str] = data['Currency Unit']
            data['currency_code'] = currency_unit[0:3]
            data['currency_name'] = re.sub(' \\(.*?\\)', '', currency_unit[5:])
            del data['Currency Unit']

            data['table_name'] = data['Table Name']
            del data['Table Name']
            # coverage
            coverage: Optional[str] = data.get('Household consumption price survey: Geographical coverage')
            del data['Household consumption price survey: Geographical coverage']
            if coverage:
                data['coverage'] = coverage

            Country_Metadata[country_code] = dict(data)
        #print(str(Country_Metadata))

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
        "Taiwan Province of China": "Taiwan, China",
        "Venezuela": "Venezuela, RB",
        "Bonaire": "Bonaire, Sint Eustatius and Saba",
        "Yemen": "Yemen, Rep.",

    }

    # build Countries map from Implied PPP conversion rates (National currency per international dollar)
    with open('data/imf-dm-export-20201110.csv', newline='', encoding="utf_8_sig") as imf_file:
        imf_reader  = csv.DictReader(imf_file)

        # 193 countries and regions in the file
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

            if country_code == 'TL': # Timor-Leste is in asia.
                continent_code = 'AS'
            else:
                continent_code: Any = pycountry_convert.country_alpha2_to_continent_code(country_code)
            # print(str(ppps))

            # because ppp and dollar_per_luncho varies depending time, we fill them when API is called.
            Countries[country_code] = { 'year_ppp': ppps,
                                        'country_code': country_code,
                                        'currency_code': Country_Metadata[country_code]['currency_code'],
                                        'continent_code': continent_code,
                                        'currency_name': Country_Metadata[country_code]['currency_name'],
                                        'country_name': Country_Metadata[country_code]['name']
                                       }
            CountryCode_Names[country_code] = Country_Metadata[country_code]['name']

        Countries['KP'] = Countries.get('KP') or {
            'year_ppp': {},
            'country_code': 'KP',
            'currency_code': 'KPW',
            'continent_code': 'AS',
            'currency_name': "North Korean Won",
            'country_name': "Korea, Democratic People's Republic of"
        }

        #print(str(Countries))
        #print(CountryCode_Names)

def update() -> None:
    ''' Update Countries to reflect the latest exchange rates. '''

    from src import exchange_rate
    year: int = datetime.datetime.today().year
    logging.info('ppp_data.update()')

    for country_code, country in Countries.items():  #type: CountryCode, Country
        country['ppp'] = country['year_ppp'].get(year, 0.0)  # country's ppp of this year
        country['exchange_rate'] = exchange_rate.exchange_rate_per_USD(country['currency_code'])
        country['dollar_per_luncho'] = exchange_rate.Dollar_Per_SDR * SDR_Per_Luncho
        country['expiration'] = exchange_rate.expiration
