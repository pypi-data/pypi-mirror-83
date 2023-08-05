__version__ = "0.0.6"

from fastcore.imports import IN_IPYTHON
from .imports import *

if IN_IPYTHON:
    from .showdoc import show_doc
    
from .core import *
from .tab_ae import *