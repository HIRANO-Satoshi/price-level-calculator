'''
   Fast Luncho API client by caching. Use this and don't this LunchoApi.py

  @author: HIRANO Satoshi
  @date: 2021-5-18
'''
import time
#import pdb; pdb.set_trace()
from typing import List, Dict, Tuple, Callable, Union, Any, Set, ClassVar, Type, Optional, cast

from luncho_python.api.luncho_api import LunchoApi
from luncho_python.api_client import ApiClient, Endpoint as _Endpoint
from luncho_python.model.luncho_data import LunchoData

CountryCode = str

class Luncho():
    ''' Fast Luncho API client by caching.
        This class converts values between Luncho and a specified currency using cached
        LunchoData. If the cache is not available, it delegates to LunchoApi which
        is a auto-generated class.

        In the cases of error, methods raise luncho_python.ApiException.
        Note that no async_req argument is supported.
    '''

    def __init__(self, api_client=None):
        self.lunchoApi = LunchoApi(api_client)             # for delegation

        self.lunchoDataCache: Dict[CountryCode, LunchoData] = {}  # Cache {CountryCode: LunchoData}
        self.allLunchoDatasExpiration: float = 0.0;
        self.countryCache: Dict[CountryCode, str] = {}       # { CountryCode: name }


    def luncho_to_currency(self, lunchoValue: float, countryCode: str, **kwargs) -> float:
        '''
          Returns a local currency value from the given Luncho value for the specified country.
        '''

        lunchoData: LunchoData = self.luncho_data(countryCode, **kwargs)
        return lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue

    def currency_to_luncho(self, lunchoValue: float, countryCode: str, **kwargs) -> float:
        '''
          Returns a Luncho value from a local currency value for the specified country.
        '''

        assert False, 'XXX Implement me'
        return 0.0

    def luncho_to_US_dollar(self, lunchoValue: float, countryCode: str, **kwargs) -> float:
        '''
          Returns a US Dollar value from the given Luncho value for the specified country.
        '''

        lunchoData: LunchoData = self.luncho_data(countryCode, **kwargs)
        if lunchoData.exchange_rate > 0:
            local_currency_value: float = lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue;
            return local_currency_value / lunchoData.exchange_rate
        else:
            return 0.0

    def US_dollar_to_luncho(self, lunchoValue: float, countryCode: str, **kwargs) -> float:
        '''
          Returns a Luncho value from a US Dollar value for the specified country.
        '''

        assert False, 'XXX Implement me'
        return 0.0

    def countries(self, **kwargs) -> Dict[CountryCode, str]:
        '''
          Returns a dict of supported country codes and country names.
        '''

        if self.countryCache:
            return self.countryCache

        self.countryCache = self.lunchoApi.countries(**kwargs)
        return self.countryCache

    def luncho_data(self, country_code: CountryCode, **kwargs) -> LunchoData:
        '''
           Returns a LunchoData of the specified country code. You don't need to use this method
           usually. Use localCurrencyFromLuncho() and USDollarFromLuncho().
        '''
        lunchoData: Optional[LunchoData] = self.lunchoDataCache.get(country_code)
        if lunchoData and lunchoData.expiration > time.time():
            return lunchoData

        lunchoData = cast(LunchoData, self.lunchoApi.luncho_data(country_code, **kwargs))
        self.lunchoDataCache[country_code] = lunchoData
        return lunchoData

    def all_luncho_data(self, **kwargs) -> Dict[CountryCode, LunchoData]:
        '''
          Returns a dict of LunchoDatas of all countries. You don't need to use this method
           usually. Use localCurrencyFromLuncho() and USDollarFromLuncho().
        '''
        if self.allLunchoDatasExpiration > time.time():
            return self.lunchoDataCache

        self.lunchoDataCache = self.lunchoApi.all_luncho_data(**kwargs)
        assert self.lunchoDataCache
        assert self.lunchoDataCache['JP']
        self.allLunchoDatasExpiration = self.lunchoDataCache['JP'].expiration
        return self.lunchoDataCache


    def __getattr__(self, method_name):
        ''' Delegates all other methods to self.lunchoApi. '''

        def method(*args, **kwargs):
            return getattr(self.lunchoApi, method_name)(*args, **kwargs)
        return method
