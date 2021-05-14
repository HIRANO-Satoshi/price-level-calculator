import { LunchoResult } from '../typescript-aurelia/models';
import { LunchoApi, ILunchoParams } from '../typescript-aurelia/LunchoApi';
/** Luncho calculator fast version with caching.  */
export declare class Luncho {
    api: LunchoApi;
    lunchoResult: LunchoResult;
    constructor(api: LunchoApi);
    luncho(params: ILunchoParams): Promise<LunchoResult>;
}
