import pytest
from tesla_api.misc import c_to_f, cast, km_to_mile, mile_to_km


def test_km_to_mile():
    assert km_to_mile(1) == 0.62


def test_mile_to_km():
    assert mile_to_km(100) == 160.93


def test_c_to_f():
    assert c_to_f(40) == 104


def test_cast():
    assert cast(1) is True
    assert cast("1") is True
    assert cast(None) is False
    assert cast("") is False
    with pytest.raises(ValueError):
        assert cast(2)
        assert cast("kek")
