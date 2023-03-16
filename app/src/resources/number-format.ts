/**
   Number formatter using numeral.js.

   Usage:

     ${local_currency_value | numberFormat: '0.00'}
 */
import * as numeral from 'numeral';

export class NumberFormatValueConverter {
    toView(value: number, format: string) {
        if (value === null || typeof value === 'undefined' || isNaN(value)) {
            return null;
        }
        return numeral(value).format(format);
    }

    // fromView(value, format) {
    //     if (value === '')
    //         return null;
    //     return numeral().unformat(value);
    // }
}
