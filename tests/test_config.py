

def test_config(vehicle):
    config = vehicle.config
    assert config.can_accept_navigation_requests is True
    assert config.can_actuate_trunks is True
    assert config.car_special_type == "base"
    assert config.car_type == "model3"
    assert config.charge_port_type == "CCS"
    assert config.default_charge_to_max is False
    assert config.ece_restrictions is True
    assert config.eu_vehicle is True
    assert config.exterior_color == "SolidBlack"
    assert config.exterior_trim == "Chrome"
    assert config.has_air_suspension is False
    assert config.has_ludicrous_mode is False
    assert config.key_version == 2
    assert str(config.last_update.date()) == "2020-11-18"
    assert config.motorized_charge_port is True
    assert config.plg is False
    assert config.rear_seat_heaters == 1
    assert config.rear_seat_type == None
    assert config.right_hand_drive is False
    assert config.roof_color == "Glass"
    assert config.seat_type == None
    assert config.spoiler_type == "None"
    assert config.sun_roof_installed == None
    assert config.third_row_seats == "<invalid>"
    assert config.use_range_badging is True
    assert config.wheel_type == "Pinwheel18"
