import copy
from typing import Any


class FullDict(dict):
    """ Dictionary without None values. """

    def __init__(self, data: dict = None, /, **kwargs: Any):
        _data = copy.deepcopy(data or {})
        _data.update(kwargs)
        super().__init__({k: v for k, v in _data.items() if v is not None})

    def __setitem__(self, key: Any, value: Any):
        if value is not None:
            super().__setitem__(key, value)
