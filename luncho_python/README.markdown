# Luncho client library for Python

- This client library includes a fast hand-written API core ([./luncho_python/api/luncho.py](./luncho_python/api/luncho.py)), a hand written
  README.markdown (this file), and auto-generated files by OpenAPI generator including [README.md](./README.md).
- Use the fast hand-written [./luncho_python/api/luncho.py](./luncho_python/api/luncho.py) rather than
  auto-generated [./luncho_python/api/luncho_api.py](./luncho_python/api/luncho_api.py)
  because luncho.py is much faster with caching and it provides functions for data conversion in addition to functions found in luncho_api.py.


## Example

- See [../server/test/test_client_lib.py](../server/test/test_client_lib.py) for example.

## Usage

- Since a pypi package is not available yet, use a symlink.

```
    cd LOCATION
    git clone https://github.com/HIRANO-Satoshi/luncho.git
    cd luncho/luncho_python

    cd YOUR_SRC
    ln -s LOCATION/luncho/luncho_python .
```

```
    import luncho_python
    from luncho_python.api import luncho_api, luncho
    from luncho_python.model.luncho_data import LunchoData

    configuration = luncho_python.Configuration(
        host = "http://luncho-index.org"
        # host = "http://localhost:8000"
    )

    country_code = 'JP'   # ISO 2 letter counry code

    self.api_client = luncho_python.ApiClient(configuration)
    self.luncho   = luncho.Luncho(self.api_client)

    # Get a local currency value from the a Luncho value.
    jpy: float = self.luncho.get_currency_from_luncho(100.0, country_code)

    # Get a US Dollar value from a Luncho value.
    usd: float = self.luncho.get_US_dollar_from_luncho(100.0, country_code)

    # Get a LunchoData to see info such as currency_code and exchange rate
    lunchoData: LunchoData = self.luncho.get_luncho_data(country_code)

    # Get a dict of supported county codes and names
    data: Dict[CountryCode, str] = self.luncho.get_countries()

    # Load or get a dict of LunchoDatas for supported countries.  Data size is about 40KB.
    # If you show data of all countries, call this before in order to load all LunchoDatas at once,
    # or it loads LunchoData one by one and that is very slow.
    self.luncho.get_all_luncho_data()
```
- See comments for detail on [./luncho_python/api/luncho.py](./luncho_python/api/luncho.py).
 - Read auto-generated [README.md](./README.md), too.

## Cached data

  - You can use cached data inside self.luncho. Caution that these data will be gone when expired or
    reloaded.
  - These variables are available.

```
        self.luncho.lunchoDataCache: Dict[CountryCode, LunchoData] = {}  # Cache {CountryCode: LunchoData}
        self.luncho.allLunchoDatasExpiration: float = 0.0;
        self.luncho.countryCache: Dict[CountryCode, str] = {}       # { CountryCode: name }
```
