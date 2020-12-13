

def test_Vehicle_Battery_attributes(vehicle):
    battery = vehicle.battery
    assert battery.estimated_range == 140.2
    assert battery.heater_on is False
    assert battery.ideal_range == 185.92
    assert battery.level == 60
    assert battery.not_enough_power_to_heat == None
    assert battery.range == 185.92
    assert battery.soc == 60
    assert battery.usable_level == 60
