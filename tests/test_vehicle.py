
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


# Add test for methods here.
