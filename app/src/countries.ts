import { autoinject, TaskQueue } from 'aurelia-framework';
import { App } from './app';
import { Luncho } from 'luncho_typescript-aurelia/luncho';
import { LunchoData } from 'luncho_typescript-aurelia/models';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';

@autoinject
export class Countries {
    app: App;
    luncho: Luncho
    taskQueue: TaskQueue;
    lunchoValue: number = 100;
    showCurrencyCode = false;
    showCountryCode = false;
    continents = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'EU': 'Europe',
        'OC': 'Australia',
        'AF': 'Africa',
    }
    constructor(app: App, taskQueue: TaskQueue, luncho: Luncho) {
        this.app = app;
        this.taskQueue = taskQueue;
        this.luncho = luncho;
    }

    attached() {
        this.lunchosForCountries();
    }

    async lunchosForCountries() {
        await this.luncho.lunchoDatas();
        for (var countryCode of Object.keys(this.luncho.lunchoDataMap)) {
            // destructive, but don't care
            this.luncho.lunchoDataMap[countryCode]['local_currency_value'] = await this.luncho.localCurrencyFromLuncho(this.lunchoValue, countryCode);
            this.luncho.lunchoDataMap[countryCode]['dollar_value'] = await this.luncho.USDollarFromLuncho(this.lunchoValue, countryCode);
        }

        // run sorter
        this.taskQueue.queueTask(() => {
            const tmp: any = $("#all-table");
            tmp.tablesorter({
                theme : 'materialize',
                // sortList: [[0,0],[1,0]],
            });
        });
    }
}
