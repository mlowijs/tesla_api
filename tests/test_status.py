import pytest
from conftest import vehi
from data import *


@pytest.mark.asyncio
async def test_Vehicle_Status(vehicle):
    status = vehicle.status
    assert str(status.gps_last_update.date()) == "1970-01-19"
    assert status.heading == 358
    assert str(status.last_update.date()) == "2020-11-18"
    assert status.latitude == 59.917045
    assert status.longitude == 7.981791
    assert status.native_latitude == 59.917045
    assert status.native_location_supported is True
    assert status.native_longitude == 7.981791
    assert status.native_type == "wgs"
    assert status.power == 0
    assert status.shift_state is None
    assert status.speed is None


@pytest.mark.asyncio
async def test_Vehicle_Status_refresh(client, mocker):
    v = vehi(client, mocker, DRIVE_STATE)
    r = await v.status.refresh()
    assert isinstance(r, dict)
