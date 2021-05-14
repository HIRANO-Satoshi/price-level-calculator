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
export interface HTTPValidationError {
    detail?: Array<ValidationError>;
}
export interface IMFPPPCountry {
    year_ppp?: {
        [key: string]: number;
    };
    currency_code?: string;
    currency_name?: string;
    country_name?: string;
}
export interface LunchoResult {
    dollar_value: number;
    local_currency_value: number;
    currency_code: string;
    country_code: string;
    country_name: string;
    currency_name: string;
    ppp?: number;
    dollar_per_luncho: number;
    exchange_rate?: number;
}
export interface ValidationError {
    loc: Array<string>;
    msg: string;
    type: string;
}
