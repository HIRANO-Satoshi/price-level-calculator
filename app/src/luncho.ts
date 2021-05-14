import { autoinject, TaskQueue } from 'aurelia-framework';
import { App } from './app';
import { LunchoApi, LunchoResult } from './gen-openapi';

export type CurrencyCode = string;
export type CountryCode = string;

@autoinject
export class LunchoCalc {
    app: App = App.app;
    api: LunchoApi = App.app.api;
    lunchoResult: LunchoResult;

    async convert(countryCode: CountryCode, lunchoValue: number): Promise<number> {
        const calc = (lunchoValue: number) => {
            return this.lunchoResult.dollar_per_luncho * this.lunchoResult.ppp * lunchoValue;
        }
        if (this.lunchoResult) {
            return Promise.resolve(calc(lunchoValue));
        }
        return this.api.luncho({countryCode: countryCode, lunchoValue: Number(lunchoValue)})
            .then((lunchoResult: LunchoResult) => {
                this.lunchoResult = lunchoResult;
                return calc(lunchoValue);
            });
    }
}
