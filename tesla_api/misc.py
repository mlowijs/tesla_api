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


def diff(old: dict, new: dict, changes: str, fixup: bool) -> dict:
    """Helper to identify changes in json reponse. Print out a FULL_DATA dict that can be copy pasted in

    Args:
        old (dict): The dict we will compare against
        new (dict):
        changes (str): What changes you want displayed/Fixed
                       Possible options: all, add, remove, change
        fixup (bool): Print out a new dict that can be used to copy pasta over.


    Example:
        diff(FULL_DATA, Vehicle._data, "all", True)

    Returns:
        dict: copy past this in and run black.

    """
    from copy import deepcopy
    import json
    import click
    import dictdiffer
    import pprint

    patches = []
    add_remove = ["add", "remove"]

    colors = {"change": "yellow", "add": "green", "remove": "red"}
    click.echo("Checking for changes in the json response.")

    for change, key, value in list(dictdiffer.diff(old, new)):
        if changes == "all" or change == changes:
            if change in add_remove:
                v = "%s %s" % value[0]
            else:
                v = "old %s new %s" % value

            click.secho(
                "%s %s %s" % (change, key, v),
                fg=colors[change],
            )

            if fixup is True:
                if change in add_remove:
                    patches.append([change, key, value])

    if fixup is True and len(patches):
        click.echo("Updated full data:\n")
        result = dictdiffer.patch(patches, old)
        p = pprint.pprint(result, indent=4)
        print("FULL_DATA = %s" % p)
        return result
