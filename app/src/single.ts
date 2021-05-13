import { autoinject, observable, TaskQueue, Aurelia } from 'aurelia-framework';
import { Router, RouteConfig } from 'aurelia-router'
import { HttpClient } from 'aurelia-fetch-client';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';
import { App } from './app';
import { DefaultApi, LunchoResult } from './gen-openapi';

@autoinject
export class Single {
    app: App = App.app;
    api: DefaultApi = App.app.api;
    countryCode: string = 'JPN';
    lunchoValue: number = 100;
    result: LunchoResult;

    constructor() {
    }

    attached() {
        this.convertFromLuncho();
    }

    convertFromLuncho() {
        this.api.convertFromLuncho({countryCode: this.countryCode, lunchoValue: Number(this.lunchoValue)})
            .then((result: LunchoResult) => {
                this.result = result;
                this.countryCode = result.country_code;
            });
    }
    // convertFromLuncho() {
    //     this.app.luncho.convertFromLuncho(this.countryCode, Number(this.lunchoValue))
    //         .then((result: LunchoResult) => {
    //             this.result = result;
    //             this.countryCode = result.country_code;
    //         });
    // }
}
