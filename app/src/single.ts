import { autoinject } from 'aurelia-framework';
import { App } from './app';
import { Luncho,  } from 'luncho-typescript-fetch/luncho';
import { LunchoDataRequest } from 'luncho-typescript-fetch/apis/LunchoApi';
import { LunchoData } from 'luncho-typescript-fetch/models';
// import { LunchoApi } from 'luncho_typescript-aurelia/LunchoApi';
//import { LunchoApi, LunchoData } from 'luncho_typescript-aurelia';
//import { LunchoApi, LunchoData } from './gen-openapi';

@autoinject
export class Single {
    app: App;
    luncho: Luncho;
    countryCode: string = 'JP';
    lunchoValue: number = 100;
    lunchoData: LunchoData;
    local_currency_value: number;
    dollar_value: number;

    constructor(app: App, luncho: Luncho) {
        this.luncho = luncho;
        this.app = app;
    }

    async activate() {
        // download country codes and names
        if (window.origin.indexOf('localhost') >= 0)
            this.countryCode = 'JP';
        else
            this.countryCode = await this.luncho.get_country_code();
        await this.luncho.get_countries(true);
    }

    attached() {
        this.convertFromLuncho();

        // var elems = document.querySelectorAll('.autocomplete');
        // var instances = M.Autocomplete.init(elems, {
        //     data: // this.luncho.countryCache,
        //     {
        //         "Apple": null,
        //         "Microsoft": null,
        //         "Google": 'https://placehold.it/250x250'
        //     },
        //     minLength: 0,
        // });
    }

    async convertFromLuncho() {
        this.lunchoData = await this.luncho.get_luncho_data({countryCode: this.countryCode});
        this.local_currency_value = await this.luncho.get_currency_from_luncho(this.lunchoValue, this.countryCode);
        this.dollar_value = await this.luncho.get_US_dollar_from_luncho(this.lunchoValue, this.countryCode);
    }
}
