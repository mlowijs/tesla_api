import pytest


@pytest.mark.asyncio
def test_Vehicle_Status_Trunks(vehicle):
    trunks = vehicle.controls.trunks
    assert trunks.frunk_open is False
    assert trunks.trunk_open is False


@pytest.mark.asyncio
async def test_Vehicle_Status_Trunks_open_frunk(vehicle):
    trunks = vehicle.controls.trunks
    assert await trunks.open_frunk() is True


@pytest.mark.asyncio
async def test_Vehicle_Status_Trunks_open_trunk(vehicle):
    trunks = vehicle.controls.trunks
    assert await trunks.open_trunk() is True
