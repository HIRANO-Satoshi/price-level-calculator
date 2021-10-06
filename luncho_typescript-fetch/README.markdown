# Luncho client library for TypeScript and Fetch

- Note that this client library has NOT BEEN TESTED AT ALL. PRs are welcome.

- This client library includes a fast hand-written API core [./src/apis/luncho.ts](./src/apis/luncho.ts), a hand written
  README.markdown (this file), and auto-generated files by OpenAPI generator including [README.md](./README.md).
- Use the fast hand-written [./luncho.ts](./luncho.ts) rather than auto-generated [./LunchoApi.ts](./LunchoApi.ts) to call the API. Because luncho.ts is much faster with caching and it provides functions for data conversion in addition to functions found in auto-generated LunchoApi.ts.

## Usage

- Since an npm package is not available yet, use a symlink.

```
    cd LOCATION
    git clone https://github.com/HIRANO-Satoshi/luncho.git
    cd luncho/luncho_typescript-fetch
    yarn install

    cd YOUR_SRC
    ln -s LOCATION/luncho/luncho_typescript-fetch .
```

```
    import { Luncho } from 'luncho_typescript-fetch/apis/luncho';

    luncho: Luncho;

    async func() {
      this.luncho = new Luncho();
      this.luncho.basePath = "https://luncho-index.org"
      // luncho.basePath = 'http://localhost:8000';

      var countryCode = 'JP';
      // var countryCode = await this.luncho.get_country_code();

      // get a local currency value from a Luncho value
      local_currency_value: number = await this.luncho.get_currency_from_luncho(100.0, countryCode);

      // get a dollar value from a Luncho value
      this.dollar_value = await this.luncho.get_US_dollar_from_luncho(100.0, countryCode);

      // get a Luncho Data for a country
      lunchoData: LunchoData = await this.luncho.get_luncho_data({countryCode: countryCode});

      // Load or get a dict of LunchoDatas for supported countries.  Data size is about 40KB.
      // If you show data of all countries, call this before in order to load all LunchoDatas at once,
      // or it loads LunchoData one by one and that is very slow.
      await this.luncho.get_all_luncho_data();

      // calculate local currency values for all countries
      for (var countryCode of Object.keys(this.luncho.lunchoDataCache)) {
          this.luncho.lunchoDataCache[countryCode]['local_currency_value'] = await this.luncho.get_currency_from_luncho(this.lunchoValue, countryCode);
          this.luncho.lunchoDataCache[countryCode]['dollar_value'] = await this.luncho.get_US_dollar_from_luncho(this.lunchoValue, countryCode);
      }
```

 - See comments for detail on [luncho.ts](./src/apis/luncho.ts).
 - Read auto-generated [README.md](./README.md), too.

## Cached data

  - You can use cached data inside self.luncho. Caution that these data will be gone when expired or
    reloaded.
  - These variables are available.

```
    this.luncho.lunchoDataCache: { [key: string]: LunchoData} = {};  // Cache {CountryCode: LunchoData}
    this.luncho.allLunchoDatasExpiration: number = 0;
    this.luncho.countryCache: { [key: string]: string; };
    this.luncho.countryCodeCache: string;
```

### Locales

  - Use [[https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DisplayNames][Intl.DisplayNames]] to show country names and currency names in your language. It is available in Chrome but not in Safari.

```
       if (intl.DisplayNames) {
           const intl: any = Intl
           var supportedLocales = intl.DisplayNames.supportedLocalesOf(navigator.languages[0])
           if (supportedLocales.length == 0)
               supportedLocales = ['en'];
           countryNames = new intl.DisplayNames(supportedLocales[0], {type: 'region'})
           currencyNames = new intl.DisplayNames(supportedLocales[0], {type: 'currency'})

           const local_countryName = countryNames.of('JP')
           const local_currencyName = currencyNames.of('JPY')
       }
```
