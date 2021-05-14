import { LunchoResult } from 'luncho-typescript-aurelia/models';
import { LunchoApi, ILunchoParams } from 'luncho-typescript-aurelia/LunchoApi';
/** Luncho calculator fast version with caching.  */
export declare class Luncho {
    api: LunchoApi;
    lunchoResults: Map<string, LunchoResult>;
    constructor(api: LunchoApi);
    /**
       Fast Luncho calculation using cache.
    */
    luncho(params: ILunchoParams): Promise<LunchoResult>;
}
