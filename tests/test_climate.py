import pytest


@pytest.mark.asyncio
async def test_Vehicle_Climate_attributes(vehicle):
    climate = vehicle.climate
    assert climate.battery_heater is False
    assert climate.battery_heater_no_power is None
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