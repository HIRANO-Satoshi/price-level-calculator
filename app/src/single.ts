import { autoinject, observable, TaskQueue, Aurelia } from 'aurelia-framework';
import { Router, RouteConfig } from 'aurelia-router'
import { HttpClient } from 'aurelia-fetch-client';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';
import { App } from './app';
import { Luncho, LunchoResult} from './luncho';

@autoinject
export class Single {
    app = App.app;
    countryCode: string = 'JPN';
    lunchoValue: number = 100;
    result: LunchoResult;

    // constructor() {
    // }

    attached() {
        this.convertFromLuncho();
    }

    convertFromLuncho() {
        this.app.luncho.convertFromLuncho(this.countryCode, Number(this.lunchoValue))
            .then((result: LunchoResult) => {
                this.result = result;
                this.countryCode = result.country_code;
            });
    }
}
