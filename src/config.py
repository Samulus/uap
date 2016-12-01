from configparser import ConfigParser
from os.path import realpath, join, exists

CONFIG_PATH = realpath(join(__file__, "..", "config.ini"))

DEFAULT_CONFIG = {
    'host': '127.0.0.1',
    'port': 8080,
    'music_folder': None,
    'login_required': True,
    'signup_allowed': True,
    'debug': False,
    'reloader': False,
}

EXAMPLE_INI = """
[settings]
# ip address and port to listen on
host = 127.0.0.1
port = 8080

# put the absolute path to your music folder
# here, i.e. C:\\Users\Sam\music or
# /home/sam/music
music_folder =

# require the user to authenticate before they can
# login to the server
login_required = True

# disable the ability for new people to register (only
# existing users can connect)
signup_allowed = True

# leave this as false unless you're a uap dev :-)
#debug = False
#reloader = False
"""


def load_settings_dict():
    """
    Loads a settings ini file from CONFIG_PATH if the file
    is not found a new one will be generated.

    :throws: SyntaxError exceptions on malformed ini files.
    :returns: A dictionary containing the application settings.
              'None' after generating an example ini file.
    """

    # generate a config.ini if it's missing
    if not exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf8") as config:
            config.write(EXAMPLE_INI)
            return None

    settings = {}
    config = ConfigParser()
    config.read(CONFIG_PATH)

    # can't find [settings] at top of ini -> throw exception
    if 'settings' not in config:
        raise SyntaxError("Missing [settings] at top of config.ini")

    # string values
    for key in ("host", "music_folder"):
        settings[key] = config.get("settings", key) \
            if key in config['settings'] else DEFAULT_CONFIG[key]

    # integer values
    key = 'port'
    settings[key] = config.getint("settings", key) \
        if key in config['settings'] else DEFAULT_CONFIG[key]

    # boolean values
    for key in ("debug", "reloader", "login_required", "signup_allowed"):
        settings[key] = config.getboolean('settings', key) \
            if key in config['settings'] else DEFAULT_CONFIG[key]

    return settings
