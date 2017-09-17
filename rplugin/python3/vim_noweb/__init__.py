import os
import sys
import logging.config

from .plugin import *

# log_filename = os.path.join(os.path.dirname(
#     sys.modules[__name__].__file__), 'nvim_noweb.log')

log_filename = 'nvim_noweb.log'

logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'local': {
            'format': '%(asctime)s %(message)s',
        }
    },
    'handlers': {
        'file': {'class': 'logging.FileHandler',
                 'formatter': 'local',
                 'level': 'DEBUG',
                 'filename': log_filename
                 }
    },
    'loggers': {'': {'handlers': ['file'],
                     'level': 'DEBUG'}},
}

logging.config.dictConfig(logger_config)
