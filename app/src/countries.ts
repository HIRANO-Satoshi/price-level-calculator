import { autoinject, TaskQueue } from 'aurelia-framework';
import { App } from './app';
import { LunchoFast } from 'luncho-typescript-aurelia-fast/luncho-fast';
import { LunchoResult } from 'luncho-typescript-aurelia/models';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';

@autoinject
export class Countries {
    app: App;
    lunchoFast: LunchoFast
    taskQueue: TaskQueue;
    lunchoValue: number = 100;
    results: LunchoResult[];
    showCurrencyCode = false;
    showCountryCode = false;

    constructor(app: App, taskQueue: TaskQueue, lunchoFast: LunchoFast) {
        this.app = app;
        this.taskQueue = taskQueue;
        this.lunchoFast = lunchoFast;
    }

    attached() {
        this.lunchosForCountries();
    }

    async lunchosForCountries() {
        this.lunchoFast.lunchos({lunchoValue: Number(this.lunchoValue)})
            .then((results: LunchoResult[]) => {
                this.results = results;

                // run sorter
                this.taskQueue.queueTask(() => {
                    const tmp: any = $("#all-table");
                    tmp.tablesorter({
                        theme : 'materialize',
                        sortListY: [[0,0],[1,0]],
                    });
                });
            });
    }
}
