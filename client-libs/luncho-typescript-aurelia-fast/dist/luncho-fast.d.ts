import { LunchoResult } from 'luncho-typescript-aurelia/models';
import { LunchoApi, ILunchoParams } from 'luncho-typescript-aurelia/LunchoApi';
/** Luncho calculator fast version with caching.  */
export declare class LunchoFast extends LunchoApi {
    lunchoResults: Map<string, LunchoResult>;
    /**
       Fast Luncho calculation using cache.
    */
    luncho(params: ILunchoParams): Promise<LunchoResult>;
}
