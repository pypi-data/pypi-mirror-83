import ephem
import os
from os.path import join, dirname, abspath, isfile
from datetime import datetime, timedelta
import logging
import json
from jinja2 import Template

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

name = "pytle"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_path(filename):
        packagedir = abspath(__file__)
        fulldir = join(dirname(packagedir), 'data')
        fullname = join(fulldir, filename)
        return fullname


class pytle:
    def __init__(self, keps_url='', cache=False):

        if keps_url:
            if cache:
                cache_dir = os.environ.get('HOME') + '/.' + type(self).__name__
                keps = self.try_cache(keps_url, cache_dir)
            else:
                keps = self.download_keps(keps_url)

            self.satlist = self.load_keps(keps)

    def get_sat_info(self, name):
        item = self.satlist.get(name, {})
        if "ephem" in item:
            item.pop("ephem")
        return item

    def get_sat_info_text(self, name):
        with open(get_path('templates/sat_info.j2')) as sat_info:
            template = Template(sat_info.read())
        return template.render(self.get_sat_info(name))

    def download_keps(self, keps_url):
        logging.debug("Downloading keps from " + keps_url)
        try:
            with urlopen(keps_url) as response:
                self.data = data = response.read()
                kep_lines = data.decode().split('\n')
        except TimeoutError:
            logging.error("Timeout in accessing " + keps_url)
            exit()

        return kep_lines

    def cache_keps(self, cache_file):
        logging.debug("Writing keps cache to " + cache_file)
        with open(cache_file, 'wb') as out_file:
            out_file.write(self.data)

    def load_keps(self, keps):
        satlist = {}
        kepslist = []
        self.names = names = [line.translate(str.maketrans(' ', '_')) for i, line in enumerate(keps) if i % 3 == 0]
        for i, line in enumerate(keps):
            if i % 3 == 2:
                name = keps[i - 2].strip().translate(str.maketrans(' ', '_'))
                eph = ephem.readtle(
                    keps[i - 2],
                    keps[i - 1],
                    keps[i])
                logging.debug("TLE " + name)
                satlist[name] = {}

                # Load satellite specific defaults (band, frequencies, mode)
                if isfile(get_path("sats/" + name + ".json")):
                    with open(get_path("sats/" + name + ".json")) as file:
                        satinfo = json.loads(file.read())
                        logging.debug("SAT " + name)

                    for key, value in satinfo[name].items():
                        try:
                            # Python 2
                            key = key.encode('utf-8') if isinstance(key, unicode) else key
                            value = value.encode('utf-8') if isinstance(value, unicode) else value
                        except NameError:
                            # Python 3 (nothing)
                            pass

                        satlist[name][key] = value

                satlist[name]["ephem"] = eph

        logging.debug("Loaded %s satellites" % len(names))
        return satlist

    def try_cache(self, keps_url, cache_dir):
        cache_file = cache_dir + '/keps.txt'
        cache_days = 7
        cache_file_ts = None
        keps = None

        # If the cache dir does not exist
        if not os.path.isdir(cache_dir):
            os.mkdir(cache_dir)

        # If the cache file does not exist
        if not os.path.isfile(cache_file):
            keps = self.download_keps(keps_url)
            self.cache_keps(cache_file=cache_file)

        # If the cache file exits
        else:
            weekago = datetime.now() - timedelta(days=cache_days)
            cache_file_ts = datetime.fromtimestamp(os.path.getctime(
                cache_file))

            # If the cache exists and is up to date
            if cache_file_ts > weekago:
                logging.debug("Using cached keps from " + cache_file)
                with open(cache_file) as file:
                    return file.read().split('\n')
            else:
                keps = self.download_keps(keps_url)
                self.cache_keps(cache_file=cache_file)

        return keps

