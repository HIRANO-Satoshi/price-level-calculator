import { autoinject, TaskQueue } from 'aurelia-framework';
import { App } from './app';
import { Luncho } from 'luncho_typescript-aurelia/luncho';
import { LunchoData } from 'luncho_typescript-aurelia/models';

@autoinject
export class Countries {
    app: App;
    luncho: Luncho
    taskQueue: TaskQueue;
    lunchoValue: number = 100;
    lunchoDatas: LunchoData[];      // this is the table data.

    showCode = false;

    filters = [
        {value: '', keys: ['country_name', 'currency_name']},
        {value: '', keys: ['continent_code']},
    ];

    constructor(app: App, taskQueue: TaskQueue, luncho: Luncho) {
        this.app = app;
        this.taskQueue = taskQueue;
        this.luncho = luncho;
    }

    attached() {
        this.lunchosForCountries();
    }

    async lunchosForCountries() {
        await this.luncho.allLunchoData();
        for (var countryCode of Object.keys(this.luncho.lunchoDataCache)) {
            // destructive, but don't care
            this.luncho.lunchoDataCache[countryCode]['local_currency_value'] = await this.luncho.localCurrencyFromLuncho(this.lunchoValue, countryCode);
            this.luncho.lunchoDataCache[countryCode]['dollar_value'] = await this.luncho.USDollarFromLuncho(this.lunchoValue, countryCode);
        }

        this.lunchoDatas = [];
        for (var countryCode of Object.keys(this.luncho.lunchoDataCache)) {
            this.lunchoDatas.push(this.luncho.lunchoDataCache[countryCode]);
        }
    }
}
