import logging
import sys
import tempfile
import zipfile
import pathlib
from urllib import request
from driverloader import constant

DEFAULT_VERSION = '71.0.3578.80'
DEFAULT_DOWNLOAD_URL = 'https://npm.taobao.org/mirrors/chromedriver'

logging.basicConfig(level=logging.INFO)


class ChromeDriver:
    def __get__(self, instance, owner):
        return get_chrome_driver()


def get_chrome_filename():
    """parse filename using platform"""
    platform = sys.platform
    platforms = {
        "win32": "win32",
        "win64": "win64",
        "linux": "linux64",
        "darwin": "mac64",
    }
    return 'chromedriver_{}.zip'.format(platforms.get(platform, ''))


def download_chrome_driver(version=None, mirror_url=None):
    """Download web driverloader from URL"""
    version = version if version else DEFAULT_VERSION
    host = mirror_url if mirror_url else DEFAULT_DOWNLOAD_URL
    url = '/'.join([host, str(version), get_chrome_filename()])
    logging.info("Downloading chrome webdriver. Please wait...")
    r = request.urlopen(url)
    logging.info("Downloading chrome webdriver finished")
    return r


def save_chrome_driver(response, target=None):
    """Save the data of download_chrome_driver."""
    with tempfile.TemporaryFile() as f:
        f.write(response.read())
        zip_file = zipfile.ZipFile(f)
        if not zip_file:
            raise ValueError("Not a zip file format")
        for file in zip_file.filelist:
            chrome_driver = pathlib.Path(target) / file.filename
            if not chrome_driver.exists():
                zip_file.extract(file, target)
            return str(chrome_driver)


def get_chrome_driver(target=None, version=None, mirror_url=None):
    """
    Get chrome driverloader from mirror_url, save to target.
    :param target: the path dir to save the driverloader
    :param version: driverloader version
    :param mirror_url: resource url to get the driverloader
    :return:
    """
    target = target if target else constant.CHROME_PATH
    abs_target = pathlib.Path(target).resolve()
    # gen = abs_target.iterdir()
    # for f in gen:
    #     if 'chromedriver' in f.name:
    #         return str(f)
    driver_data = download_chrome_driver(version, mirror_url)
    return save_chrome_driver(driver_data, abs_target)
