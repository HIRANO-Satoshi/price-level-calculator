/**
  Fast Luncho API with caching. Use this and don't this LunchoApi.ts.

  @author: HIRANO Satoshi
  @date: 2021-5-15
*/
import { LunchoData } from './models';
import { LunchoApi, LunchoDataRequest } from './apis/LunchoApi';
//window['GlobalFetch'] = window.fetch;
import { Configuration } from './runtime';

export type CountryCode = string;

/**
    Fast Luncho API client by caching.
        This class converts values between Luncho and a specified currency using cached
        LunchoData. If the cache is not available, it delegates to LunchoApi which
        is a auto-generated class.

        In the cases of error, methods throws an Error. See LunchoApi.ts for error.
 */
export class Luncho extends LunchoApi {

    lunchoDataCache: { [key: string]: LunchoData} = {};  // Cache {CountryCode: LunchoData}
    allLunchoDatasExpiration: number = 0;
    countryCache: { [key: string]: string; };
    countryCodeCache: string;

    IntlCountryNames: any;  // Intl.DisplayNames for country names
    IntlCurrencyNames: any; // Intl.DisplayNames for currency names
    // localCountryNames: {[key: string]: string} = {}         // {countryCode : countryName}
    // localCurrencyNames: {[key: string]: string; } = {}        // {countryCode : currencyName}

    constructor() {
        let basePath: string;
        if (window.origin.indexOf('localhost') >= 0)
            basePath = 'http://localhost:8000';
        else
            basePath = window.origin;
        super(new Configuration({
             basePath: basePath
         }));

        // prepare local name converters
        if ((<any>Intl).DisplayNames) {
            var supportedLocales = (<any>Intl).DisplayNames.supportedLocalesOf(browserLocale())
            if (supportedLocales.length == 0)
                supportedLocales = ['en'];
            this.IntlCountryNames = new (<any>Intl).DisplayNames(supportedLocales[0], {type: 'region'})
            this.IntlCurrencyNames = new (<any>Intl).DisplayNames(supportedLocales[0], {type: 'currency'})
        }
    }

    // setBasePath(basePath: string) {
    //     this.configuration.basePath = basePath;
    // }

    /**
       Returns a local currency value from the given Luncho value.

       @param lunchoValue A Luncho value to be converted.
       @param countryCode A 2-letter country code. The result is in the primary currency of the country.
       @return Promise for a value in local currency.
    */
    async get_currency_from_luncho(lunchoValue: number, countryCode: string): Promise<number> {
        return this.get_luncho_data({countryCode: countryCode})
            .then((lunchoData: LunchoData) => {
                  return(lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue);
            });
    }

    /**
       Returns a Luncho value from the given local currency value (not implemented).

       @param localValue A value in local currency to be converted.
       @param countryCode A 2-letter country code of the country for the localValue.
       @return Promise for a value in Luncho.
    */
    async get_luncho_from_currency(localValue: number, countryCode: string): Promise<number> {
        debugger;  // XXX Implement me

        return this.get_luncho_data({countryCode: countryCode})
            .then((_lunchoData: LunchoData) => {
                  return(0.0);
            });
    }

    /**
       Returns a US Dollar value from the given Luncho value using cache.

       @param lunchoValue A Luncho value to be converted.
       @param countryCode A 2-letter country code.
       @return Promise for a value in US dollar.
    */
    async get_US_dollar_from_luncho(lunchoValue: number, countryCode: string): Promise<number> {
        return this.get_luncho_data({countryCode: countryCode})
            .then((lunchoData: LunchoData) => {
                if (lunchoData.exchange_rate > 0) {
                    const local_currency_value = lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue;
                    return(local_currency_value / lunchoData.exchange_rate);
                } else
                    return 0.0
            });
    }

    /**
       Returns a Luncho value from the given US Dollar value (not implemented).

       @param dollarValue A value in US dollar to be converted.
       @param countryCode A 2-letter country code of the country.
       @return Promise for a value in Luncho.
    */
    async get_luncho_from_US_dollar(_dollarValue: number, countryCode: string): Promise<number> {
        debugger;  // XXX Implement me

        return this.get_luncho_data({countryCode: countryCode})
            .then((lunchoData: LunchoData) => {
                if (lunchoData.exchange_rate > 0) {
                    return 0.0;
                } else
                    return 0.0;
            });
    }


    /**
       Returns a Luncho data for the given country code.

       @param param A LunchoDataRequest object.
       @param localName True for country names and currency names in the local lauguage. Ignored if Intl.DisplayNames is not available.
       @return Promise for LunchoData.
    */
    async get_luncho_data(param: LunchoDataRequest, localName=true): Promise<LunchoData> {
        if (param && param.countryCode) {
            const lunchoData: LunchoData = this.lunchoDataCache[param.countryCode];
            // if (lunchoData) {
            if (lunchoData && lunchoData.expiration > Date.now()/1000) {
                return Promise.resolve(lunchoData);
            }
        }

        return super.lunchoData(param)
            .then((lunchoData: LunchoData) => {
                this.lunchoDataCache[param.countryCode] = lunchoData;
                if (localName && this.IntlCountryNames) {
                    lunchoData.country_name = this.IntlCountryNames.of(lunchoData.country_code);
                    lunchoData.currency_name = this.IntlCurrencyNames.of(lunchoData.currency_code);
                }
                return(lunchoData);
            });
    }

    /**
       Returns a dict of Luncho datas of all countries.

       @param localName True for country names and currency names in the local lauguage. Ignored if Intl.DisplayNames is not available.
       @return Promise for a dict of Luncho datas of all countries.
    */
    async get_all_luncho_data(localName=true): Promise<{ [key: string]: LunchoData} > {
        if (this.allLunchoDatasExpiration > Date.now()/1000) {
            return Promise.resolve(this.lunchoDataCache);
        }

        return super.allLunchoData()
            .then((lunchoDatas: { [key: string]: LunchoData}) => {
                this.lunchoDataCache = lunchoDatas;
                this.allLunchoDatasExpiration = lunchoDatas['JP'].expiration;
                if (localName && this.IntlCountryNames) {
                    for (var countryCode of Object.keys(this.lunchoDataCache)) {
                        this.lunchoDataCache[countryCode].country_name = this.IntlCountryNames.of(countryCode);
                        this.lunchoDataCache[countryCode].currency_name = this.IntlCurrencyNames.of(this.lunchoDataCache[countryCode].currency_code);
                    }
                }
                return(lunchoDatas);
            });
    }

    /**
       Returns a dict of supported country codes and country names.

       @param localName True for country names and currency names in the local lauguage. Ignored if Intl.DisplayNames is not available.
       @return Promise for a dict of supported country codes and country names.
    */
    async get_countries(localName=true): Promise<{ [key: string]: string; }> {
        if (this.countryCache) {
            return Promise.resolve(this.countryCache);
        }

        return super.countries()
            .then((countryCache: { [key: string]: string; }) => {
                this.countryCache = countryCache;
                if (localName && this.IntlCountryNames) {
                    for (var countryCode of Object.keys(this.countryCache)) {
                        this.countryCache[countryCode] = this.IntlCountryNames.of(countryCode);
                    }
                }
                return(countryCache);
            });
    }

    /**
       Returns an estimated country code. Available only if the server supports.
    */
    async get_country_code(): Promise<string> {
        if (this.countryCodeCache) {
            return Promise.resolve(this.countryCodeCache);
        }

        return super.countryCode()
            .then((countryCode: string) => {
                this.countryCodeCache = countryCode;
                return(this.countryCodeCache);
            });
    }

}

function browserLocale () {
    let lang: string;

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
