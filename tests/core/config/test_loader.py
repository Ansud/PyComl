from app.core.config.loader import Settings


def test_no_settings() -> None:
    settings = Settings.load()
    assert settings.data.default


def test_settings_exists() -> None:
    # Create settings in temp dir
    Settings.load()
    # And load them
    settings = Settings.load()
    assert not settings.data.default


def test_settings_wrong_format() -> None:
    # Create settings in temp dir
    initial = Settings.load()

    # Break them
    with initial.file_name.open("w+") as f:
        f.write("It is not JSON.")

    # And load back, should be default settings
    settings = Settings.load()
    assert settings.data.default


def test_settings_wrong_format_in_json() -> None:
    # Create settings in temp dir
    initial = Settings.load()

    # Break them, bit they will load properly, because we have defaults in fields
    with initial.file_name.open("w+") as f:
        f.write("{}")

    settings = Settings.load()
    assert not settings.data.default
