import { autoinject } from 'aurelia-framework';
import { App } from './app';
import { LunchoFast } from 'luncho-typescript-aurelia-fast/luncho-fast';
import { LunchoResult } from 'luncho-typescript-aurelia/models';
// import { LunchoApi } from 'luncho-typescript-aurelia/LunchoApi';
//import { LunchoApi, LunchoResult } from 'luncho-typescript-aurelia';
//import { LunchoApi, LunchoResult } from './gen-openapi';

@autoinject
export class Single {
    app: App;
    lunchoFast: LunchoFast;
    countryCode: string = 'JPN';
    lunchoValue: number = 100;
    result: LunchoResult;

    constructor(app: App, lunchoFast: LunchoFast) {
        this.lunchoFast = lunchoFast;
        this.app = app;
    }

    attached() {
        this.convertFromLuncho();
    }

    async convertFromLuncho() {
        this.lunchoFast.luncho({countryCode: this.countryCode, lunchoValue: Number(this.lunchoValue)})
            .then((result: LunchoResult) => {
                this.result = result;
                this.countryCode = result.country_code;
            });
    }
}
