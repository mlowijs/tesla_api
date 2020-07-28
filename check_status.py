import asyncio
from tesla_api import TeslaApiClient
import datetime
import time
import os

async def main():
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    client = TeslaApiClient(username, password)

    vehicles = await client.list_vehicles()

    v = vehicles[0]
    await v.wake_up()
    await v.get_state()

    energy_sites = await client.list_energy_sites()

    e = energy_sites[0]
    print(e)
    charging_state = await v.charge.get_state()
    state = charging_state["charging_state"]
    try:
        while True:
            status = await e.get_energy_site_live_status()
            print(datetime.datetime.now(), "House:", status['load_power'], "Solar:", status['solar_power'],
                  "Percent:", f"{status['percentage_charged']:.2f}", "Car Charge:", state)
            if status['percentage_charged'] > 75:
                if state != "Charging" and status['load_power'] + 1000 < status['solar_power']:
                    desired_state = "Charging"
                elif state == "Charging" and status['load_power'] <= status['solar_power']:
                    desired_state = "Charging"
                else:
                    desired_state = "Stopped"
            else:
                desired_state = "Stopped"

            if state != desired_state:
                if desired_state == "Charging":
                    print("Starting charge")
                    await v.charge.start_charging()
                elif desired_state == "Stopped":
                    print("Stopping charge")
                    await v.charge.stop_charging()

            state = desired_state

            time.sleep(300)
    finally:
            await client.close()

asyncio.run(main())

