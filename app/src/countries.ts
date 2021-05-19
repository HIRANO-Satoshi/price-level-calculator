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
    lunchoDatas: { [key: string]: LunchoData} = {};
    continentCode: string = null;

    constructor(app: App, taskQueue: TaskQueue, luncho: Luncho) {
        this.app = app;
        this.taskQueue = taskQueue;
        this.luncho = luncho;
    }

    attached() {
        this.lunchosForCountries();
    }

    continentChanged() {
        this.filterContinent();

        //$("#all-table").trigger("update");
        // var resort = true,
        // callback = function(_table) {
        //     console.log('table updated!');
        // };
        // $("#all-table").trigger("update", [resort, callback]);
        // $("#all-table").trigger("updateCache");
    }

    filterContinent() {
        if (this.continentCode) {
            this.lunchoDatas = {};
            for (var countryCode of Object.keys(this.luncho.lunchoDataCache)) {
                if (this.luncho.lunchoDataCache[countryCode].continent_code == this.continentCode)
                    this.lunchoDatas[countryCode] = this.luncho.lunchoDataCache[countryCode];
            }
        } else
            this.lunchoDatas = this.luncho.lunchoDataCache;
    }

    async lunchosForCountries() {
        await this.luncho.allLunchoData();
        for (var countryCode of Object.keys(this.luncho.lunchoDataCache)) {
            // destructive, but don't care
            this.luncho.lunchoDataCache[countryCode]['local_currency_value'] = await this.luncho.localCurrencyFromLuncho(this.lunchoValue, countryCode);
            this.luncho.lunchoDataCache[countryCode]['dollar_value'] = await this.luncho.USDollarFromLuncho(this.lunchoValue, countryCode);
        }

        this.filterContinent();
        this.sort();
    }

    sort() {
        // run sorter
        this.taskQueue.queueTask(() => {
            const tmp: any = $("#all-table");
            tmp.tablesorter({
                theme : 'materialize',
                sortList: [[0,0]],  // initial sort on country name in ascending order
                resort: true,       // sort when update
            });
        });
    }
}
