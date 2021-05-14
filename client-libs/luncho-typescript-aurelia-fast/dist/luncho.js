"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Luncho = void 0;
const lodash_1 = require("lodash");
/** Luncho calculator fast version with caching.  */
class Luncho {
    constructor(api) {
        this.lunchoResults = new Map(); // Cache {CountryCode: LunchoResult}
        this.api = api;
    }
    /**
       Fast Luncho calculation using cache.
    */
    luncho(params) {
        return __awaiter(this, void 0, void 0, function* () {
            const lunchoResult = this.lunchoResults.get(params.countryCode);
            if (lunchoResult) {
                var result = lodash_1.cloneDeep(this.lunchoResults.get(params.countryCode));
                result.local_currency_value = result.dollar_per_luncho * result.ppp * params.lunchoValue;
                result.dollar_value = result.local_currency_value / result.exchange_rate;
                return Promise.resolve(result);
            }
            this.api.luncho(params)
                .then((result) => {
                this.lunchoResults.set(params.countryCode, lodash_1.cloneDeep(result));
                return result;
            });
        });
    }
}
exports.Luncho = Luncho;
