from pathlib import Path
import configparser

_COMMON = 'common'

def load_settings(path=None):
    '''Read (or create) settings file.'''
    result = configparser.ConfigParser()
    p = path or _get_path()
    if p.is_file():
        result.read(p)
    return result

def replace_settings(config, path=None):
    '''Replace settings file with this.'''
    p = path or _get_path()
    with p.open(mode='w') as f:
        config.write(f)

def get_option(config, name):
    if not config.has_section(_COMMON):
        return None
    if not config.has_option(_COMMON, name):
        return None
    return config.get(_COMMON, name)

def set_option(config, name, value):
    if not config.has_section(_COMMON):
        config.add_section(_COMMON)
    config.set(_COMMON, name, value)


def _get_path():
    d = Path('~/.config/share-hv').expanduser()
    if not d.is_dir():
        d.mkdir(parents=True)
    return Path(d, 'settings.ini')
