import pytest


@pytest.mark.asyncio
async def test_TeslaApiClient_get_vehicle(client, vehicle, mocker):
    async def result():
        return vehicle
    mocker.patch.object(client, "get_vehicle", return_value=result())
    assert await client.get_vehicle("Lightning McQueen") is vehicle


@pytest.mark.asyncio
async def test_TeslaApiClient_list_vehicles(client, vehicle, mocker):
    async def result():
        return [vehicle]

    mocker.patch.object(client, "list_vehicles", return_value=result())
    assert len(await client.list_vehicles())
