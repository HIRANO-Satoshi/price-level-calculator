import { autoinject } from 'aurelia-framework';
import { App, getFlagEmoji, formatCurrency } from './app';
import { Luncho, LunchoData  } from 'luncho-typescript-fetch';

@autoinject
export class Single {
    app: App;
    luncho: Luncho;
    countryCode: string = 'JP';
    lunchoValue: number = 100;
    lunchoData: LunchoData;
    local_currency_string: string;
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

    // convert from Luncho to local currency and USD
    async convertFromLuncho() {
        this.lunchoData = await this.luncho.get_luncho_data({countryCode: this.countryCode});
        this.decimals = this.app.countryData.currencies[this.lunchoData.currency_code].decimals;

        const value = await this.luncho.get_currency_from_luncho(this.lunchoValue, this.countryCode);
        this.local_currency_string = formatCurrency(value, this.decimals);
        this.dollar_value = await this.luncho.get_US_dollar_from_luncho(this.lunchoValue, this.countryCode);
    }

    // convert from local currency to Luncho and USD
    async convertFromLocalCurrency() {
        this.lunchoData = await this.luncho.get_luncho_data({countryCode: this.countryCode});
        this.decimals = this.app.countryData.currencies[this.lunchoData.currency_code].decimals;

        const value = Number(this.local_currency_string);
        console.log(value);
        this.lunchoValue = await this.luncho.get_luncho_from_currency(value, this.countryCode);

        this.dollar_value = await this.luncho.get_US_dollar_from_luncho(this.lunchoValue, this.countryCode);
    }

    getFlagEmoji(countryCode: string) {
        return getFlagEmoji(countryCode);
    }

}
