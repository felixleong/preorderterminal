import os.path
from preorder.config.parser import ConfigParser
from preorder.config.schema import CONFIG_SCHEMA


__DEFAULT_CONFIG_PATH = [
    os.path.expandvars('$HOME/.config/preorderterminal.ini'),
    './.config.ini',
]


# Upon loading/import, we would load up the configuration
__parser = ConfigParser()
__parser.read(__DEFAULT_CONFIG_PATH)
__config = CONFIG_SCHEMA(__parser.as_dict())

# Load up the config
EMAIL = __config.get('email', None)
