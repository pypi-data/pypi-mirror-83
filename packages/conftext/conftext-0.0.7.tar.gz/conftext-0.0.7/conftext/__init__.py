__version__ = "0.0.7"

from configparser import ConfigParser
from pydantic import BaseModel
from invoke import task, Program, Collection
from conftext import conftext
from conftext import conf_ini


###
# Schema
###

# NOTE: ConfigParser doesn't like `None`, so we use strings for now.

class MultiTenantV1(BaseModel):
    service: str = str(None)
    context: str = str(None)


class MultiTenantV2(BaseModel):
    tenant: str = str(None)
    environment: str = str(None)


###
# Public API
###

class NoConftext(Exception):
    pass


def get_config(**kwargs) -> ConfigParser:
    """
    Get config
    
    kwargs can be used to overwrite settings from config file. If the value of a kwarg is `None`,
    it will be ignored.
    """
    config_file = conftext.find_file()
    
    if not config_file and not kwargs:
        raise NoConftext('No "%s" file found and no kwargs given.' % conftext.CONFTEXT_FILENAME)
    
    if config_file:
        config = conftext.read_from_file(config_file)[conftext.CONFTEXT_SECTION]
    else:
        config = dict()
    
    for key, val in kwargs.items():
        if val is not None:
            config[key] = val
    
    return config


def get_config_v2(**kwargs) -> ConfigParser:
    config_file = conftext.find_file()
    
    if not config_file and not kwargs:
        raise NoConftext('No "%s" file found and no kwargs given.' % conftext.CONFTEXT_FILENAME)
    
    config = conftext.read_from_file(config_file)
    
    for key, val in kwargs.items():
        if val is not None:
            config[config.default_section][key] = val
    
    return config


def get_ini_config(config_filepath, conftext=None, module_name=None):
    """
    Get config from ini file
    
    Can use module name to look for config file in corresponding path under `~/.config`. Only use
    the conftext machinery if its nexessary to select from multiple sections in config file.
    """
    config_file = conf_ini.read_config(config_filepath)
    return conf_ini.get_config_section(config_file, conftext, module_name)


###
# Tasks
###

@task(default=True)
def show(ctxt, verbose=False):
    """
    Show config context
    """
    config_file = conftext.find_file()
    if not config_file:
        config_file = conftext.ask_path()
        config = conftext.initialize_config()
        conftext.write_to_file(config_file, config)
    if verbose:
        print(config_file)
    print(conftext.format_string(conftext.read_from_file(config_file)))


@task
def schemas(ctxt):
    """
    List all schemas
    """
    for key, val in conftext.get_schemas().items():
        print(key, val.schema_json())


@task
def init(ctxt):
    """
    Initialize a conftext file
    """
    config = conftext.initialize_config()
    print(config)


###
# Invoke setup
###

namespace = Collection()
namespace.add_task(init)
namespace.add_task(show)
namespace.add_task(schemas)
program = Program(namespace=namespace)
