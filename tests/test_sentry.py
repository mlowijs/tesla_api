import pytest


def test_sentry_attributes(vehicle):
    sentry = vehicle.controls.sentry

    assert sentry.is_active is False
    assert sentry.is_available is True


@pytest.mark.asyncio
async def test_Vehicle_Controls_Sentry_enable(vehicle):
    sentry = vehicle.controls.sentry
    assert await sentry.enable() is True


@pytest.mark.asyncio
async def test_Vehicle_Controls_Sentry_disable_(vehicle):
    sentry = vehicle.controls.sentry
    assert await sentry.disable() is True
