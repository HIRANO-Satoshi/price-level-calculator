import { autoinject } from 'aurelia-framework';
import { LunchoData } from './models';
import { LunchoApi } from './LunchoApi';

export type CountryCode = string;

/** Luncho calculator fast version with caching.  */
@autoinject
export class Luncho extends LunchoApi {

//    lunchoDataList: LunchoData[];                 // data of all countries.
    lunchoDataMap: Map<string, LunchoData> = new Map();  // Cache {CountryCode: LunchoData}
    allLunchoDatasFetched = false;

    /**
       Returns a local data for the given country code.
    */
    async getLunchoData(countryCode?: string): Promise<LunchoData> {
        const lunchoData: LunchoData = this.lunchoDataMap.get(countryCode);
        if (lunchoData) {
            return Promise.resolve(lunchoData);
        }

        return super.lunchoData({countryCode: countryCode})
            .then((lunchoData: LunchoData) => {
                this.lunchoDataMap.set(countryCode, lunchoData);
                  return(lunchoData);
            });
    }

    /**
       Returns a local data for the given country code.
    */
    async getLunchoDatas(): Promise<Map<CountryCode, LunchoData>> {
        if (this.lunchoDataMap.size > 0) {
            return Promise.resolve(this.lunchoDataMap);
        }

        return super.lunchoDatas()
            .then((lunchoDatas: LunchoData[]) => {
                this.lunchoDataMap = new Map();
                for (const lunchoData of lunchoDatas) {
                    this.lunchoDataMap.set(lunchoData.country_code, lunchoData);
                }
                return(this.lunchoDataMap);
            });
    }

    /**
       Returns a local currency value from the given Luncho value.
    */
    async localCurrencyFromLuncho(lunchoValue: number, countryCode?: string): Promise<number> {
        return this.getLunchoData(countryCode)
            .then((lunchoData: LunchoData) => {
                  return(lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue);
            });
    }

    async YYYlocalCurrencyFromLuncho(lunchoValue: number, countryCode?: string): Promise<number> {
        const lunchoData: LunchoData = this.lunchoDataMap.get(countryCode);
        const calc = ((): number => {
            return lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue;
        });

        if (lunchoData) {
            return Promise.resolve(calc());
        }

        return super.lunchoData({countryCode: countryCode})
            .then((lunchoData: LunchoData) => {
                this.lunchoDataMap.set(countryCode, lunchoData);
                  return(calc());
            });
    }

    /**
       Returns a US Dollar value from the given Luncho value.
    */
    async USDollarFromLuncho(lunchoValue: number, countryCode?: string): Promise<number> {
        return this.getLunchoData(countryCode)
            .then((lunchoData: LunchoData) => {
                const local_currency_value = lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue;
                return(local_currency_value / lunchoData.exchange_rate);
            });
    }

    async YYYUSDollarFromLuncho(lunchoValue: number, countryCode?: string): Promise<number> {
        const lunchoData: LunchoData = this.lunchoDataMap.get(countryCode);
        const calc = ((): number => {
            const local_currency_value = lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue;
            const dollar_value = local_currency_value / lunchoData.exchange_rate;
            return dollar_value;
        });

        if (lunchoData) {
            return Promise.resolve(calc());
        }

        return super.lunchoData({countryCode: countryCode})
            .then((lunchoData: LunchoData) => {
                this.lunchoDataMap.set(countryCode, lunchoData);
                  return(calc());
            });
    }
}
