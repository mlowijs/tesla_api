import pytest


def test_Vehicle_Gui_attributes(vehicle):
    media = vehicle.media
    assert media.center_display == "off"
    assert media.remote_control_enabled is True


@pytest.mark.asyncio
async def test_Vehicle_Media_toggle_media_playback(vehicle):
    media = vehicle.media
    assert await media.toggle_media_playback() is True


@pytest.mark.asyncio
async def test_Vehicle_Media_next_track(vehicle):
    media = vehicle.media
    assert await media.next_track() is True


@pytest.mark.asyncio
async def test_Vehicle_Media_prev_track(vehicle):
    media = vehicle.media
    assert await media.prev_track() is True


@pytest.mark.asyncio
async def test_Vehicle_Media_next_fav(vehicle):
    media = vehicle.media
    assert await media.next_fav() is True


@pytest.mark.asyncio
async def test_Vehicle_Media_prev_fav(vehicle):
    media = vehicle.media
    assert await media.prev_fav() is True


@pytest.mark.asyncio
async def test_Vehicle_Media_volume_up(vehicle):
    media = vehicle.media
    assert await media.volume_up() is True


@pytest.mark.asyncio
async def test_Vehicle_Media_volume_down(vehicle):
    media = vehicle.media
    assert await media.volume_down() is True
