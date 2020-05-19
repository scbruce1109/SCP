from .base import *

try:
    from .local_aws_settings import *
except:
    from .production_settings import *
