import { autoinject, observable, TaskQueue, Aurelia } from 'aurelia-framework';
import { Router, RouteConfig } from 'aurelia-router'
import { HttpClient } from 'aurelia-fetch-client';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';
import { App } from './app';
import { Luncho, LunchoResult} from './luncho';

@autoinject
export class Countries {
    app = App.app;
    taskQueue: TaskQueue;
    lunchoValue: number = 100;
    results: LunchoResult[];
    showCurrencyCode = false;
    showCountryCode = false;

    constructor(taskQueue: TaskQueue) {
        this.taskQueue = taskQueue;
    }

    attached() {
        this.convertFromLunchos();
    }

    convertFromLunchos() {
        this.app.luncho.convertFromLunchos(Number(this.lunchoValue))
            .then((results: LunchoResult[]) => {
                this.results = results;
                this.sorterInit();
            });
    }

    sorterInit() {
        this.taskQueue.queueTask(() => {
            // attached() {
            const tmp: any = $("#all-table");
            //tmp.tablesorter();
            tmp.tablesorter({
                theme : 'materialize',
                sortListY: [[0,0],[1,0]],
            });
        });
    }
}
