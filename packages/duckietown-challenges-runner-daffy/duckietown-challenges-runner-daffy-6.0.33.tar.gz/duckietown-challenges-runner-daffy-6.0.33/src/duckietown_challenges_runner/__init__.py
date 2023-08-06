# coding=utf-8
__version__ = "6.0.33"

import sys

from zuper_commons.logs import ZLogger

logger = ZLogger(__name__)

enc = sys.getdefaultencoding()

logger.info(f"{__version__}")
from .runner import dt_challenges_evaluator

from .runner_local import runner_local_main
