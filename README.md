# Tesla API

This is a package for connecting to the Tesla API.

## Usage for a vehicle

```python
from tesla_api import TeslaApiClient

client = TeslaApiClient('your@email.com', 'yourPassword')

vehicles = client.list_vehicles()

for v in vehicles:
    print(v.vin)
    v.controls.flash_lights()
```


## Usage for Powerwall 2

```python
from tesla_api import TeslaApiClient

client = TeslaApiClient('your@email.com', 'yourPassword')

energy_sites = client.list_energy_sites()
print("Number of energy sites = %d" % (len(energy_sites)))
assert(len(energy_sites)==1)
reserve = energy_sites[0].get_backup_reserve_percent()
print("Backup reserve percent = %d" % (reserve))
print("Increment backup reserve percent")
energy_sites[0].set_backup_reserve_percent(reserve+1)
```
