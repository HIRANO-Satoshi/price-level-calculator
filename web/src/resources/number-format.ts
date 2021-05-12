import 'numeral'
declare function require(x: string): any;
var numeral = require('numeral')

export class NumberFormatValueConverter {
    toView(value, format) {
        if (value === null || typeof value === 'undefined' || isNaN(value)) {
            return null;
        }
        return numeral(value).format(format);
    }
    
    fromView(value, format) {
        if (value === '')
            return null;
        return numeral().unformat(value);
    }
}
