from .message import handlers as _message
from .inline import handlers as _inline


handlers = _message + _inline
