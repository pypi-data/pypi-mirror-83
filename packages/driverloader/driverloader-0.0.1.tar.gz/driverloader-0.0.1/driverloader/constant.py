from pathlib import Path

DRIVER_DIR = 'executor'
DRIVER_PATH = Path(__file__).parent.resolve() / DRIVER_DIR
if not DRIVER_PATH.exists():
    DRIVER_PATH.mkdir()

CHROME_PATH = DRIVER_PATH / 'chrome'
FIREFOX_PATH = DRIVER_PATH / 'firefox'
if not CHROME_PATH.exists():
    CHROME_PATH.mkdir()
if not FIREFOX_PATH.exists():
    FIREFOX_PATH.mkdir()

# chrome_driver = DRIVER_PATH / 'chromedriver.exe'
# firefox_driver = DRIVER_PATH / 'geckodriver.exe'
