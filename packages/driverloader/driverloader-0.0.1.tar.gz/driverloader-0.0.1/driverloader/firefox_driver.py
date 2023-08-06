import logging
import sys
import platform
import tempfile
import zipfile
import tarfile
import pathlib
from urllib import request
from driverloader import constant


DEFAULT_VERSION = 'v0.27.0'
DEFAULT_DOWNLOAD_URL = 'https://npm.taobao.org/mirrors/geckodriver'

logging.basicConfig(level=logging.INFO)


class FirefoxDriver:
    def __get__(self, instance, owner):
        return get_firefox_driver()

def get_firefox_filename(version=DEFAULT_VERSION):
    """parse filename using platform"""
    system = sys.platform
    if system.startswith('win'):
        system = system[:3]
    file_map = {
        "linux32": f"geckodriver-{version}-linux32.tar.gz",
        "linux64": f"geckodriver-{version}-linux64.tar.gz",
        "darwin32": f"geckodriver-{version}-macos.tar.gz",
        "darwin64": f"geckodriver-{version}-macos.tar.gz",
        "win32": f"geckodriver-{version}-win32.zip",
        "win64": f"geckodriver-{version}-win64.zip",
    }
    bit = platform.architecture()[0][:2]
    file = file_map.get(system + bit, '')
    return file


def download_firefox_driver(version=None, mirror_url=None):
    """Download web driverloader from URL"""
    version = version if version else DEFAULT_VERSION
    host = mirror_url if mirror_url else DEFAULT_DOWNLOAD_URL
    url = '/'.join([host, str(version), get_firefox_filename(version)])
    logging.info("Downloading firefox webdriver. Please wait...")
    r = request.urlopen(url)
    logging.info("Downloading firefox webdriver finished")
    return r


def save_firefox_driver(response, target=None):
    with tempfile.TemporaryFile() as f:
        f.write(response.read())
        if zipfile.is_zipfile(f):
            comp_file = zipfile.ZipFile(f)
        elif tarfile.is_tarfile(f):
            comp_file = tarfile.TarFile(f)
        else:
            raise ValueError("Not zip or tar format file")

        for file in comp_file.filelist:
            target = target if target else constant.FIREFOX_PATH
            abs_target = pathlib.Path(target).resolve()
            driver = pathlib.Path(abs_target) / file.filename
            if not driver.exists():
                comp_file.extract(file, abs_target)
            return str(driver)


def get_firefox_driver(target=None, version=None, mirror_url=None):
    """
    Get firefox driverloader from mirror_url, save to target.
    :param target: the path dir to save the driverloader
    :param version: driverloader version
    :param mirror_url: resource url to get the driverloader
    :return:
    """
    target = target if target else constant.FIREFOX_PATH
    abs_target = pathlib.Path(target).resolve()
    # gen = abs_target.iterdir()
    # for f in gen:
    #     if 'geckodriver' in f.name:
    #         return str(f)
    driver_data = download_firefox_driver(version, mirror_url)
    return save_firefox_driver(driver_data, abs_target)
