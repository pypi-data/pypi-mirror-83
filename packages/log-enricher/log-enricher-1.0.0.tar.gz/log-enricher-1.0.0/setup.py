# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['log_enricher']

package_data = \
{'': ['*']}

install_requires = \
['python-json-logger>=0.1.11,<0.2.0', 'strenum>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'log-enricher',
    'version': '1.0.0',
    'description': 'Library to enrich structured logs',
    'long_description': 'log-enricher\n============\n[![CircleCI](https://circleci.com/gh/arni-inaba/log-enricher.svg?style=svg)](https://circleci.com/gh/arni-inaba/log-enricher)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/log-enricher.svg)](https://pypi.org/project/log-enricher/)\n[![PyPI Version](https://img.shields.io/pypi/v/log-enricher.svg)](https://pypi.org/project/log-enricher/)\n[![License](https://img.shields.io/badge/license-mit-blue.svg)](https://pypi.org/project/log-enricher/)\n\nThis is a log enricher, useful for adding custom fields to log records.\n\nThis was developed at [GRID](https://github.com/GRID-is) for use with our\npython backend services and intended to emit structured logs.\n\ninstallation\n------------\n```\npip install log-enricher\n```\n\nconfiguration\n-------------\n\n`log-enricher.initialize_logging(...)` configures the `logging` library and takes in `enrichers`, a list of \nfunctions that return a dictionary. When a log message is sent, the enrichers are run automatically and their \noutput is added to the log message, if structured logging is enabled.\n\nFurthermore, `initialize_logging()` takes a list of `loggers` to use, a switch to control `structured_logs` \n(JSON logs, default on), and a `log_level` setting.\n\nLogs will be output in a structured JSON format by default - if `structured_logs` is `True` - \nor in a plain, console-friendly format if `structured_logs` is `False`.\n\nconfig example\n--------------\n```python\nimport os\n\nfrom log_enricher import initialize_logging, Level\nfrom log_enricher.enrichers import Enricher\n\nclass UserContextEnricher(Enricher):\n    def __call__(self) -> Dict[str, Any]:\n        user_context = get_user_context()\n        return {"username": user_context.get("username")}\n\nextra_log_properties = {\n    "app_version": Config.APP_VERSION, "release_stage": Config.RELEASE_STAGE\n}\n\ndef main():\n    initialize_logging(\n        loggers=["uvicorn", "sqlalchemy"],\n        structured_logs=os.environ.get("STRUCTURED_LOGS", True),\n        log_level=Level.INFO,\n        enrichers=[UserContextEnricher(), lambda: extra_log_properties],\n    )\n```\n\nenrichers\n---------\nTo build a log enricher, make a subclass of Enricher, or Callable, and implement `__call__()`. Any method returning \na dict can be used to enrich log records. See [log_enricher/enrichers.py](log_enricher/enrichers.py). The key-value\npairs in the dict are added as attribute-value pairs to the log record. Of course, any method calls in the \nenrichers need to  work in any subsequent context the logging system is called.\n',
    'author': 'Arni Inaba Kjartansson',
    'author_email': 'arni@grid.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arni-inaba/log-enricher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
