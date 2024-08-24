import logging
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class FileSort(str, Enum):
    file_name = "file_name"
    exif_date = "file_date"


class BaseSettings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, use_enum_values=True)


class OpenAISettings(BaseSettings):
    key: str = Field(default="")


class MLSettings(BaseSettings):
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    keywords: bool = Field(default=False)


class WikiSettings(BaseSettings):
    username: str = Field(default="Your Wiki Login")
    source: str = Field(default="{{own}}")
    author: str = Field(default="Author")
    categories: list[str] = Field(default_factory=list)
    license: str = Field(default="{{self|cc-by-sa-4.0}}")
    language: str = Field(default="en")


class UISettings(BaseSettings):
    default_image_sort: FileSort = Field(default=FileSort.file_name)
    update_exif: bool = Field(default=False)
    log_level: int = Field(default=logging.WARNING)


class ApplicationSettings(BaseSettings):
    wiki: WikiSettings = Field(default_factory=WikiSettings)
    ui: UISettings = Field(default_factory=UISettings)
