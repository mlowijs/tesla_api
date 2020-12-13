import pytest
from conftest import FULL_DATA, AsyncMock, MagicMock
from tesla_api.exceptions import ApiError


@pytest.mark.asyncio
async def test_TeslaApiClient_get_vehicle(client, vehicle, mocker):
    mocker.patch.object(client, "get_vehicle", new=AsyncMock(return_value=vehicle))
    assert await client.get_vehicle("Lightning McQueen") is vehicle


@pytest.mark.asyncio
async def test_TeslaApiClient_list_vehicles(client, vehicle, mocker):
    mocker.patch.object(client, "list_vehicles", new=AsyncMock(return_value=[vehicle]))
    assert len(await client.list_vehicles())


@pytest.mark.asyncio
async def test_TeslaApiClient_get(client, mocker, vehicle):
    ctx = MagicMock()
    resp = AsyncMock()

    ctx.__aenter__.return_value = resp
    ctx.__aexit__.return_value = resp
    err = AsyncMock(return_value={"error": "ICE > EV"})
    ok = AsyncMock(return_value={"response": FULL_DATA})
    resp.json = err

    mocker.patch.object(client, "_get_headers", return_value={"hello": "you"})
    mocker.patch.object(client, "authenticate", new=AsyncMock(return_value=None))
    mocker.patch.object(client._session, "get", return_value=ctx)

    with pytest.raises(ApiError):
        await client.get("vehicles")

    resp.json = ok

    raw = await client.get("vehicles")
    assert raw == FULL_DATA == vehicle._data


@pytest.mark.asyncio
@pytest.mark.skip()
async def test_TeslaApiClient_list_energy_sites(client, mocker, vehicle):
    data = await client.list_energy_sites()
