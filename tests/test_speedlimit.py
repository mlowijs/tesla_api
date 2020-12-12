

def test_speedlimit_attributes(vehicle):
    speedlimit = vehicle.controls.speedlimit
    assert speedlimit.current_limit == 52.81799540172746
    assert speedlimit.current_limit_mph == 85.0
    assert speedlimit.is_active is False
    assert speedlimit.max_limit_mph == 90
    assert speedlimit.pin_code_set is False


# Add test for methods.
