"""EnviTechAlApp.views — split from monolithic views.py (36k lines) on 18-07-2026.

urls.py keeps using `from EnviTechAlApp import views` unchanged: this package
exposes every former top-level name.  shared.py holds imports and
module globals (signs / active_users — see 14-07 NameError incident);
each family module star-imports shared, and the linker below restores the
monolith's flat namespace for cross-family calls.
"""
from .shared import *  # noqa: F401,F403
from .logviews import *  # noqa: F401,F403
from .job import *  # noqa: F401,F403
from .drinking import *  # noqa: F401,F403
from .gaseous import *  # noqa: F401,F403
from .verif import *  # noqa: F401,F403
from .packing import *  # noqa: F401,F403
from .viscous import *  # noqa: F401,F403
from .microbial import *  # noqa: F401,F403
from .vehicular import *  # noqa: F401,F403
from .inspection import *  # noqa: F401,F403
from .machine import *  # noqa: F401,F403
from .lux import *  # noqa: F401,F403
from .calib import *  # noqa: F401,F403
from .generate import *  # noqa: F401,F403
from .sample import *  # noqa: F401,F403
from .noise import *  # noqa: F401,F403
from .ambient import *  # noqa: F401,F403
from .waste import *  # noqa: F401,F403
from .misc import *  # noqa: F401,F403

_FAMILY_MODULES = ['logviews', 'job', 'drinking', 'gaseous', 'verif', 'packing', 'viscous', 'microbial', 'vehicular', 'inspection', 'machine', 'lux', 'calib', 'generate', 'sample', 'noise', 'ambient', 'waste', 'misc']


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
