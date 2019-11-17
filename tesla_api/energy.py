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

class Energy:
    def __init__(self, api_client, energy_site_id):
        self._api_client = api_client
        self._energy_site_id = energy_site_id

    def get_energy_site_info(self):
        return self._api_client.get('energy_sites/{}/site_info'.format(self._energy_site_id))

    # Helper functions for get_energy_site_info
    def get_backup_reserve_percent(self):
        return int(self.get_energy_site_info()["backup_reserve_percent"])
    def get_operating_mode(self):
        return self.get_energy_site_info()["default_real_mode"]
    def get_version(self):
        return self.get_energy_site_info()["version"]
    def get_battery_count(self):
        return int(self.get_energy_site_info()["battery_count"])

    def get_energy_site_live_status(self):
        return self._api_client.get('energy_sites/{}/live_status'.format(self._energy_site_id))

    # Helper functions for get_energy_site_live_status
    def get_energy_site_live_status_percentage_charged(self):
        return int(self.get_energy_site_live_status()["percentage_charged"])
    def get_energy_site_live_status_total_pack_energy(self):
        return float(self.get_energy_site_live_status()["energy_left"])
    def get_energy_site_live_status_total_pack_energy(self):
        return int(self.get_energy_site_live_status()["total_pack_energy"])

    # Setting of the backup_reserve_percent used in self_consumption
    # (i.e. self-powered mode).
    # On my Powerwall 2, setting backup_reserve_percent > energy_left
    # causes the battery to charge at 1.7kW
    def set_backup_reserve_percent(self, backup_reserve_percent):
        assert(backup_reserve_percent>=0)
        assert(backup_reserve_percent<=100)
        return self._api_client.post(
            endpoint='energy_sites/{}/backup'.format(self._energy_site_id),
            data={"backup_reserve_percent": backup_reserve_percent}
            )

    # Correspondence between mode names and the Tesla app:
    #   mode = 'self_consumption' = "self-powered" on app
    #   mode = 'backup' = "backup-only" on app
    #   mode = 'autonomous' = "Advanced - Time-based control" on app
    # Note: setting 'backup' mode causes my Powerwall 2 to charge at 3.4kW
    def set_operating_mode(self, mode):
        return self._api_client.post(
            endpoint='energy_sites/{}/operation'.format(self._energy_site_id),
            data={"default_real_mode": mode}
            )

    # helper functions for set_operating_mode
    def set_operating_mode_self_consumption(self):
        return self.set_operating_mode('self_consumption')
    def set_operating_mode_backup(self):
        return self.set_operating_mode('backup')
    def set_operating_mode_autonomous(self):
        return self.set_operating_mode('autonomous')
    # Functions to set parameters for 'autonomous' mode have not yet been
    # written since you're probably better off using the Tesla app if you
    # want to configure the gateway for time-based controls (i.e. so that
    # it autonomously decides when to charge and discharge).
