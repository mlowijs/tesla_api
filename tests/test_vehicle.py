import pytest
from conftest import vehi
from data import *


@pytest.mark.asyncio
async def test_Vehicle_attributes(vehicle):
    assert vehicle.access_type == "OWNER"
    assert vehicle.api_version == 12
    assert vehicle.car_version == "2020.44.10.1 955dc1dd145e"
    assert vehicle.color == "SolidBlack"
    assert vehicle.name == "888888"
    assert vehicle.id == 999999999999
    assert vehicle.id_s == "999999999999"
    assert vehicle.in_service is False
    assert str(vehicle.last_update.date()) == "2020-11-18"
    assert vehicle.odometer == 2652.51
    assert vehicle.state == "online"
    assert vehicle.tokens == ["dae9f13e1889e1e1", "1ad6b8d43a795273"]
    assert vehicle.vin == "5YJ3E7EB4LF999999"
    assert len(vehicle.option_codes)

    with pytest.raises(AttributeError):
        assert vehicle.non_existing_att

    with pytest.raises(KeyError):
        assert vehicle._data["looooool"]


@pytest.mark.asyncio
async def test_Vehicle_get_charge_state(client, mocker):
    v = vehi(client, mocker, CHARGE_STATE)
    r = await v.get_charge_state()
    assert r == CHARGE_STATE


@pytest.mark.asyncio
async def test_Vehicle_get_climate_state(client, mocker):
    v = vehi(client, mocker, CLIMATE_STATE)
    r = await v.get_climate_state()
    assert r == CLIMATE_STATE


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_Vehicle_compose_image(vehicle):
    # This test works when i test it manually but fails in the suit.
    data = await vehicle.compose_image("STUD_SIDE")
    assert len(data)


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_Vehicle_address(vehicle):
    # lat lon to the royal palace in Oslo.
    # allow this to fail if the remote service is down.
    data = await vehicle.address(59.916911, 10.727567)
    assert "Det kongelige slott" in data


@pytest.mark.asyncio
@pytest.mark.skip(reason="#TODO")
async def test_Vehicle_nearby_charging_sites(vehicle):
    # data = await vehicle.nearby_charging_sites()
    pass


@pytest.mark.asyncio
async def test_Vehicle_is_mobile_access_enabled(client, mocker):
    v = vehi(client, mocker, True)
    result = await v.is_mobile_access_enabled()
    assert result is True


@pytest.mark.asyncio
async def test_Vehicle_get_data(client, mocker):
    v = vehi(client, mocker, CHARGE_STATE)
    r = await v.get_data()
    assert r == CHARGE_STATE


@pytest.mark.asyncio
async def test_Vehicle_full_update(client, mocker):
    v = vehi(client, mocker, FULL_DATA)
    r = await v.get_data()
    assert r == FULL_DATA


@pytest.mark.asyncio
async def test_Vehicle_get_state(client, mocker):
    v = vehi(client, mocker, VEHICLE_STATE)
    r = await v.get_state()
    assert isinstance(r, dict)


@pytest.mark.asyncio
async def test_Vehicle_get_drive_state(client, mocker):
    v = vehi(client, mocker, DRIVE_STATE)
    r = await v.get_data()
    assert r == DRIVE_STATE


@pytest.mark.asyncio
async def test_Vehicle_get_gui_settings(client, mocker):
    v = vehi(client, mocker, GUI_SETTINGS)
    r = await v.get_data()
    assert r == GUI_SETTINGS


@pytest.mark.asyncio
@pytest.mark.skip(reason="#TODO")
async def test_Vehicle_wake_up(vehicle):
    pass


@pytest.mark.asyncio
@pytest.mark.skip(reason="#TODO")
async def test_Vehicle_remote_start(vehicle):
    pass


@pytest.mark.asyncio
async def test_Vehicle_refresh(client, mocker):
    v = vehi(client, mocker, ATTRS)
    r = await v.refresh()
    assert r == ATTRS
