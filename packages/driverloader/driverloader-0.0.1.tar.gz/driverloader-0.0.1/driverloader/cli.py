import click
from driverloader.chrome_driver import get_chrome_driver
from driverloader.firefox_driver import get_firefox_driver


def download_driver(name: str, dst=None, version=None):
    if name.lower() == 'chrome':
        return get_chrome_driver(target=dst, version=None)
    elif name.lower() == 'firefox':
        return get_firefox_driver(target=dst, version=None)
    raise ValueError("name must be chrome or firefox")


@click.command()
@click.argument('driver_name', type=click.Choice(['chrome', 'firefox']))
@click.argument('path', type=click.Path(exists=True))
@click.option('-v', '--version')
def cli(driver_name, path, version):
    """Webdriver downloader  of chrome and firefox.

    - driver_name: Which driver, [chrome, firefox] supported.\n
    - path: Path to save the driver.
    """
    return download_driver(driver_name, path, version=version)


if __name__ == '__main__':
    cli()
