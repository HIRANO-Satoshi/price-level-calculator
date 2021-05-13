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


import * as runtime from '../runtime';
import {
    HTTPValidationError,
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    IMFPPPCountry,
    IMFPPPCountryFromJSON,
    IMFPPPCountryToJSON,
    LunchoResult,
    LunchoResultFromJSON,
    LunchoResultToJSON,
} from '../models';

export interface ConvertFromLunchoRequest {
    countryCode?: string;
    lunchoValue?: number;
}

export interface ConvertFromLunchoAllRequest {
    lunchoValue: number;
}

export interface ConvertFromLunchoDummyRequest {
    currencyCode: string;
    lunchoValue: number;
}

export interface TestRequest {
    countryCode?: string;
    lunchoValue?: number;
}

/**
 * 
 */
export class DefaultApi extends runtime.BaseAPI {

    /**
     * Convert From Luncho
     */
    async convertFromLunchoRaw(requestParameters: ConvertFromLunchoRequest): Promise<runtime.ApiResponse<LunchoResult>> {
        const queryParameters: any = {};

        if (requestParameters.countryCode !== undefined) {
            queryParameters['country_code'] = requestParameters.countryCode;
        }

        if (requestParameters.lunchoValue !== undefined) {
            queryParameters['luncho_value'] = requestParameters.lunchoValue;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/convert-from-luncho/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => LunchoResultFromJSON(jsonValue));
    }

    /**
     * Convert From Luncho
     */
    async convertFromLuncho(requestParameters: ConvertFromLunchoRequest): Promise<LunchoResult> {
        const response = await this.convertFromLunchoRaw(requestParameters);
        return await response.value();
    }

    /**
     * Convert From Luncho All
     */
    async convertFromLunchoAllRaw(requestParameters: ConvertFromLunchoAllRequest): Promise<runtime.ApiResponse<Array<LunchoResult>>> {
        if (requestParameters.lunchoValue === null || requestParameters.lunchoValue === undefined) {
            throw new runtime.RequiredError('lunchoValue','Required parameter requestParameters.lunchoValue was null or undefined when calling convertFromLunchoAll.');
        }

        const queryParameters: any = {};

        if (requestParameters.lunchoValue !== undefined) {
            queryParameters['luncho_value'] = requestParameters.lunchoValue;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/convert-from-luncho-all`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(LunchoResultFromJSON));
    }

    /**
     * Convert From Luncho All
     */
    async convertFromLunchoAll(requestParameters: ConvertFromLunchoAllRequest): Promise<Array<LunchoResult>> {
        const response = await this.convertFromLunchoAllRaw(requestParameters);
        return await response.value();
    }

    /**
     * Convert From Luncho Dummy
     */
    async convertFromLunchoDummyRaw(requestParameters: ConvertFromLunchoDummyRequest): Promise<runtime.ApiResponse<any>> {
        if (requestParameters.currencyCode === null || requestParameters.currencyCode === undefined) {
            throw new runtime.RequiredError('currencyCode','Required parameter requestParameters.currencyCode was null or undefined when calling convertFromLunchoDummy.');
        }

        if (requestParameters.lunchoValue === null || requestParameters.lunchoValue === undefined) {
            throw new runtime.RequiredError('lunchoValue','Required parameter requestParameters.lunchoValue was null or undefined when calling convertFromLunchoDummy.');
        }

        const queryParameters: any = {};

        if (requestParameters.currencyCode !== undefined) {
            queryParameters['currency_code'] = requestParameters.currencyCode;
        }

        if (requestParameters.lunchoValue !== undefined) {
            queryParameters['luncho_value'] = requestParameters.lunchoValue;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/convert-from-luncho-dummy/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.TextApiResponse(response) as any;
    }

    /**
     * Convert From Luncho Dummy
     */
    async convertFromLunchoDummy(requestParameters: ConvertFromLunchoDummyRequest): Promise<any> {
        const response = await this.convertFromLunchoDummyRaw(requestParameters);
        return await response.value();
    }

    /**
     * Countries
     */
    async countriesRaw(): Promise<runtime.ApiResponse<{ [key: string]: IMFPPPCountry; }>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/countries`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => runtime.mapValues(jsonValue, IMFPPPCountryFromJSON));
    }

    /**
     * Countries
     */
    async countries(): Promise<{ [key: string]: IMFPPPCountry; }> {
        const response = await this.countriesRaw();
        return await response.value();
    }

    /**
     * Test
     */
    async testRaw(requestParameters: TestRequest): Promise<runtime.ApiResponse<LunchoResult>> {
        const queryParameters: any = {};

        if (requestParameters.countryCode !== undefined) {
            queryParameters['country_code'] = requestParameters.countryCode;
        }

        if (requestParameters.lunchoValue !== undefined) {
            queryParameters['luncho_value'] = requestParameters.lunchoValue;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        const response = await this.request({
            path: `/test/`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => LunchoResultFromJSON(jsonValue));
    }

    /**
     * Test
     */
    async test(requestParameters: TestRequest): Promise<LunchoResult> {
        const response = await this.testRaw(requestParameters);
        return await response.value();
    }

}
