import { autoinject } from 'aurelia-framework';
import { App, getFlagEmoji } from './app';
import { Luncho  } from 'luncho-typescript-fetch';
import { LunchoData } from 'luncho-typescript-fetch';
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
    decimals: number;

    constructor(app: App) {
        this.app = app;
        this.luncho = app.luncho;
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
    }

    async convertFromLuncho() {
        this.lunchoData = await this.luncho.get_luncho_data({countryCode: this.countryCode});
        this.local_currency_value = await this.luncho.get_currency_from_luncho(this.lunchoValue, this.countryCode);
        this.dollar_value = await this.luncho.get_US_dollar_from_luncho(this.lunchoValue, this.countryCode);
        this.decimals = this.app.countryData.currencies[this.lunchoData.currency_code].decimals;
    }

    getFlagEmoji(countryCode: string) {
        return getFlagEmoji(countryCode);
    }

}
