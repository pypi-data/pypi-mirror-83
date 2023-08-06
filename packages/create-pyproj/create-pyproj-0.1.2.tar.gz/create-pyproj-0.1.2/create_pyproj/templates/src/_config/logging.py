import logging.config
from pathlib import Path

import yaml

DIR = Path(__file__).parent.absolute()
LOGPATH = DIR.parent.parent / 'logs'


def configureLogging():
    """."""
    Path(LOGPATH).mkdir(exist_ok=True)
    mainfilename = LOGPATH / 'main.log'
    debugfilename = LOGPATH / 'debug.log'

    with open(DIR / 'logging.yaml', 'r') as f:
        log_cfg = yaml.full_load(f)

    log_cfg['handlers']['file_handler']['filename'] = mainfilename
    log_cfg['handlers']['rotating_handler']['filename'] = debugfilename

    logging.config.dictConfig(log_cfg)

    # Set ERROR level logging on verbose modules
    modules = ['botocore', 'urllib3', 'googleapiclient']
    for module in modules:
        logging.getLogger(module).setLevel(logging.ERROR)

