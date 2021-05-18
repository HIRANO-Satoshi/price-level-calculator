'''
   Fast Luncho API client by caching. Use this and don't this LunchoApi.py

  @author: HIRANO Satoshi
  @date: 2021-5-18
'''
import time
from typing import List, Dict, Tuple, Callable, Union, Any, Set, ClassVar, Type, Optional, cast

from luncho_python.api.luncho_api import LunchoApi
from luncho_python.api_client import ApiClient, Endpoint as _Endpoint
from luncho_python.model.luncho_data import LunchoData

CountryCode = str

class Luncho(LunchoApi):
    def __init__(self, api_client=None):
        self.lunchoDataMap: Dict[CountryCode, LunchoData] = {}  # Cache {CountryCode: LunchoData}
        self.allLunchoDatasFetched: bool = False
        self.countryMap: Dict[CountryCode, str] = {}       # { CountryCode: name }
        super().__init__(api_client)


    def luncho_data_fast(self, country_code: CountryCode, **kwargs) -> LunchoData:
        '''
           Returns a Luncho data for the given country code using cache.
        '''
        lunchoData: Optional[LunchoData] = self.lunchoDataMap.get(country_code)
        if lunchoData and lunchoData.expiration > time.time():
            return lunchoData

        lunchoData = self.luncho_data(country_code, **kwargs)
        lunchoData = cast(LunchoData, lunchoData)
        self.lunchoDataMap[country_code] = lunchoData
        return lunchoData

    def luncho_datas_fast(self, **kwargs) -> Dict[CountryCode, LunchoData]:
        '''
        Returns a local data for the given country code using cache.
        '''
        if self.allLunchoDatasFetched:
            lunchoData: Optional[LunchoData] = self.lunchoDataMap.get('JP')
            if lunchoData and lunchoData.expiration > time.time():
                return self.lunchoDataMap

        lunchoDatas: Dict[CountryCode, LunchoData] = self.luncho_datas(**kwargs)
        self.lunchoDataMap = lunchoDatas
        self.allLunchoDatasFetched = True
        return lunchoDatas


    def countries_fast(self, **kwargs) -> Dict[CountryCode, str]:
        '''
        Returns a local data for the given country code using cache.
        '''

        #import pdb; pdb.set_trace()
        if self.countryMap:
            return self.countryMap

        self.countryMap = self.countries(**kwargs)
        return self.countryMap

    def localCurrencyFromLuncho(self, lunchoValue: float, countryCode: str, **kwargs) -> float:
        '''
        Returns a local currency value from the given Luncho value using cache.
        '''

        lunchoData: LunchoData = self.luncho_data_fast(countryCode, **kwargs)
        return lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue

    def USDollarFromLuncho(self, lunchoValue: float, countryCode: str, **kwargs) -> float:
        '''
        Returns a US Dollar value from the given Luncho value using cache.
        '''

        lunchoData: LunchoData = self.luncho_data_fast(countryCode, **kwargs)
        if lunchoData.exchange_rate > 0:
            local_currency_value: float = lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue;
            return local_currency_value / lunchoData.exchange_rate
        else:
            return 0.0
