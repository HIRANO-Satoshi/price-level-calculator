/* tslint:disable */
/* eslint-disable */
/**
 * Custom title
 * This is a very custom OpenAPI schema
 *
 * The version of the OpenAPI document: 2.5.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * Data needed to convert between Luncho and local currency. 
 * @export
 * @interface LunchoData
 */
export interface LunchoData {
    /**
     * 
     * @type {string}
     * @memberof LunchoData
     */
    country_code: string;
    /**
     * 
     * @type {string}
     * @memberof LunchoData
     */
    country_name: string;
    /**
     * 
     * @type {string}
     * @memberof LunchoData
     */
    continent_code: string;
    /**
     * 
     * @type {string}
     * @memberof LunchoData
     */
    currency_code: string;
    /**
     * 
     * @type {string}
     * @memberof LunchoData
     */
    currency_name: string;
    /**
     * 
     * @type {number}
     * @memberof LunchoData
     */
    exchange_rate?: number;
    /**
     * 
     * @type {number}
     * @memberof LunchoData
     */
    ppp?: number;
    /**
     * 
     * @type {number}
     * @memberof LunchoData
     */
    dollar_per_luncho: number;
}

export function LunchoDataFromJSON(json: any): LunchoData {
    return LunchoDataFromJSONTyped(json, false);
}

export function LunchoDataFromJSONTyped(json: any, ignoreDiscriminator: boolean): LunchoData {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'country_code': json['country_code'],
        'country_name': json['country_name'],
        'continent_code': json['continent_code'],
        'currency_code': json['currency_code'],
        'currency_name': json['currency_name'],
        'exchange_rate': !exists(json, 'exchange_rate') ? undefined : json['exchange_rate'],
        'ppp': !exists(json, 'ppp') ? undefined : json['ppp'],
        'dollar_per_luncho': json['dollar_per_luncho'],
    };
}

export function LunchoDataToJSON(value?: LunchoData | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'country_code': value.country_code,
        'country_name': value.country_name,
        'continent_code': value.continent_code,
        'currency_code': value.currency_code,
        'currency_name': value.currency_name,
        'exchange_rate': value.exchange_rate,
        'ppp': value.ppp,
        'dollar_per_luncho': value.dollar_per_luncho,
    };
}


