import pytest


@pytest.mark.asyncio
async def test_Vehicle_Gui_attributes(vehicle):
    gui = vehicle.gui
    assert gui.charge_rate_unit == "kW"
    assert gui.distance_unit == "km/hr"
    assert str(gui.last_update.date()) == "2020-11-18"
    assert gui.range_unit == "Rated"
    assert gui.temperature_unit == "C"
    assert gui.twenty_four_hour is True
