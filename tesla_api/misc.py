"""Misc helpers."""
from typing import Optional, Union


class Dict(dict): # type: ignore
    """Just a helper that includes a tip in KeyError excetion to the user."""
    def __init__(self, arg):
        super().__init__(arg)

    def __missing__(self, key):
        raise KeyError(f"{key} is missing. Try using vehicle.refresh()")


def mile_to_km(value: int) -> float:
    """Convert from mile to km"""
    return round(value * 1.609344, 2)


def km_to_mile(value: int) -> float:
    """Convert from km to mile"""
    return round(value * 0.621371192, 2)


def c_to_f(value):
    """Convert celsius to farenheit"""
    return value * 1.8 + 32


def cast(value: Optional[Union[str, int]]) -> bool:
    """Helper"""
    correct = [True, 1, "1", "true"]
    falsy = [False, "false", 0, "0", None, ""]

    if value in correct:
        return True
    elif value in falsy:
        return False

    raise ValueError("%s expects value that can be bool")
