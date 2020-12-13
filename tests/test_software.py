from datetime import datetime

import pytest
from conftest import vehi


"""
        "software_update": {
            "download_perc": 100,
            "expected_duration_sec": 2700,
            "install_perc": 1,
            "status": "",
            "version": "2020.48.10",
        },

        DEBUG:asserted.utils:Value for Software.download_percent is 1
DEBUG:asserted.utils:Value for Software.install_percent is 1
DEBUG:asserted.utils:Value for Software.status is
DEBUG:asserted.utils:Value for Software.update_available is False
DEBUG:asserted.utils:Value for Software.version is
"""



def test_Vehicle_Controls_Software_attributes(vehicle):
    software = vehicle.controls.software
    assert isinstance(software.done_at, datetime)
    assert software.install_percent == 1
    assert software.download_percent == 100
    assert software.status == ""
    assert software.update_available is True
    assert software.version == "2020.48.10"

@pytest.mark.asyncio
async def test_Vehicle_Controls_Software_update(client, mocker):
    v = vehi(client, mocker, {"result": True})
    software = v.controls.software
    assert await software.update(datetime.now())
    assert await software.update(99999)

@pytest.mark.asyncio
async def test_Vehicle_Controls_Software_cancel_update(client, mocker):
    v = vehi(client, mocker, {"result": True})
    software = v.controls.software
    assert await software.cancel_update()
