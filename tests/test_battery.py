

def test_Vehicle_Battery_attributes(vehicle):
    battery = vehicle.battery
    assert battery.estimated_range == 225.63
    assert battery.heater_on is False
    assert battery.ideal_range == 299.21
    assert battery.not_enough_power_to_heat is False
    assert battery.range == 299.21
    assert battery.soc == 60
    assert battery.usable_soc == 60
