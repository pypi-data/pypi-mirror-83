from .models import *
from .api import *
from .utils import *
from .client import Client


def init(lib):
    import multio
    multio.init(lib)
