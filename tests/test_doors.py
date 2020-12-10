import pytest


@pytest.mark.asyncio
async def test_Vehicle_Status_Doors(vehicle):
    doors = vehicle.controls.doors
    assert doors.front_driver_door_open is False
    assert doors.front_passanger_door_open is False
    assert doors.rear_driver_door_open is False
    assert doors.rear_passenger_door_open is False
