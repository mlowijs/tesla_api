# Tesla API

This is a package for connecting to the Tesla API.

## Usage for a vehicle

```python
import asyncio
from tesla_api import TeslaApiClient

async def main():
    client = TeslaApiClient('your@email.com', 'yourPassword')

    vehicles = await client.list_vehicles()

    for v in vehicles:
        print(v.vin)
        await v.controls.flash_lights()

asyncio.run(main())
```


## Usage for Powerwall 2

```python
import asyncio
from tesla_api import TeslaApiClient

async def main():
    client = TeslaApiClient('your@email.com', 'yourPassword')

    energy_sites = await client.list_energy_sites()
    print("Number of energy sites = %d" % (len(energy_sites)))
    assert(len(energy_sites)==1)
    reserve = await energy_sites[0].get_backup_reserve_percent()
    print("Backup reserve percent = %d" % (reserve))
    print("Increment backup reserve percent")
    await energy_sites[0].set_backup_reserve_percent(reserve+1)

asyncio.run(main())
```
