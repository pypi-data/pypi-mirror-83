import configparser

"""
global/singleton config object to be uses across modules
"""
config = None


def verify_required_options(section, option_keys):
    """
    Verifies that section exists, and that it has option_keys defined
    :param str section: Section in the config
    :param list[str] option_keys: list of required options
    :rtype: SectionProxy
    """
    myconfig = read_config()
    if section not in myconfig:
        raise configparser.NoSectionError(section)
    for option in option_keys:
        if option not in myconfig[section]:
            raise configparser.NoOptionError(option, section)
    return myconfig[section]


def read_config(path='config.ini', force=False):
    """
    :param str path:
    :param bool force:
    :rtype: ConfigParser
    """
    global config
    if not config or force:
        config = configparser.ConfigParser()
        config.read(path)
    return config


def fetch_config(url, user, password, cache_timeout=86400, force=False):
    """
    :param str url:
    :param str user:
    :param str password:
    :param int cache_timeout: timeout seconds
    :param bool force: force config reload
    :rtype: ConfigParser
    """
    global config
    if not config or force:
        import os
        import hashlib
        from diskcache import Cache
        from requests import get
        from requests.auth import HTTPBasicAuth
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cfg_path = os.environ.get('GLOBCONF_CACHE_PATH', 'tmp')
        config = configparser.ConfigParser()

        with Cache(cfg_path, timeout=cache_timeout) as c:
            cfg_string = c.get(url_hash)
            if cfg_string is None:
                r = get(url, auth=HTTPBasicAuth(user, password))
                r.raise_for_status()
                cfg_string = r.text
                c.add(url_hash, cfg_string)
        config.read_string(cfg_string)
    return config
