/**
   Fast Luncho API by caching. Don't this
*/
import { LunchoData } from './models';
import { LunchoApi, ILunchoDataParams } from './LunchoApi';

export type CountryCode = string;

export class Luncho extends LunchoApi {

    lunchoDataMap: { [key: string]: LunchoData} = {};  // Cache {CountryCode: LunchoData}
    allLunchoDatasFetched = false;
    countryMap: { [key: string]: string; };


    /**
       Returns a local data for the given country code using cache.
    */
    async lunchoData(param: ILunchoDataParams ): Promise<LunchoData> {
        const lunchoData: LunchoData = this.lunchoDataMap[param.countryCode];
        if (lunchoData) {
            return Promise.resolve(lunchoData);
        }

        return super.lunchoData(param)
            .then((lunchoData: LunchoData) => {
                this.lunchoDataMap[param.countryCode] = lunchoData;
                  return(lunchoData);
            });
    }

    /**
       Returns a local data for the given country code using cache.
    */
    async lunchoDatas(): Promise<{ [key: string]: LunchoData} > {
        if (this.allLunchoDatasFetched) {
            return Promise.resolve(this.lunchoDataMap);
        }

        return super.lunchoDatas()
            .then((lunchoDatas: { [key: string]: LunchoData}) => {
                this.lunchoDataMap = lunchoDatas;
                this.allLunchoDatasFetched = true;
                return(lunchoDatas);
            });
    }

    /**
       Returns a local data for the given country code using cache.
    */
    async getCountries(): Promise<{ [key: string]: string; }> {
        if (this.countryMap) {
            return Promise.resolve(this.countryMap);
        }

        return super.countries()
            .then((countryMap: { [key: string]: string; }) => {
                this.countryMap = countryMap;
                  return(countryMap);
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
                const local_currency_value = lunchoData.dollar_per_luncho * lunchoData.ppp * lunchoValue;
                return(local_currency_value / lunchoData.exchange_rate);
            });
    }
}