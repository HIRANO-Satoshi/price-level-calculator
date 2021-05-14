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
        this.api = api;
    }
    luncho(params) {
        return __awaiter(this, void 0, void 0, function* () {
            const calc = (lunchoValue) => {
                var result = lodash_1.cloneDeep(this.lunchoResult);
                result.dollar_per_luncho * result.ppp * lunchoValue;
                return result;
            };
            if (this.lunchoResult) {
                return Promise.resolve(calc(params.lunchoValue));
            }
            this.api.luncho(params)
                .then((result) => {
                this.lunchoResult = result;
                return calc(params.lunchoValue);
            });
        });
    }
}
exports.Luncho = Luncho;
