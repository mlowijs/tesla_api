import pytest
from conftest import vehi
from data import *


@pytest.mark.asyncio
async def test_Vehicle_Climate_attributes(vehicle):
    climate = vehicle.climate
    assert climate.battery_heater is False
    assert climate.battery_heater_no_power is False
    assert climate.climate_keeper_mode == "off"
    assert climate.defrost_mode == 0
    assert climate.driver_temp_setting == 20.5
    assert climate.fan_status == 0
    assert climate.inside_temp == 13.0
    assert climate.is_auto_conditioning_on is False
    assert climate.is_climate_on is False
    assert climate.is_front_defroster_on is False
    assert climate.is_preconditioning is False
    assert climate.is_rear_defroster_on is False
    assert str(climate.last_update.date()) == "2020-11-18"
    assert climate.left_temp_direction == 0
    assert climate.max_avail_temp == 28.0
    assert climate.min_avail_temp == 15.0
    assert climate.outside_temp == 12.0
    assert climate.passenger_temp_setting == 20.5
    assert climate.remote_heater_control_enabled is False
    assert climate.right_temp_direction == 0
    assert climate.seat_heater_left == 0
    assert climate.seat_heater_rear_center == 0
    assert climate.seat_heater_rear_left == 0
    assert climate.seat_heater_rear_right == 0
    assert climate.seat_heater_right == 0
    assert climate.side_mirror_heaters is False
    assert climate.wiper_blade_heater is False


@pytest.mark.asyncio
async def test_Vehicle_refresh(client, mocker):
    v = vehi(client, mocker, CLIMATE_STATE)
    data = await v.climate.refresh()
    assert data == CLIMATE_STATE


@pytest.mark.asyncio
async def test_Vehicle_Climate_set_seat_heater(vehicle):

    with pytest.raises(ValueError):
        await vehicle.climate.set_seat_heater(-1)
    with pytest.raises(ValueError):
        await vehicle.climate.set_seat_heater(seat=99)

    await vehicle.climate.set_seat_heater(temp=3, seat=0)


@pytest.mark.asyncio
async def test_Vehicle_Climate_start_climate(vehicle):
    await vehicle.climate.start_climate()


@pytest.mark.asyncio
async def test_Vehicle_Climate_stop_climate(vehicle):
    await vehicle.climate.stop_climate()


@pytest.mark.asyncio
async def test_Vehicle_Climate_enable_max_defrost(vehicle):
    await vehicle.climate.enable_max_defrost()


@pytest.mark.asyncio
async def test_Vehicle_Climate_disable_max_defrost(vehicle):
    await vehicle.climate.disable_max_defrost()


@pytest.mark.asyncio
async def test_Vehicle_Climate_set_temperature(vehicle):
    await vehicle.climate.set_temperature(driver_temperature=21, passenger_temperature=28)


@pytest.mark.asyncio
async def test_Vehicle_Climate_start_steering_wheel_heater(vehicle):
    await vehicle.climate.start_steering_wheel_heater()


@pytest.mark.asyncio
async def test_Vehicle_Climate_stop_steering_wheel_heater(vehicle):
    await vehicle.climate.stop_steering_wheel_heater()
