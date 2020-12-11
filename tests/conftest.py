import asyncio

import pytest
from data import (CHARGE_STATE, DRIVE_STATE, FULL_DATA, GUI_SETTINGS,
                  VEHICLE_STATE)
from tesla_api import TeslaApiClient
from tesla_api.vehicle import Vehicle


@pytest.fixture(scope="session")
def client():

    fake_client = TeslaApiClient("fake@email.com", "fake_password")

    return fake_client


@pytest.fixture()
def vehicle(client, mocker):

    v = Vehicle(client, FULL_DATA)
    # never for the the mock to work..
    # just patching this manually since it will not work anyway.
    async def _command(command_endpoint, data=None, _retry=True):
        return True
    v._command = _command

    return v
