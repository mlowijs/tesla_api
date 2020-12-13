from datetime import datetime

import pytest
from conftest import vehi


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
