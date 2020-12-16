"""
A collection of objects used for typing across the library.

Mostly this is TypedDict instances used to represent API responses.
"""

from typing import List, Literal, Optional, TypedDict, Union

# asleep seems to only happen when in service.
VehicleState = Literal["asleep", "offline", "online", "shutdown"]


class _BaseResponseBase(TypedDict):
    response: object


class BaseResponse(_BaseResponseBase, total=False):
    count: int


class CommandResponse(TypedDict):
    reason: str
    result: bool


class ErrorResponse(TypedDict):
    response: None
    error: str
    error_description: Literal[""]


class ChargeStateResponse(TypedDict):  # TODO
    battery_heater_on: bool
    battery_level: int  # Percent
    battery_range: float  # TODO: Range in miles?
    charge_current_request: int
    charge_current_request_max: int
    charge_enable_request: bool
    charge_energy_added: float
    charge_limit_soc: int
    charge_limit_soc_max: int
    charge_limit_soc_min: int
    charge_limit_soc_std: int
    charge_miles_added_ideal: float
    charge_miles_added_rated: float
    charge_port_cold_weather_mode: Optional[bool]
    charge_port_door_open: bool
    charge_port_latch: Literal["Blocking"]
    charge_rate: float
    charge_to_max_range: bool
    charger_actual_current: int
    charger_phases: None
    charger_pilot_current: int
    charger_power: int
    charger_voltage: int
    charging_state: Literal["Disconnected"]
    conn_charge_cable: Literal["<invalid>"]
    est_battery_range: float
    fast_charger_brand: Literal["<invalid>"]
    fast_charger_present: bool
    fast_charger_type: Literal["<invalid>"]
    ideal_battery_range: float
    managed_charging_active: bool
    managed_charging_start_time: None
    managed_charging_user_canceled: bool
    max_range_charge_counter: int
    minutes_to_full_charge: int  # TODO
    not_enough_power_to_heat: bool
    scheduled_charging_pending: bool
    scheduled_charging_start_time: None
    time_to_full_charge: float  # TODO
    timestamp: int
    trip_charging: bool
    usable_battery_level: int
    user_charge_enable_request: None


class ClimateStateResponse(TypedDict):  # TODO
    # The Optional attributes here are all None if the car is not awake.
    battery_heater: bool
    battery_heater_no_power: bool
    climate_keeper_mode: Literal["camp", "dog", "off"]
    defrost_mode: int
    driver_temp_setting: float
    fan_status: int
    inside_temp: Optional[float]
    is_auto_conditioning_on: Optional[bool]
    is_climate_on: bool
    is_front_defroster_on: bool
    is_preconditioning: bool
    is_rear_defroster_on: bool
    left_temp_direction: Optional[int]
    max_avail_temp: float
    min_avail_temp: float
    outside_temp: Optional[float]
    passenger_temp_setting: float
    remote_heater_control_enabled: bool
    right_temp_direction: Optional[int]
    seat_heater_left: int
    seat_heater_rear_center: int
    seat_heater_rear_left: int
    seat_heater_rear_right: int
    seat_heater_right: int
    side_mirror_heaters: bool
    steering_wheel_heater: bool
    timestamp: int
    wiper_blade_heater: bool


class DriveStateResponse(TypedDict):
    # This differs from timestamp when the GNSS system has not got a signal yet.
    gps_as_of: int  # Seconds
    heading: int  # TODO
    latitude: float
    longitude: float
    native_latitude: float
    native_location_supported: int
    native_longitude: float
    native_type: Literal["wgs"]
    power: int  # TODO: KW?
    shift_state: Literal[None, "D", "P", "R"]  # TODO
    speed: Optional[int]  # TODO: mph?
    timestamp: int  # Milliseconds


class GUISettingsResponse(TypedDict):
    gui_24_hour_time: bool
    gui_charge_rate_units: Literal["kW"]  # TODO
    gui_distance_units: Literal["mi/hr", "km/hr"]
    gui_range_display: Literal["Rated"]  # TODO: 'Percent'?
    gui_temperature_units: Literal["C", "F"]  # TODO
    show_range_units: bool  # TODO
    timestamp: int  # Milliseconds


class TokenResponse(TypedDict):
    access_token: str
    token_type: Literal["bearer"]
    expires_in: int  # Seconds
    refresh_token: str
    created_at: int  # Timestamp (seconds)


class _TokenParamsPassword(TypedDict):
    grant_type: Literal["password"]
    client_id: str
    client_secret: str
    email: str
    password: str


class _TokenParamsRefresh(TypedDict):
    grant_type: Literal["refresh_token"]
    client_id: str
    client_secret: str
    refresh_token: str


TokenParams = Union[_TokenParamsPassword, _TokenParamsRefresh]


class VehicleConfigResponse(TypedDict):
    can_accept_navigation_requests: bool
    can_actuate_trunks: bool
    car_special_type: Literal["base"]
    car_type: Literal["models2"]
    charge_port_type: Literal["EU", "US"]
    ece_restrictions: bool  # UNECE regulations (e.g. limit turning of steering wheel).
    eu_vehicle: bool
    exterior_color: Literal["Black"]
    has_air_suspension: bool
    has_ludicrous_mode: bool
    motorized_charge_port: bool
    plg: bool  # ??
    rear_seat_heaters: int  # TODO
    rear_seat_type: int  # 0
    rhd: bool  # Right-hand drive
    roof_color: Literal["Glass"]
    seat_type: int  # 2 = 2020 seats
    spoiler_type: Literal["None"]
    sun_roof_installed: Literal[0]  # 0 = Not installed
    third_row_seats: Literal["None"]
    timestamp: int  # Milliseconds
    use_range_badging: bool  # ??
    wheel_type: Literal["Slipstream19Carbon"]


class _VehicleStateMedia(TypedDict):
    remote_control_enabled: bool


class _VehicleStateSoftwareUpdate(TypedDict):
    download_perc: int
    expected_duration_sec: int
    install_perc: int
    # '' = No firmware updates available (if duration is not 0,
    # then other updates are available, such as a games update).
    # available = Downloaded, ready to install.
    # downloading_wifi_wait = Waiting for WiFi connection to resume download.
    status: Literal["", "available", "downloading", "downloading_wifi_wait", "scheduled"]
    # Empty string if no version available or not a firmware update.
    version: str


class _VehicleStateSpeedLimit(TypedDict):
    active: bool
    current_limit_mph: float
    max_limit_mph: int
    min_limit_mph: int
    pin_code_set: bool


class _VehicleStateResponseBase(TypedDict):
    api_version: int
    autopark_state_v2: Literal["standby", "ready", "unavailable"]
    calendar_supported: bool
    car_version: str  # Software version
    # 0 = off, 2,3,4 = ??
    center_display_state: int
    df: int  # ??
    dr: int  # ??
    ft: int  # ??
    is_user_present: bool
    locked: bool
    media_state: _VehicleStateMedia
    notifications_supported: bool
    odometer: float  # TODO: Miles
    parsed_calendar_supported: bool
    pf: int  # ??
    pr: int  # ??
    remote_start: bool  # Currently activated
    remote_start_enabled: bool  # Available to activate via the API
    remote_start_supported: bool
    rt: int  # ??
    sentry_mode: bool
    sentry_mode_available: bool  # This will be False when driving etc.
    software_update: _VehicleStateSoftwareUpdate
    speed_limit_mode: _VehicleStateSpeedLimit
    timestamp: int  # milliseconds
    valet_mode: bool
    valet_pin_needed: bool
    vehicle_name: Optional[str]


class VehicleStateResponse(_VehicleStateResponseBase, total=False):
    autopark_style: Literal["dead_man"]
    homelink_device_count: int
    homelink_nearby: bool
    last_autopark_error: Literal["no_error"]
    smart_summon_available: bool
    summon_standby_mode_enabled: bool


class _VehiclesIdResponseBase(TypedDict):
    id: int
    vehicle_id: int
    vin: str
    display_name: str  # ??
    # No longer correct. https://tesla-api.timdorr.com/vehicle/optioncodes
    option_codes: str
    color: None  # ??
    # Seems to hold 2 tokens, with a new one pushing out the older one every few minutes.
    tokens: List[str]  # ??
    state: VehicleState
    in_service: bool
    id_s: str  # String version of id.
    calendar_enabled: bool
    access_type: Literal["OWNER"]
    api_version: int
    backseat_token: None  # ??
    backseat_token_updated_at: None  # ??


class VehiclesIdResponse(_VehiclesIdResponseBase, total=False):
    user_id: int


class VehicleDataResponse(VehiclesIdResponse):
    drive_state: DriveStateResponse
    climate_state: ClimateStateResponse
    charge_state: ChargeStateResponse
    gui_settings: GUISettingsResponse
    vehicle_state: VehicleStateResponse
    vehicle_config: VehicleConfigResponse


VehiclesResponse = List[VehiclesIdResponse]


# Energy sites

class EnergySite(TypedDict):
    energy_site_id: int
    resource_type: Literal["solar"]
    site_name: str
    id: int
    solar_power: int
    sync_grid_alert_enabled: bool
    breaker_alert_enabled: bool


class _EnergySiteInfoUserSettings(TypedDict):
    storm_mode_enabled: None
    sync_grid_alert_enabled: bool
    breaker_alert_enabled: bool


class _EnergySiteInfoComponents(TypedDict):
    solar: bool
    battery: bool
    grid: bool
    backup: bool
    gateway: str
    load_meter: bool
    tou_capable: bool
    storm_mode_capable: bool
    flex_energy_request_capable: bool
    car_charging_data_supported: bool
    configurable: bool
    grid_services_enabled: bool


class EnergySiteInfoResponse(TypedDict):
    id: str
    site_name: str
    installation_date: str
    user_settings: _EnergySiteInfoUserSettings
    components: _EnergySiteInfoComponents
    backup_reserve_percent: int  # TODO
    default_real_mode: str
    version: str
    battery_count: int
    time_zone_offset: int


class EnergySiteLiveStatusResponse(TypedDict):
    solar_power: int
    grid_status: str
    grid_services_active: bool
    percentage_charged: int
    energy_left: float
    total_pack_energy: int
    timestamp: str


ProductsResponse = List[Union[VehiclesIdResponse, EnergySite]]
