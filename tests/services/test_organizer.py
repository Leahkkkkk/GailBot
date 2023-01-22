# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-01-16 14:05:26
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-01-16 15:16:42

from gailbot.services.organizer import (
    OrganizerService,
    Source,
    Settings
)


########
SOURCES_WS = "./output/ws/organizer/sources"
SETTINGS_WS = "./output/ws/organizer/settings"


SETTINGS_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/GailBot/gailbot/configs/settings/default.toml"
AUDIO_PATH = "./data/dev_test_data/media/audio/wav/SineWaveMinus16.wav"
########


def test_source():
    source_name = "audio"
    organizer = OrganizerService(SOURCES_WS, SETTINGS_WS)
    assert organizer.add_source(source_name, AUDIO_PATH)
    print(organizer.source_names())
    print(organizer.is_source(source_name))
    print(organizer.is_source_configured(source_name))
    print(organizer.get_source_details(source_name))
    source = organizer.get_source(source_name)
    assert type(source) == Source
    print(source.workspace)


def test_settings():
    organizer = OrganizerService(SOURCES_WS, SETTINGS_WS)
    profile_name = "default"
    assert organizer.create_new_settings_profile(
        profile_name, SETTINGS_PATH
    )
    print(organizer.get_profile_names())
    LOCAL_SAVE_PATH = "output/test_settings"
    organizer.save_settings_profile(profile_name, LOCAL_SAVE_PATH)
    organizer.remove_settings_profile(profile_name)
    print(organizer.get_profile_names())
    organizer.load_settings_profile(f"{LOCAL_SAVE_PATH}/{profile_name}.toml")
    print(organizer.get_profile_names())
    new_name = "test"
    organizer.change_profile_name(profile_name, new_name)
    assert organizer.is_settings_profile(new_name)
    assert not organizer.is_settings_profile(profile_name)

    print(organizer.get_settings_profile_details(new_name))

    source_name = "audio"
    assert organizer.add_source(source_name, AUDIO_PATH)
    assert organizer.apply_settings_profile_to_source(
        source_name, new_name
    )

    print(organizer.get_source_settings_profile(source_name).to_dict())

    organizer.change_profile_name(new_name, profile_name)

    print(organizer.get_sources_using_settings_profile(new_name))
    print(organizer.get_sources_using_settings_profile(profile_name))

    assert organizer.is_settings_profile(profile_name)
    assert not organizer.is_settings_profile(new_name)