from app.core.config.schema import ApplicationSettings, DefaultSettings


def test_schema_can_be_created() -> None:
    # Just check that default settings are present
    settings = ApplicationSettings()
    assert not settings.default

    # And that default settings has default = True
    def_settings = DefaultSettings()
    assert def_settings.default
