# globconf

Creates a global configparser object, regardless of the project and module in need of it
In addition a docker container can be used to host protected config files, consumable by the parser object
 

## Getting Started
In a project using globconf:
```
from globconf import config, verify_required_options, read_config, fetch_config
# when starting the app, the config can be loaded from a specific path:
read_config(path='flaf.ini', force=True)  # will reload the config, even if it already is loaded
# or from the globconfd container, where caching is supported as convenience for offline developers:
load_config('http://localhost:5000/env_users.conf.dist', 'user', 'pass', cache_timeout=86400, force=True)
# if config is not explicitly loaded, it will default to automatically attempt to read in config.ini.

# required options are verified using verify_required_options, which will return a configparser.SectionProxy
cfg = verify_required_options('Section name', ['list', 'of', 'required', 'options', 'for', 'the', 'section'])
 
# beyond this, its still basic ConfigParser as you know it..
```

In modules:
```
from globconf import verify_required_options
class module(object):
    def __init__(self):
        sec = 'service now'
        self.cfg = verify_required_options(sec, ['host', 'user', 'pwd'])
        if not self.cfg.getboolean('verify_ssl', fallback=True):
            import urllib3
            urllib3.disable_warnings(InsecureRequestWarning)
```

And your module is happy as long as someone has initialised the needed section in the global config.

##globconfd via docker
docker run -it -v ./users.conf:env_users.conf -v ./cfgs:/configs -p 5000:5000 ssch/globconfd:latest -d

### Prerequisites

configparser, diskcache, requests


### Building
Build:
```
sudo python setup.py sdist bdist_wheel
twine upload dist/*
```



## Authors

* **Steffen Schumacher** - *Initial work* - [steffenschumacher](https://github.com/steffenschumacher)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
Nahh..
