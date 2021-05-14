"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
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
exports.LunchoFast = void 0;
const aurelia_framework_1 = require("aurelia-framework");
const LunchoApi_1 = require("luncho-typescript-aurelia/LunchoApi");
const lodash_1 = require("lodash");
/** Luncho calculator fast version with caching.  */
let LunchoFast = class LunchoFast extends LunchoApi_1.LunchoApi {
    constructor() {
        super(...arguments);
        this.lunchoResults = new Map(); // Cache {CountryCode: LunchoResult}
    }
    /**
       Fast Luncho calculation using cache.
    */
    luncho(params) {
        const _super = Object.create(null, {
            luncho: { get: () => super.luncho }
        });
        return __awaiter(this, void 0, void 0, function* () {
            const lunchoResult = this.lunchoResults.get(params.countryCode);
            if (lunchoResult) {
                var result = lodash_1.cloneDeep(this.lunchoResults.get(params.countryCode));
                result.local_currency_value = result.dollar_per_luncho * result.ppp * params.lunchoValue;
                result.dollar_value = result.local_currency_value / result.exchange_rate;
                return Promise.resolve(result);
            }
            return _super.luncho.call(this, params)
                .then((result) => {
                this.lunchoResults.set(params.countryCode, lodash_1.cloneDeep(result));
                return result;
            });
        });
    }
};
LunchoFast = __decorate([
    aurelia_framework_1.autoinject
], LunchoFast);
exports.LunchoFast = LunchoFast;
