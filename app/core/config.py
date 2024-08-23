from pathlib import Path

import yaml


def load_config_as_dict(config_filename):
    current_path = Path(__file__).absolute().parent

    # Config is in upper/upper directory (move to any home plz)
    config_path = current_path.parent.parent / config_filename

    with config_path.open("r") as f:
        config = yaml.safe_load(f)

    return config


class LeftFrameConfig:
    _config = load_config_as_dict("config/general.yaml")["left_frame"]

    username = _config["username"]
    source = _config["source"]
    author = _config["author"]
    categories = _config["categories"]
    license = _config["license"]
    language = _config["language"]


class RightFrameConfig:
    _config = load_config_as_dict("config/general.yaml")["right_frame"]
    default_image_sort = _config["default_image_sort"]
