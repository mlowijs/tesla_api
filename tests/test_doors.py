import pytest


@pytest.mark.asyncio
async def test_Vehicle_Status_Doors(vehicle):
    doors = vehicle.controls.doors
    assert doors.driver_door_open is False
    assert doors.passenger_door_open is False
    assert doors.rear_driver_door_open is False
    assert doors.rear_passenger_door_open is False
    assert doors.locked is True


@pytest.mark.asyncio
async def test_Vehicle_Status_Doors_lock(vehicle):
    doors = vehicle.controls.doors
    assert await doors.lock() is True


@pytest.mark.asyncio
async def test_Vehicle_Status_Doors_unlock(vehicle):
    doors = vehicle.controls.doors
    assert await doors.unlock() is True
