from typing import Any, Callable

import yaml

from ..getcurdir import getcurdir


yaml_path = getcurdir(__file__) + "/strings.yaml"

with open(yaml_path) as file:
    _dict: dict[str, str] = yaml.safe_load(file)

for key, val in _dict.items():
    _dict[key] = val.strip()

def get(func: Callable[..., str], **kwargs: Any) -> str:
    key = func.__name__.replace("_", "-")
    return _dict[key].format_map(kwargs)
