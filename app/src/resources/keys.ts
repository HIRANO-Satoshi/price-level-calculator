export class KeysValueConverter {
    toView(obj) {
        if (typeof obj === 'undefined' || obj === null)
            return [];
        return Object.keys(obj);
    }
  }
