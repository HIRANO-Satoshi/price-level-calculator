import { autoinject, observable, TaskQueue, Aurelia } from 'aurelia-framework';
import { Router, RouteConfig } from 'aurelia-router'
import {HttpClient} from 'aurelia-fetch-client';
import 'tablesorter';
import 'tablesorter/dist/css/theme.materialize.min.css';

export type CurrencyCode = string;
export type CountryCode = string;

export interface LunchoResult {
    country_code: CountryCode,
    country_name: string,

    currency_code: CurrencyCode,
    currency_name: string,
    ppp: number,
    exchange_rate: number,

    dollar_per_luncho: number,

    dollar_value: number,
    local_currency_value,
}

export interface LunchoCountry {
    country_name: string,        // Afghanistan
    currency_code: CurrencyCode, // AFN  (ISO 3 letter currency code)
    currency_name: string,       // Afghani
    ppp: number                  // PPP in local currency of currency_name
    [year_ppp: number]: number,   // { year: ppp }  Optional
}
export interface LuncoCountryDict {
    [index: string]: LunchoCountry
}

@autoinject
export class Luncho {
    public taskQueue: TaskQueue;              // Aurelia taskQueue
    httpClient = new HttpClient();  // https://aurelia.io/docs/plugins/http-services#aurelia-fetch-client

    constructor(taskQueue: TaskQueue) {
        this.taskQueue = taskQueue;
    }

    async getCountries(): Promise<LunchoResult> {
        return this.httpClient.fetch(`http://localhost:8000/countries`)
            .then((response: Response) => response.json())
    }

    async convertFromLunchos(lunchoValue: number): Promise<LunchoResult[]> {
        var params = {
            luncho_value: Number(lunchoValue),
        };
        const qs = new URLSearchParams(<any>params)
        return this.httpClient.fetch(`http://localhost:8000/convert-from-luncho-all/?${qs}`)
            .then((response: Response) => response.json());
    }

    async convertFromLuncho(countryCode: string, lunchoValue: number) {
        var params = {
            country_code: countryCode,
            luncho_value: Number(lunchoValue),
        };
        const qs = new URLSearchParams(<any>params)
        return this.httpClient.fetch(`http://localhost:8000/convert-from-luncho/?${qs}`)
            .then((response: Response) => response.json());
    }
}
