# Tesla API

This is a package for connecting to the Tesla API.

## Usage

```python
from tesla_api import TeslaApiClient

client = ApiClient('your@email.com', 'yourPassword')

vehicles = client.list_vehicles()

for v in vehicles:
    print(v.vin)
    v.controls.flash_lights()
```