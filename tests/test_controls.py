import pytest


@pytest.mark.asyncio
async def test_Vehicle_Controls_flash_lights(vehicle):
    controls = vehicle.controls
    assert await controls.flash_lights() is True


@pytest.mark.asyncio
async def test_Vehicle_Controls_honk_horn(vehicle):
    controls = vehicle.controls
    assert await controls.honk_horn() is True


@pytest.mark.asyncio
async def test_Vehicle_Controls_vent_sunroof(vehicle):
    controls = vehicle.controls
    assert await controls.vent_sunroof() is True


@pytest.mark.asyncio
async def test_Vehicle_Controls_close_sunroof(vehicle):
    controls = vehicle.controls
    assert await controls.close_sunroof() is True


@pytest.mark.asyncio
async def test_Vehicle_Controls_set_valet_mode(vehicle):
    controls = vehicle.controls
    assert await controls.set_valet_mode() is True
