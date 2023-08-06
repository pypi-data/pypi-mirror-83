#!/usr/bin/env python3
#
# Tiny webservice to host password protected cfg files placed in /cfgdir inside a container
#

import os
import re
import sys
import logging
from io import BytesIO
import configparser
from flask import Flask, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Forbidden, NotFound

app = Flask(__name__)
auth = HTTPBasicAuth()
log = logging.getLogger('globconfd')
passwords, paths = None, None
root_dir = os.environ.get('ENVUSERROOT', '/configs')
if app.debug or os.environ.get('DEBUG', False):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log.setLevel(logging.DEBUG)
    app.debug = True
else:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    log.setLevel(logging.INFO)

log.info('hosting files from %s', root_dir)


@auth.verify_password
def verify_password(username, password):
    if username in passwords and check_password_hash(passwords.get(username), password):
        log.debug('Validated password of %s', username)
        return username
    log.debug('Could not validate password of user %s', username)
    return False


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@auth.login_required
def index(path):
    log.info('GET %s from %s', path, auth.current_user())
    path_regex = paths[auth.current_user()]
    if not re.match(path_regex, path):
        raise Forbidden('{} does not have access to read {} - paths must match {}'.format(auth.current_user(),
                                                                                          path, path_regex))
    abs_path = os.path.join(root_dir, path)
    try:
        f = open(abs_path, 'rb')
        bs = BytesIO(b'')
        bs.write(f.read())
        f.close()
        bs.seek(0)
        log.debug('Was able to read file %s for %s - sending it now', abs_path, auth.current_user())
        name = os.path.basename(abs_path)
        return send_file(filename_or_fp=bs, mimetype='text/plain', attachment_filename=name, as_attachment=True)
    except FileNotFoundError as fnfe:
        log.error('Was unable to locate file %s for %s', abs_path, auth.current_user())
        raise NotFound('No file {} exists?'.format(path))
    except PermissionError as pe:
        log.error('Was not allowed to read file %s for %s', abs_path, auth.current_user())
        raise Forbidden('The file in {} is not allowed to be read by this service? Check permissions'.format(path))


def read_users():
    global passwords, paths
    if passwords is not None:
        return
    users_cfg = configparser.ConfigParser()
    file = os.environ.get('ENVUSERCFGFILE', '/env_users.conf')
    log.info('Reading users from %s', file)
    users_cfg.read(file)
    passwords = {}
    paths = {}
    for section in users_cfg.sections():
        user = users_cfg.get(section, 'username')
        passwords[user] = generate_password_hash(users_cfg.get(section, 'password'))
        paths[user] = r'{}'.format(users_cfg.get(section, 'path_regex'))
        log.debug('Initialized user %s with path regex %s', user, paths[user])


read_users()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.debug)
