import pytest


def test_Vehicle_Status_Trunks(vehicle):
    trunks = vehicle.controls.trunks
    assert trunks.frunk_open is False
    assert trunks.trunk_open is False


# test methods here.
