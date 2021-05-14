import { autoinject } from 'aurelia-framework';
import { LunchoResult } from 'luncho-typescript-aurelia/models';
import { LunchoApi, ILunchoParams } from 'luncho-typescript-aurelia/LunchoApi';
import { cloneDeep as deepCopy } from 'lodash';


/** Luncho calculator fast version with caching.  */
@autoinject
export class LunchoFast extends LunchoApi {

    lunchoResults: Map<string, LunchoResult> = new Map();  // Cache {CountryCode: LunchoResult}

    /**
       Fast Luncho calculation using cache.
    */
    async luncho(params: ILunchoParams): Promise<LunchoResult> {
        const lunchoResult: LunchoResult = this.lunchoResults.get(params.countryCode);

        if (lunchoResult) {
            var result: LunchoResult = deepCopy(this.lunchoResults.get(params.countryCode)) as LunchoResult;
            result.local_currency_value = result.dollar_per_luncho * result.ppp * params.lunchoValue;
            result.dollar_value = result.local_currency_value / result.exchange_rate;
            return Promise.resolve(result);
        }

        return super.luncho(params)
            .then((result: LunchoResult) => {
                this.lunchoResults.set(params.countryCode, deepCopy(result));
                return result;
            });
    }
}
