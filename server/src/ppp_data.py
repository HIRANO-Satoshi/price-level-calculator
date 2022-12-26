'''
  Luncho PPP data

  See for detail:  https://luncho-index.org/about#data

  @author HIRANO Satoshi
  @since  2021/05/13


'''

import csv
import datetime
import io
import json
import logging
import os
import re
from typing import List, Dict, Tuple, Union, Any, Type, Generator, Optional, ClassVar, cast
from typing_extensions import TypedDict
import pycountry
import pycountry_convert

import conf
from conf import SDR_Per_Luncho
#from src import exchange_rate
from src.types import Currency, CurrencyCode, C1000, CountryCode, LunchoData, Country
from src.utils import error

PPP_File  = 'data/imf-dm-export-20221225.csv'
ICP_File  = 'data/Data_Extract_From_ICP_2017_Metadata.csv'


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

    if not os.getcwd().endswith('server') and not conf.Is_AppEngine:
        os.chdir("server");

    def process_one_country(data):
        ''' Process a country metadata and put it in Country_Metadata map.

         ICP_File contains for countries and regions as following.

          ITA,Italian Republic,EUR: Euro,Italy,Capital-city only
          JAM,Jamaica,JMD: Jamaican Dollar,Jamaica,...
          JPN,Japan,JPY: Yen,Japan,Capital-city only

        '''

        country_data: Any

        country_code3 = data['Code']     # ISO 3 letter code
        del data['Code']
        if country_code3 == 'BON': # bonaire, but not found in IMF PPP data
            country_code3 = 'BES';
        if country_code3 == 'KSV': # Kosovo is not found in pycountry but in IMF PPP data
            country_data = kosovo
        else:
            country_data: Any = pycountry.countries.get(alpha_3=country_code3)
        if country_data:
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
        else:
            print("No location information on IP address: " + country_code3)
            #error(country_code3, "No location information on IP address")

    for file in (ICP_File, 'data/Data_Extract_From_ICP_Fix.csv'):
        with open(file, newline='', encoding="utf_8_sig") as metadata_file:
            metadata_reader  = csv.DictReader(metadata_file)

            for data in metadata_reader:
                process_one_country(data)
            #breakpoint()

    with open('data/imf-dm-mapping.json') as f:
        mapping = json.load(f)

    # build Countries map from Implied PPP conversion rates (National currency per international dollar)
    #
    # PPP_File
    #
    # Antigua and Barbuda,1.296,1.283,1.344,1.36,1.363,1.42,1.505,1.599,1.735,1.746,1.711,1.698,1.701,1.692,1.71,1.716,1.735,1.737,1.754,1.755,1.743,1.731,1.716,1.668,1.651,1.673,1.63,1.647,1.686,1.703,1.709,1.691,1.829,1.854,1.915,2.04,2.06,2.094,2.09,2.057,2.055,2.059,2.054,2.048,2.046,2.047,2.05
    # Argentina,0,0,0,0,0,0,0,0,0.001,0.016,0.334,0.766,0.851,0.817,0.822,0.831,0.816,0.798,0.776,0.751,0.742,0.718,0.923,1,1.032,1.104,1.219,1.364,1.648,1.887,2.256,2.733,3.218,3.941,5.452,6.867,9.295,10.257,14.024,20.753,29.119,41.198,56.231,70.931,84.788,97.39,108.15
    #
    with open(PPP_File, newline='', encoding="utf_8_sig") as imf_file:
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

            if country_code in ('TL', 'KP'): # Timor-Leste and North Korea are in asia.
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

        # Countries['KP'] = Countries.get('KP') or {
        #     'year_ppp': {},
        #     'country_code': 'KP',
        #     'currency_code': 'KPW',
        #     'continent_code': 'AS',
        #     'currency_name': "North Korean Won",
        #     'country_name': "Korea, Democratic People's Republic of"
        # }

        #print(str(Countries))
        #print(CountryCode_Names)

def update() -> None:
    ''' Update Countries to reflect the latest exchange rates. '''

    from src import exchange_rate
    year: int = datetime.datetime.today().year
    logging.info('ppp_data.update()')

    with exchange_rate.global_variable_lock:
        for country_code, country in Countries.items():  #type: CountryCode, Country
            country['ppp'] = country['year_ppp'].get(year, 0.0)  # country's ppp of this year
            country['exchange_rate'] = exchange_rate.exchange_rate_per_USD(country['currency_code'])
            country['dollar_per_luncho'] = SDR_Per_Luncho / exchange_rate.SDR_Per_Dollar
            country['expiration'] = exchange_rate.expiration
