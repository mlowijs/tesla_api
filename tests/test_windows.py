import pytest


@pytest.mark.asyncio
async def test_Vehicle_Status_Windows_attributes(vehicle):
    windows = vehicle.controls.windows
    assert windows.passenger_window_open is False
    assert windows.rear_passenger_window_open is False
    assert windows.driver_window_open is False
    assert windows.rear_driver_window_open is False


@pytest.mark.asyncio
async def test_Vehicle_Status_Windows_driver_window_close(vehicle):
    windows = vehicle.controls.windows
    assert await windows.close() is True


@pytest.mark.asyncio
async def test_Vehicle_Status_Windows_passanger_window_vent(vehicle):
    windows = vehicle.controls.windows
    assert await windows.vent(1333, 1) is True
