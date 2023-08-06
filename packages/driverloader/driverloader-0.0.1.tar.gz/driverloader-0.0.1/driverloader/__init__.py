from .chrome_driver import get_chrome_driver, ChromeDriver
from .firefox_driver import get_firefox_driver, FirefoxDriver


class Drivers:
    chrome = ChromeDriver()
    firefox = FirefoxDriver()


drivers = Drivers()
