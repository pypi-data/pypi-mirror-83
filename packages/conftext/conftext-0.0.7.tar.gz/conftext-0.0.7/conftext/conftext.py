import os
import sys
import pkg_resources
from configparser import ConfigParser

CONFTEXT_FILENAME = '.conftext.ini'
CONFTEXT_SECTION = 'conftext'


def user_home():
    return os.path.expanduser('~')


def default_config_path():
    return os.path.join(user_home(), '.config', CONFTEXT_FILENAME[1:])


stop_paths = [os.path.sep, os.path.dirname(user_home())]


def find_file():
    """
    Find config files
    
    Will first look for `.conftext.ini` in the current working dir and then subsequently upwards the
    users home directory, or if home is not found, upwards to top-level dir `/`.
    
    Then it will look for `~/.config/conftext.ini`
    
    Returns `False` if no files found.
    """
    current_path = os.getcwd()
    
    # Check from current dir upwards `stop_paths` dir for `.conftext.ini`
    while current_path not in stop_paths:
        candidate_path = os.path.join(current_path, CONFTEXT_FILENAME)
        if os.path.isfile(candidate_path):
            return candidate_path
        else:
            current_path = os.path.dirname(current_path)
    
    # Check for default path `~/.config/conftext.ini`
    candidate_path = default_config_path()
    if os.path.isfile(candidate_path):
        return candidate_path
    
    # Finally return false if no conf file found.
    return False


def ask_path():
    cwd_config_path = os.path.join(os.getcwd(), CONFTEXT_FILENAME)
    print("No config file was found. Create one with default settings?")
    print("[1] %s" % default_config_path())
    print("[2] %s" % cwd_config_path)
    choice = input("Type 1 or 2 then enter: ")
    
    if choice == '1':
        return default_config_path()
    elif choice == '2':
        return cwd_config_path
    else:
        sys.exit('Invalid choice: %s' % choice)


def write_to_file(filepath, config):
    with open(filepath, 'w') as config_file_obj:
        config.write(config_file_obj)
    print("Wrote config to %s" % filepath)


def read_from_file(config_filepath_or_string) -> ConfigParser:
    config = ConfigParser(default_section=CONFTEXT_SECTION)
    if not config.read(config_filepath_or_string):
        config.read_string(config_filepath_or_string)
    return config


def format_string(config):
    return '[%s]' % '/'.join(config[CONFTEXT_SECTION].values())


def get_schemas():
    return {ep.name: ep.load() for ep in pkg_resources.iter_entry_points(group='conftext')}


def initialize_config() -> ConfigParser:
    """
    Create initial config
    """
    
    # select from registered schamas in package entries
    schemas = dict(enumerate(get_schemas().items(), start=1))
    print("Schemas registered as entry points:")
    for num, (name, schema) in schemas.items():
        print(num, name, schema)
    
    in_val = input('select schema by number: ')
    name, selected_schema = schemas[int(in_val)]
    print("selected '%s': %s" % (name, selected_schema))
    
    print(dict(selected_schema()))
    
    # create and return selected config
    schema = ConfigParser()
    schema[CONFTEXT_SECTION] = dict(selected_schema())
    return schema
