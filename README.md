# Tesla API

This is a package for connecting to the Tesla API.

## Usage for a vehicle

```python
import asyncio
from tesla_api import TeslaApiClientAsync

async def main():
    client = TeslaApiClientAsync('your@email.com', 'yourPassword')

    vehicles = await client.list_vehicles()

    for v in vehicles:
        print(v.vin)
        await v.controls.flash_lights()

asyncio.run(main())
```


## Usage for Powerwall 2

```python
import asyncio
from tesla_api import TeslaApiClientAsync

async def main():
    client = TeslaApiClientAsync('your@email.com', 'yourPassword')

    energy_sites = await client.list_energy_sites()
    print("Number of energy sites = %d" % (len(energy_sites)))
    assert(len(energy_sites)==1)
    reserve = await energy_sites[0].get_backup_reserve_percent()
    print("Backup reserve percent = %d" % (reserve))
    print("Increment backup reserve percent")
    await energy_sites[0].set_backup_reserve_percent(reserve+1)

asyncio.run(main())
```

## Synchronous interface

There is also a legacy synchronous interface available if not using an asyncio loop in your project:

```python
from tesla_api import TeslaApiClient

client = TeslaApiClient('your@email.com', 'yourPassword')

vehicles = client.list_vehicles()

for v in vehicles:
    print(v.vin)
    v.controls.flash_lights()
```
