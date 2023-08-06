from unittest import TestCase
from configparser import NoSectionError, NoOptionError


class TestGlobconf(TestCase):
    def test_verify_required_options(self):
        from globconf import verify_required_options, read_config
        read_config('someapp.ini')
        try:
            cfg = verify_required_options('dummy cfg for app_user', ['test'])
            self.assertEqual(cfg['test'], 'test')
        except Exception as e:
            self.fail(str(e))
        try:
            cfg = verify_required_options('dummy cfg for app_user', ['absent'])
            self.fail('Was able to get SectionProxy for absent option?')
        except NoOptionError as noe:
            pass  # expected..

    def test_fetch_config(self):
        from globconf import verify_required_options, fetch_config
        from requests.exceptions import HTTPError, ConnectionError
        from time import time, sleep
        t1 = time()
        fetch_config('http://localhost:5000/tests/someapp.ini', 'app_user', 'app_pass', cache_timeout=1)
        t2 = time()
        fetch_config('http://localhost:5000/tests/someapp.ini', 'app_user', 'app_pass', cache_timeout=1, force=True)
        t3 = time()
        self.assertGreater(t2-t1, t3-t2, msg='Subsequent fetch of the config, after caching was slower?')
        print('Noncached: {}, cached: {}'.format(t2-t1, t3-t2))
        try:
            cfg = verify_required_options('dummy cfg for app_user', ['test'])
            self.assertEqual(cfg['test'], 'test')
        except Exception as e:
            self.fail(str(e))
        try:
            fetch_config('http://blah.com:5000/tests/someapp.ini', 'app_user', 'app_pass', cache_timeout=1, force=True)
            self.fail('Survived fetch of nonexistent host')
        except ConnectionError as he:
            pass
        sleep(1)
        try:
            fetch_config('http://localhost:5000/tests/bogus.ini', 'app_user', 'app_pass', cache_timeout=1, force=True)
            self.fail('Survived fetch of nonexistent url')
        except HTTPError as he:
            self.assertEqual(he.response.status_code, 404)
        sleep(2)
        try:
            fetch_config('http://localhost:5000/tests/someapp.ini', 'crapp_user', 'crapp_pass', cache_timeout=1, force=True)
            self.fail('Survived fetch using invalid auth')
        except HTTPError as he:
            self.assertEqual(he.response.status_code, 401)
        sleep(1)
        try:
            fetch_config('http://localhost:5000/tests/someapp.ini', 'build_agent', 'build_pass', cache_timeout=1, force=True)
            self.fail('Survived fetch using unauthed path')
        except HTTPError as he:
            self.assertEqual(he.response.status_code, 403)




