# Tesla API

This is a package for connecting to the Tesla API.

## Usage for a vehicle

```python
import asyncio
from tesla_api import TeslaApiClient

async def main():
    async with TeslaApiClient('your@email.com', 'yourPassword') as client:
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

    await client.close()

asyncio.run(main())
```


## Reusing API tokens

To avoid needing to store login details, you can pass in a previous API token.
Each time a new API token is created (either from a new login, or by refreshing an
expired token), the `on_new_token` callback will be called.

```python
async def save_token(token):
    open("token_file", "w").write(token)

async def main():
    email = password = token = None
    try:
        token = open("token_file").read()
    except OSError:
        email = input("Email> ")
        password = input("Password> ")
    client = TeslaApiClient(email, password, token, on_new_token=save_token)
    ...
```

If you only want to verify and save a user's token for later use,
you could use the `authenticate()` method:
```python
async def main():
    async with TeslaApiClient(email, password, on_new_token=save_token) as client:
        await client.authenticate()
```
