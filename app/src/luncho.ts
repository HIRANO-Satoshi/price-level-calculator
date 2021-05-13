import { autoinject, TaskQueue } from 'aurelia-framework';
import { App } from './app';
import { DefaultApi, LunchoResult } from './gen-openapi';

export type CurrencyCode = string;
export type CountryCode = string;

@autoinject
export class LunchoCalc {
    app: App = App.app;
    api: DefaultApi = App.app.api;
    lunchoResult: LunchoResult;

    async convert(currencyCode: CurrencyCode, lunchoValue: number): Promise<number> {
        const calc = (lunchoValue: number) => {
            return this.lunchoResult.dollar_per_luncho * this.lunchoResult.ppp * lunchoValue;
        }
        if (this.lunchoResult) {
            return Promise.resolve(calc(lunchoValue));
        }
        return this.api.luncho({currencyCode: currencyCode, lunchoValue: Number(lunchoValue)})
            .then((lunchoResult: LunchoResult) => {
                this.lunchoResult = lunchoResult;
                return calc(lunchoValue);
            });
    }
}
