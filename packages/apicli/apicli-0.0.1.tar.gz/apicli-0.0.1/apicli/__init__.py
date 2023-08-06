from apicli.model import Model
from apicli.namespace import Namespace
from apicli.fields import *
from apicli.api import API

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s\t%(name)-25s %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger('apicli')
