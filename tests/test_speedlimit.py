import pytest
from conftest import vehi


def test_Vehicle_Controls_Speedlimit_attributes(vehicle):
    speedlimit = vehicle.controls.speedlimit
    assert speedlimit.current_limit == 136.79
    assert speedlimit.current_limit_mph == 85.0
    assert speedlimit.is_active is False
    assert speedlimit.max_limit_mph == 90
    assert speedlimit.pin_code_set is False


@pytest.mark.asyncio
async def test_Vehicle_Controls_Speedlimit_activate_speed_limit(client, mocker):
    v = vehi(client, mocker, {"result": True})
    speedlimit = v.controls.speedlimit
    assert await speedlimit.activate_speed_limit(9999) is True


@pytest.mark.asyncio
async def test_Vehicle_Controls_Speedlimit_deactivate_speed_limit(vehicle):
    speedlimit = vehicle.controls.speedlimit
    assert await speedlimit.activate_speed_limit(1234) is True


@pytest.mark.asyncio
async def test_Vehicle_Controls_Speedlimit_set_speed_limit(client, mocker):
    v = vehi(client, mocker, {"result": True})
    speedlimit = v.controls.speedlimit
    with pytest.raises(ValueError):
        await speedlimit.set_speed_limit(99999)


    with pytest.raises(KeyError):
        v._data.pop("gui_settings")
        await speedlimit.set_speed_limit(90)


@pytest.mark.asyncio
async def test_Vehicle_Controls_Speedlimit_set_speed_clear_speed_limit_pin(vehicle):
    speedlimit = vehicle.controls.speedlimit
    with pytest.raises(ValueError):
        await speedlimit.clear_speed_limit_pin(0)
    await speedlimit.clear_speed_limit_pin("1234")
    await speedlimit.clear_speed_limit_pin(1234)
