/**
  Fast Luncho API by caching. Use this and don't this LunchoApi.ts

  @author: HIRANO Satoshi
  @date: 2021-5-15
*/
import { HttpClient } from 'aurelia-http-client';
import { AuthStorage } from './AuthStorage';
import { LunchoData } from './models';
import { LunchoApi, ILunchoDataParams } from './LunchoApi';

export type CountryCode = string;

export class Luncho extends LunchoApi {

    lunchoDataCache: { [key: string]: LunchoData} = {};  // Cache {CountryCode: LunchoData}
    allLunchoDatasFetched = false;
    countryCache: { [key: string]: string; };

    IntlCountryNames: any;  // Intl.DisplayNames for country names
    IntlCurrencyNames: any; // Intl.DisplayNames for currency names
    // localCountryNames: {[key: string]: string} = {}         // {countryCode : countryName}
    // localCurrencyNames: {[key: string]: string; } = {}        // {countryCode : currencyName}

    constructor(httpClient: HttpClient, authStorage: AuthStorage) {
        super(httpClient, authStorage);

        // prepare local name converters
        var supportedLocales = (<any>Intl).DisplayNames.supportedLocalesOf(browserLocale())
        if (supportedLocales.length == 0)
            supportedLocales = ['en'];
        this.IntlCountryNames = new (<any>Intl).DisplayNames(supportedLocales[0], {type: 'region'})
        this.IntlCurrencyNames = new (<any>Intl).DisplayNames(supportedLocales[0], {type: 'currency'})
    }


    /**
       Returns a Luncho data for the given country code using cache.
    */
    async lunchoData(param: ILunchoDataParams, localName=true): Promise<LunchoData> {
        const lunchoData: LunchoData = this.lunchoDataCache[param.countryCode];
        if (lunchoData && lunchoData.expiration > Date.now()/1000) {
            return Promise.resolve(lunchoData);
        }

        return super.lunchoData(param)
            .then((lunchoData: LunchoData) => {
                this.lunchoDataCache[param.countryCode] = lunchoData;
                if (localName) {
                    lunchoData.country_name = this.IntlCountryNames.of(lunchoData.country_code);
                    lunchoData.currency_name = this.IntlCurrencyNames.of(lunchoData.currency_code);
                }
                return(lunchoData);
            });
    }

    /**
       Returns a local data for the given country code using cache.
    */
    async allLunchoData(localName=true): Promise<{ [key: string]: LunchoData} > {
        if (this.allLunchoDatasFetched && this.lunchoDataCache['JP'].expiration > Date.now()/1000) {
            return Promise.resolve(this.lunchoDataCache);
        }

        return super.allLunchoData()
            .then((lunchoDatas: { [key: string]: LunchoData}) => {
                this.lunchoDataCache = lunchoDatas;
                this.allLunchoDatasFetched = true;
                if (localName) {
                    for (var countryCode of Object.keys(this.lunchoDataCache)) {
                        this.lunchoDataCache[countryCode].country_name = this.IntlCountryNames.of(countryCode);
                        this.lunchoDataCache[countryCode].currency_name = this.IntlCurrencyNames.of(this.lunchoDataCache[countryCode].currency_code);
                    }
                }
                return(lunchoDatas);
            });
    }

    /**
       Returns a local data for the given country code using cache.
    */
    async getCountries(localName=true): Promise<{ [key: string]: string; }> {
        if (this.countryCache) {
            return Promise.resolve(this.countryCache);
        }

        return super.countries()
            .then((countryCache: { [key: string]: string; }) => {
                this.countryCache = countryCache;
                if (localName) {
                    for (var countryCode of Object.keys(this.countryCache)) {
                        this.countryCache[countryCode] = this.IntlCountryNames.of(countryCode);
                    }
                }
                return(countryCache);
            });
    }

    /**
       Returns a local currency value from the given Luncho value using cache.
    */
    async localCurrencyFromLuncho(lunchoValue: number, countryCode?: string): Promise<number> {
        return this.lunchoData({countryCode: countryCode})
            .then((lunchoData: LunchoData) => {
                  return(lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue);
            });
    }

    /**
       Returns a US Dollar value from the given Luncho value using cache.
    */
    async USDollarFromLuncho(lunchoValue: number, countryCode?: string): Promise<number> {
        return this.lunchoData({countryCode: countryCode})
            .then((lunchoData: LunchoData) => {
                if (lunchoData.exchange_rate > 0) {
                    const local_currency_value = lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue;
                    return(local_currency_value / lunchoData.exchange_rate);
                } else
                    return 0.0
            });
    }
}

function browserLocale () {
  var lang

  if (navigator.languages && navigator.languages.length) {
    // latest versions of Chrome and Firefox set this correctly
      lang = navigator.languages[0];
  } else if ((<any>navigator).userLanguage) {
    // IE only
      lang = (<any>navigator).userLanguage;
  } else {
    // latest versions of Chrome, Firefox, and Safari set this correctly
      lang = navigator.language || 'en';
  }

  return lang
}
