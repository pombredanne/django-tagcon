import sys
if sys.version_info[0] == 3:
    raise SystemExit("Django-Tagcon does not yet support Python 3")
if sys.version_info[0] != 2 or sys.version_info[1] < 5:
    raise SystemExit("Django-Tagcon requires Python 2.5 or greater")
del sys

# Python 2.5 doesn't support ``from .base import *``, so we do the same thing
# in a roundabout manner.
from .base import __all__ as _all
globals().update(dict((x, getattr(base, x)) for x in _all))
del _all
