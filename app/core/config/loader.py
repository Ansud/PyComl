import random
import string
from pathlib import Path
from typing import ClassVar, Self

from pydantic import ValidationError
from PyQt6.QtCore import QStandardPaths

from app.core.constants import PYCOML_APP_NAME
from app.core.logging import logger

from .schema import ApplicationSettings


class Settings:
    NAME: ClassVar[str] = "app_config.json"
    # 1 Megabyte of config file is enough for everything
    MAX_SIZE: ClassVar[int] = 1 * 1024 * 1024

    file_name: Path
    data: ApplicationSettings

    def __init__(self):
        raise NotImplementedError("Please do not instanciate directly, use load() function.")

    def save(self) -> None:
        random_string = "".join(random.choices(string.ascii_lowercase, k=8))

        new_file = self.file_name.parent / (self.file_name.name + random_string)
        save_logger = logger.bind(file_name=str(new_file))

        save_logger.debug("Try to save config file")

        try:
            with new_file.open("w+") as f:
                f.write(self.data.model_dump_json(indent=4))
        except OSError as e:
            save_logger.warning("Failed to save config file", exception=repr(e))
            return

        save_logger.debug("Try to move config file to proper place", to=str(self.file_name))
        new_file.rename(self.file_name)

    @classmethod
    def generate_default(cls) -> ApplicationSettings:
        logger.debug("Generate default config")
        return ApplicationSettings()

    @classmethod
    def load(cls) -> Self:
        app_data = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.AppDataLocation)
        config_file_path = Path(app_data[0]) / PYCOML_APP_NAME
        config_file_path.mkdir(exist_ok=True)

        file_name = config_file_path / cls.NAME

        def try_load() -> ApplicationSettings | None:
            load_logger = logger.bind(file_name=str(file_name))

            if not file_name.exists():
                return None

            file_size = file_name.stat().st_size

            if file_size > cls.MAX_SIZE:
                load_logger.warning("Config file size is too large, reset it", size=file_size)
                return None

            try:
                with file_name.open("r+") as f:
                    raw_data = f.read()
            except OSError as e:
                load_logger.warning("Failed to open config file, reset it", exception=repr(e))
                return None

            try:
                return ApplicationSettings.model_validate_json(raw_data)
            except ValidationError as e:
                load_logger.warning("Config file malformed, reset it", exception=repr(e))
                return None

        app_data = try_load()

        obj = cls.__new__(cls)
        obj.file_name = file_name

        if app_data is not None:
            obj.data = app_data
            return obj

        obj.data = cls.generate_default()
        obj.save()
        return obj


# Simulate old behaviour
_settings = Settings.load()


class LeftFrameConfig:
    username = _settings.data.wiki.username
    source = _settings.data.wiki.source
    author = _settings.data.wiki.author
    categories = "|".join(_settings.data.wiki.categories)
    license = _settings.data.wiki.license
    language = _settings.data.wiki.language


class RightFrameConfig:
    default_image_sort = str(_settings.data.ui.default_image_sort)
