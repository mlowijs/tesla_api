
import pytest


@pytest.mark.asyncio
async def test_Vehicle_attributes(vehicle):
    assert vehicle.access_type == "OWNER"
    assert vehicle.api_version == 12
    assert vehicle.car_version == "2020.44.10.1 955dc1dd145e"
    assert vehicle.color == "SolidBlack"
    assert vehicle.display_name == "888888"
    assert vehicle.id == 999999999999
    assert vehicle.id_s == "999999999999"
    assert vehicle.in_service is False
    assert str(vehicle.last_update.date()) == "2020-11-18"
    assert vehicle.odometer == 1024.1678860374077
    assert vehicle.state == "online"
    assert vehicle.tokens == ['dae9f13e1889e1e1', '1ad6b8d43a795273']
    assert vehicle.vin == "5YJ3E7EB4LF999999"

    with pytest.raises(AttributeError):
        assert vehicle.non_existing_att

    with pytest.raises(KeyError):
        assert vehicle._data["looooool"]




@pytest.mark.asyncio
async def _test_Vehicle_get_charge_state(vehicle):
    data = await vehicle.get_charge_state()
    # think the path dont work here.
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def _test_Vehicle_get_climate_state(vehicle):
    data = await vehicle.get_climate_state()
    # think the path dont work here.
    assert isinstance(data, dict)



@pytest.mark.asyncio
async def test_Vehicle_compose_image(vehicle): # TEST AND FIXME
    data = await vehicle.compose_image("STUD_SIDE")


@pytest.mark.asyncio
async def test_Vehicle_address(vehicle):
    # lat lon to the royal palace in Oslo.
    data = await vehicle.address(59.916911, 10.727567)
    assert "Det kongelige slott" in data


@pytest.mark.asyncio
async def test_Vehicle_nearby_charging_sites(vehicle):
    #data = await vehicle.nearby_charging_sites()
    pass

@pytest.mark.asyncio
async def test_Vehicle_is_mobile_access_enabled(vehicle):
    #data = await vehicle.is_mobile_access_enabled()
    pass


@pytest.mark.asyncio
async def test_Vehicle_get_data(vehicle):
    pass


@pytest.mark.asyncio
async def test_Vehicle_full_update(vehicle):
    pass

@pytest.mark.asyncio
async def test_Vehicle_get_state(vehicle):
    pass


@pytest.mark.asyncio
async def test_Vehicle_get_drive_state(vehicle):
    pass

@pytest.mark.asyncio
async def test_Vehicle_get_gui_settings(vehicle):
    pass


@pytest.mark.asyncio
async def test_Vehicle_wake_up(vehicle):
    pass


@pytest.mark.asyncio
async def test_Vehicle_remote_start(vehicle):
    pass


@pytest.mark.asyncio
async def test_Vehicle_update(vehicle):
    pass
    # dunno wtf this does, just the attr so the car?
