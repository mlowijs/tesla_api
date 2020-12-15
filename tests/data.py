import copy

__all__ = ("FULL_DATA", "GUI_SETTINGS", "VEHICLE_STATE", "DRIVE_STATE", "CHARGE_STATE", "ATTRS", "KEYS", "CLIMATE_STATE")

KEYS = [
    "charge_state",
    "climate_state",
    "drive_state",
    "gui_settings",
    "vehicle_config",
    "vehicle_state",
]

FULL_DATA = {
    "access_type": "OWNER",
    "api_version": 12,
    "backseat_token": None,
    "backseat_token_updated_at": None,
    "calendar_enabled": True,
    "charge_state": {
        "battery_heater_on": False,
        "battery_level": 60,
        "battery_range": 185.92,
        "charge_current_request": 16,
        "charge_current_request_max": 16,
        "charge_enable_request": True,
        "charge_energy_added": 22.66,
        "charge_limit_soc": 69,
        "charge_limit_soc_max": 100,
        "charge_limit_soc_min": 50,
        "charge_limit_soc_std": 90,
        "charge_miles_added_ideal": 92.5,
        "charge_miles_added_rated": 92.5,
        "charge_port_cold_weather_mode": False,
        "charge_port_door_open": False,
        "charge_port_latch": "Engaged",
        "charge_rate": 0.0,
        "charge_to_max_range": False,
        "charger_actual_current": 0,
        "charger_phases": None,
        "charger_pilot_current": 16,
        "charger_power": 0,
        "charger_voltage": 2,
        "charging_state": "Disconnected",
        "conn_charge_cable": "<invalid>",
        "est_battery_range": 140.2,
        "fast_charger_brand": "<invalid>",
        "fast_charger_present": False,
        "fast_charger_type": "<invalid>",
        "ideal_battery_range": 185.92,
        "managed_charging_active": False,
        "managed_charging_start_time": None,
        "managed_charging_user_canceled": False,
        "max_range_charge_counter": 0,
        "minutes_to_full_charge": 0,
        "not_enough_power_to_heat": None,
        "scheduled_charging_pending": False,
        "scheduled_charging_start_time": None,
        "time_to_full_charge": 0.0,
        "timestamp": 1605725427656,
        "trip_charging": False,
        "usable_battery_level": 60,
        "user_charge_enable_request": None,
    },
    "climate_state": {
        "battery_heater": False,
        "battery_heater_no_power": None,
        "climate_keeper_mode": "off",
        "defrost_mode": 0,
        "driver_temp_setting": 20.5,
        "fan_status": 0,
        "inside_temp": 13.0,
        "is_auto_conditioning_on": False,
        "is_climate_on": False,
        "is_front_defroster_on": False,
        "is_preconditioning": False,
        "is_rear_defroster_on": False,
        "left_temp_direction": 0,
        "max_avail_temp": 28.0,
        "min_avail_temp": 15.0,
        "outside_temp": 12.0,
        "passenger_temp_setting": 20.5,
        "remote_heater_control_enabled": False,
        "right_temp_direction": 0,
        "seat_heater_left": 0,
        "seat_heater_rear_center": 0,
        "seat_heater_rear_left": 0,
        "seat_heater_rear_right": 0,
        "seat_heater_right": 0,
        "side_mirror_heaters": False,
        "timestamp": 1605725427656,
        "wiper_blade_heater": False,
    },
    "color": None,
    "display_name": "888888",
    "drive_state": {
        "gps_as_of": 1605725335,
        "heading": 358,
        "latitude": 59.917045,
        "longitude": 7.981791,
        "native_latitude": 59.917045,
        "native_location_supported": 1,
        "native_longitude": 7.981791,
        "native_type": "wgs",
        "power": 0,
        "shift_state": None,
        "speed": None,
        "timestamp": 1605725427656,
    },
    "gui_settings": {
        "gui_24_hour_time": True,
        "gui_charge_rate_units": "kW",
        "gui_distance_units": "km/hr",
        "gui_range_display": "Rated",
        "gui_temperature_units": "C",
        "show_range_units": False,
        "timestamp": 1605725427656,
    },
    "id": 999999999999,
    "id_s": "999999999999",
    "in_service": False,
    "option_codes": "AD15,MDL3,PBSB,RENA,BT37,ID3W,RF3G,S3PB,DRLH,DV2W,W39B,APF0,COUS,BC3B,CH07,PC30,FC3P,FG31,GLFR,HL31,HM31,IL31,LTPB,MR31,FM3B,RS3H,SA3P,STCP,SC04,SU3C,T3CA,TW00,TM00,UT3P,WR00,AU3P,APH3,AF00,ZCST,MI00,CDM0",
    "state": "online",
    "tokens": ["dae9f13e1889e1e1", "1ad6b8d43a795273"],
    "user_id": 7777777,
    "vehicle_config": {
        "can_accept_navigation_requests": True,
        "can_actuate_trunks": True,
        "car_special_type": "base",
        "car_type": "model3",
        "charge_port_type": "CCS",
        "default_charge_to_max": False,
        "ece_restrictions": True,
        "eu_vehicle": True,
        "exterior_color": "SolidBlack",
        "exterior_trim": "Chrome",
        "has_air_suspension": False,
        "has_ludicrous_mode": False,
        "key_version": 2,
        "motorized_charge_port": True,
        "plg": False,
        "rear_seat_heaters": 1,
        "rear_seat_type": None,
        "rhd": False,
        "roof_color": "Glass",
        "seat_type": None,
        "spoiler_type": "None",
        "sun_roof_installed": None,
        "third_row_seats": "<invalid>",
        "timestamp": 1605725427656,
        "use_range_badging": True,
        "wheel_type": "Pinwheel18",
    },
    "vehicle_id": 9999999999,
    "vehicle_state": {
        "api_version": 12,
        "autopark_state_v2": "unavailable",
        "calendar_supported": True,
        "car_version": "2020.44.10.1 955dc1dd145e",
        "center_display_state": 0,
        "df": 0,
        "dr": 0,
        "fd_window": 0,
        "fp_window": 0,
        "ft": 0,
        "is_user_present": False,
        "locked": True,
        "media_state": {"remote_control_enabled": True},
        "notifications_supported": True,
        "odometer": 1648.193379,
        "parsed_calendar_supported": True,
        "pf": 0,
        "pr": 0,
        "rd_window": 0,
        "remote_start": False,
        "remote_start_enabled": True,
        "remote_start_supported": True,
        "rp_window": 0,
        "rt": 0,
        "sentry_mode": False,
        "sentry_mode_available": True,
        "software_update": {
            "download_perc": 100,
            "expected_duration_sec": 2700,
            "install_perc": 1,
            "status": "",
            "version": "2020.48.10",
        },
        "speed_limit_mode": {
            "active": False,
            "current_limit_mph": 85.0,
            "max_limit_mph": 90,
            "min_limit_mph": 50,
            "pin_code_set": False,
        },
        "timestamp": 1605725427656,
        "valet_mode": False,
        "valet_pin_needed": True,
        "vehicle_name": None,
    },
    "vin": "5YJ3E7EB4LF999999",
}


GUI_SETTINGS = FULL_DATA["gui_settings"]
VEHICLE_STATE = FULL_DATA["vehicle_state"]
DRIVE_STATE = FULL_DATA["drive_state"]
CHARGE_STATE = FULL_DATA["charge_state"]
CLIMATE_STATE = FULL_DATA["climate_state"]
ATTRS = copy.deepcopy(FULL_DATA)

for key in KEYS:
    ATTRS.pop(key, None)




if __name__ == "__main__":
    import asyncio
    import click
    from tesla_api import TeslaApiClient
    from tesla_api.misc import diff


    @click.command(help="Tool to check for diff in api response")
    @click.option("--username", help="Username to your tesla account")
    @click.option(
        "--password",
        prompt=False,
        hide_input=False,
        confirmation_prompt=False,
        help="Password to your tesla account",
    )
    @click.option(
        "--changes",
        default="all",
        type=click.Choice(["add", "remove", "change", "all"]),
        help="What changes do you want to be displayed",
    )
    @click.option(
        "--fixup",
        default=False,
        help="Add any removed or added to FULL_DATA",
        is_flag=True
    )
    def main(username, password, changes, fixup):
        async def something():
            client = TeslaApiClient(username, password)
            vehicles = await client.list_vehicles()
            v = vehicles[0]
            await v.wake_up()
            data = await v.full_update()

            diff(FULL_DATA, v._data, changes, fixup)

        asyncio.run(something())

    main()
