default_config = {
  'version': 1,
  'formatters': {
    'brief': {
      'format': '%(message)s'
    },
    'json': {
      'format': '%(timestamp)s %(service)s %(loglevel)s %(message)s',
      'class': 'jsonlogger.logger.CustomJsonFormatter'
    }
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'formatter': 'json',
      'stream': 'ext://sys.stdout'
    },
    'file': {
      'class': 'logging.handlers.RotatingFileHandler',
      'formatter': 'json',
      'filename': '/var/log/osm-seed/logfile.log',
      'maxBytes': 5242880,
      'backupCount': 10
    }
  },
  'loggers': {
    'main-debug': {
      'handlers': [
        'console',
        'file'
      ],
      'level': 'DEBUG'
    },
    'main-info': {
      'handlers': [
        'console',
        'file'
      ],
      'level': 'INFO'
    },
    'main-warning': {
      'handlers': [
        'console',
        'file'
      ],
      'level': 'WARNING'
    },
    'main-error': {
      'handlers': [
        'console',
        'file'
      ],
      'level': 'ERROR'
    },
    'main-critical': {
      'handlers': [
        'console',
        'file'
      ],
      'level': 'CRITICAL'
    }
  }
}
