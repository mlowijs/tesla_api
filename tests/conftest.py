import pytest
from data import (CHARGE_STATE, DRIVE_STATE, FULL_DATA, GUI_SETTINGS,
                  VEHICLE_STATE)
from tesla_api import TeslaApiClient
from tesla_api.vehicle import Vehicle


@pytest.fixture()
def client():

    fake_client = TeslaApiClient("fake@email.com", "fake_password")

    return fake_client


@pytest.fixture()
def vehicle(client, mocker):
    #mocker.patch.object(client.get_vehicle, Vehicle(client, FULL_DATA))

    return Vehicle(client, FULL_DATA)
