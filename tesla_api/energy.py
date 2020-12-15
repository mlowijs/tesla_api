##############################################################################
# Class to manage a Powerwall (tested on one Powerwall 2) via the Tesla API
##############################################################################
# MIT License
#
# Copyright (c) 2019 S.W. Moore
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import date, datetime, time
from typing import Optional, Union


class Energy:
    def __init__(self, api_client, energy_site_id):
        self._api_client = api_client
        self._energy_site_id = energy_site_id

    @property
    def site_id(self):
        return self._energy_site_id

    async def get_energy_site_info(self):
        return await self._api_client.get(
            "energy_sites/{}/site_info".format(self._energy_site_id))

    # Helper functions for get_energy_site_info
    async def get_backup_reserve_percent(self):
        info = await self.get_energy_site_info()
        return int(info["backup_reserve_percent"])

    async def get_operating_mode(self):
        info = await self.get_energy_site_info()
        return info["default_real_mode"]

    async def get_version(self):
        info = await self.get_energy_site_info()
        return info["version"]

    async def get_battery_count(self):
        info = await self.get_energy_site_info()
        return int(info["battery_count"])

    async def get_energy_site_calendar_history_data(
            self, kind="energy", period="day",
            end_date: Optional[Union[str, date]] = None) -> dict:
        """Return historical energy data.

        Args:
            kind: [power, energy, self_consumption]
            period: Amount of time to include in report. One of day, week, month, year,
                and lifetime. When kind is 'power', this parameter is ignored, and the
                period is always 'day'.
            end_date: A date/datetime object, or a str in ISO 8601 format
                (e.g. 2019-12-23T17:39:18.546Z). The response report interval ends at this
                datetime and starts at the beginning of the given period. For example,
                with datetime(year=2020, month=5, day=1), this gets all data for May 1st.
                Defaults to the current time.
        """
        params = {"kind": kind, "period": period}

        if isinstance(end_date, date):
            if not isinstance(end_date, datetime):
                end_date = datetime.combine(end_date, time(23, 59, 59))
            elif end_date.hour == 0 and end_date.minute == 0:
                # If the datetime object's time is 00:00 then the API returns nothing.
                # We adjust by adding 23:59, so it's possible to use
                # datetime(year=2020, month=5, day=2) and it gets the data for
                # May 2, 2020 as expected.
                end_date = end_date.replace(hour=23, minute=59, second=59)
            end_date = end_date.isoformat()

        if end_date is not None:
            params["end_date"] = end_date

        return await self._api_client.get(
            "energy_sites/{}/calendar_history".format(self._energy_site_id), params=params)

    async def get_energy_site_live_status(self):
        return await self._api_client.get(
            "energy_sites/{}/live_status".format(self._energy_site_id))

    # Helper functions for get_energy_site_live_status
    async def get_energy_site_live_status_percentage_charged(self):
        status = await self.get_energy_site_live_status()
        return int(status["percentage_charged"])

    async def get_energy_site_live_status_energy_left(self):
        status = await self.get_energy_site_live_status()
        return float(status["energy_left"])

    async def get_energy_site_live_status_total_pack_energy(self):
        status = await self.get_energy_site_live_status()
        return int(status["total_pack_energy"])

    async def get_solar_power(self):
        status = await self.get_energy_site_live_status()
        return int(status["solar_power"])

    # Setting of the backup_reserve_percent used in self_consumption
    # (i.e. self-powered mode).
    # On my Powerwall 2, setting backup_reserve_percent > energy_left
    # causes the battery to charge at 1.7kW
    async def set_backup_reserve_percent(self, backup_reserve_percent):
        assert 0 <= backup_reserve_percent <= 100
        return await self._api_client.post(
            endpoint="energy_sites/{}/backup".format(self._energy_site_id),
            data={"backup_reserve_percent": backup_reserve_percent},
        )

    # Correspondence between mode names and the Tesla app:
    #   mode = 'self_consumption' = "self-powered" on app
    #   mode = 'backup' = "backup-only" on app
    #   mode = 'autonomous' = "Advanced - Time-based control" on app
    # Note: setting 'backup' mode causes my Powerwall 2 to charge at 3.4kW
    async def set_operating_mode(self, mode):
        return await self._api_client.post(
            endpoint="energy_sites/{}/operation".format(self._energy_site_id),
            data={"default_real_mode": mode})

    # helper functions for set_operating_mode
    async def set_operating_mode_self_consumption(self):
        return await self.set_operating_mode("self_consumption")

    async def set_operating_mode_backup(self):
        return await self.set_operating_mode("backup")

    async def set_operating_mode_autonomous(self):
        return await self.set_operating_mode("autonomous")
