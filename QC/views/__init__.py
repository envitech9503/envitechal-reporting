"""QC.views - split from monolithic QC/views.py (13,268 lines) on 18-07-2026.

QC/urls.py keeps using `from . import views` unchanged: this package
exposes every former top-level name. shared.py holds the imports and
module globals; dw / ww / core modules star-import shared, and the
linker below restores the flat monolith namespace for cross-module
calls at runtime.
"""
from .shared import *  # noqa: F401,F403
from .dw import *  # noqa: F401,F403
from .ww import *  # noqa: F401,F403
from .core import *  # noqa: F401,F403
from .reagent_prep import *  # noqa: F401,F403

_FAMILY_MODULES = ['dw', 'ww', 'core', 'reagent_prep']


def _link():
    # Inject the full package namespace into every family module so that
    # cross-family calls resolve exactly as they did in the single-file
    # monolith.  setdefault: a module's own definitions always win.
    import sys
    pkg = sys.modules[__name__]
    ns = {k: v for k, v in vars(pkg).items()
          if not (k.startswith('__') or k == '_FAMILY_MODULES')}
    for name in _FAMILY_MODULES:
        mod = sys.modules[__name__ + '.' + name]
        for k, v in ns.items():
            mod.__dict__.setdefault(k, v)


_link()
del _link
