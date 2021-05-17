import { autoinject, TaskQueue } from 'aurelia-framework';
import { App } from './app';
import { Luncho, CountryCode } from 'luncho-typescript-aurelia/luncho';
import { LunchoData } from 'luncho-typescript-aurelia/models';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';

@autoinject
export class Countries {
    app: App;
    luncho: Luncho
    taskQueue: TaskQueue;
    lunchoValue: number = 100;
    local_currency_values: Map<CountryCode, number>
    dollar_values: Map<CountryCode, number>;
    lunchoDataMap: Map<string, LunchoData>;
    showCurrencyCode = false;
    showCountryCode = false;

    constructor(app: App, taskQueue: TaskQueue, luncho: Luncho) {
        this.app = app;
        this.taskQueue = taskQueue;
        this.luncho = luncho;
    }

    attached() {
        this.lunchosForCountries();
    }

    async lunchosForCountries() {
        this.local_currency_values = new Map();
        this.dollar_values = new Map();
        this.lunchoDataMap = await this.luncho.getLunchoDatas();
        for (var [countryCode, lunchoData] of this.lunchoDataMap) {
            // destructive, but don't care
            lunchoData['local_currency_value'] = await this.luncho.localCurrencyFromLuncho(this.lunchoValue, countryCode);
            lunchoData['dollar_value'] = await this.luncho.USDollarFromLuncho(this.lunchoValue, countryCode);
        }

        // run sorter
        this.taskQueue.queueTask(() => {
            const tmp: any = $("#all-table");
            tmp.tablesorter({
                theme : 'materialize',
                // sortList: [[0,0],[1,0]],
            });
        });

    //     lunchoDataMap.forEach((_lunchoData: LunchoData, countryCode: CountryCode) => {
    //         this.luncho.localCurrencyFromLuncho(this.lunchoValue, countryCode)
    //             .then((value: number) => {
    //                 this.local_currency_values.set(countryCode, value);
    //                 this.luncho.USDollarFromLuncho(this.lunchoValue, countryCode)
    //                     .then((value: number) => {
    //                         this.dollar_values.set(countryCode, value);
    //                     });
    //             });
    //     });

    //     this.luncho.lunchos({lunchoValue: Number(this.lunchoValue)})
    //         .then((results: LunchoData[]) => {
    //             this.results = results;

    //             // run sorter
    //             this.taskQueue.queueTask(() => {
    //                 const tmp: any = $("#all-table");
    //                 tmp.tablesorter({
    //                     theme : 'materialize',
    //                     sortListY: [[0,0],[1,0]],
    //                 });
    //             });
    //         });
        // }
    }
}
