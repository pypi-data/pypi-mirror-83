## Quick start:

Download chrome driver:
```python
from driverloader import drivers
print(drivers.chrome)
```

Download firefox driver:
```python
from driverloader import drivers
print(drivers.firefox)
```

The drivers would be downloaded in **executor/** dir of the webdrivers package.
You can find chromedriver.exe or geckodriver.exe in the dir.


Using with selenium:
```python
from selenium.webdriver import Chrome
from driverloader import drivers

browser = Chrome(drivers.chrome)
browser.quit()
```

Downloading to customized path:
```python
import driverloader
driver_path = driverloader.get_chrome_driver(target='.')
```

or absolute path:
```python
import pathlib
import driverloader

current_dir = pathlib.Path(__file__).parent.parent
print(driverloader.get_chrome_driver(current_dir))
```

## command line
Using driverloader by command line like this:
```bash
driverloader chrome .
driverloader firefox .
```
Two arguments:
- driver_name, chrome and firefox supported.
- path,  the path you want to save the driver.

Options:
- `-v` or `--version`, pool support now.


## Mirror URL
webdriver-downloader get the drivers from https://npm.taobao.org/mirrors/
- chrome driver: https://npm.taobao.org/mirrors/chromedriver/
- firefox driver: https://npm.taobao.org/mirrors/geckodriver/