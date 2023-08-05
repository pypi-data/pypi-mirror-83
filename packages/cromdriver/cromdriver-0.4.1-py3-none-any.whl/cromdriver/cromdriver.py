import os
import errno
import sys
import zipfile
import io

import requests
from appdirs import user_data_dir

URL_CHROMEDRIVER = 'http://chromedriver.storage.googleapis.com/'
APP_DATA = user_data_dir('cromdriver')


def get_latest_release_web() -> str:
    """Get the latest release of chromedriver in on the website
    """
    response = requests.get(URL_CHROMEDRIVER + 'LATEST_RELEASE')
    if response.ok:
        return response.text


def create_release_directory(version):
    """Download the chromedriver from website

    Args:
        version (str): version of chromedriver to download
    """
    path = os.path.join(APP_DATA, 'RELEASE', version)
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


def get_chromedriver_path(version=None) -> str:
    """Get the directory path where binaries are

    Args:
        version (str): version of chromedriver to download. Optional, last release by default
    """
    if version is None:
        version = get_latest_release_file()

    return os.path.join(APP_DATA, 'RELEASE', version)


def get_chromedriver_url(version, platform) -> str:
    """Create the URL for downloading chromedrivers

    Args:
        version (str): version of chromedriver to download
        platform (str): version of chromedriver to download
    """
    if platform == 'linux':
        architecture = '64'
    elif platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif platform == 'win':
        architecture = '32'
    else:
        raise RuntimeError(
                'Could not determine chromedriver download URL for this platform.')

    return URL_CHROMEDRIVER + version + '/chromedriver_' + platform + architecture + '.zip'


def download_binary(url, target_location):
    """Download binary from URL

    Download a zip and extract it in a target location

    Args:
        url (str): URL of the zip file
        target_location (str): path where to extract
    """
    response = requests.get(url)
    if response.ok:
        z_file = zipfile.ZipFile(io.BytesIO(response.content))
        z_file.extractall(target_location)
    else:
        print('Impossible to download zip from url : {}'.format(url))


def set_latest_release_file(version):
    """Create a file with the latest release version

    Args:
        version (str): version of chromedriver to download
    """
    path = os.path.join(APP_DATA, 'RELEASE', 'LATEST_RELEASE')
    with open(path, 'w') as outfile:
        outfile.write(version)


def get_latest_release_file() -> str:
    """Get the latest release version downloaded installed
    """
    path = os.path.join(APP_DATA, 'RELEASE', 'LATEST_RELEASE')
    try:
        with open(path, 'r') as infile:
            return infile.read()
    except FileNotFoundError:
        return None


def updating_path(path):
    """Adding chromedriver directory in the PATH environnemnt

    Args:
        path (str): path of the directory
    """
    if sys.platform.startswith('win'):
        os.environ['PATH'] += ';' + path
    else:
        os.environ['PATH'] += ':' + path


def test_url(url) -> bool:
    """Test if the url exists

    Args:
        url (str): URL to test
    """
    if requests.get(url).ok:
        return True
    return False


#def get_chromedriver_path():
#    return os.path.join(APP_DATA, 'RELEASE', get_latest_release_file())


def download_chromedriver(version, platform=None):
    """Download the chromedriver from website

    Args:
        version (str): version of chromedriver to download
    """

    if platform is None:
        if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
            platform = 'linux'
        elif sys.platform == 'darwin':
            platform = 'darwin'
        elif sys.platform.startswith('win'):
            platform = 'win'
        else:
            raise RuntimeError(
                'Could not determine chromedriver download URL for this platform.')

    url = get_chromedriver_url(version, platform)

    if test_url(url):
        print('Downloading version : {}'.format(version))
        create_release_directory(version)
        target_location = get_chromedriver_path(version)
        download_binary(url, target_location)
    else:
        raise RuntimeError('URL {} doesn\'t exists'.format(url))


def updating_chromedriver():
    """Compare the lastest release on website with the installed one.

    Download binary if not and add to PATH
    """

    latest_release_web = get_latest_release_web()
    latest_release_file = get_latest_release_file()

    if latest_release_web == latest_release_file:
        updating_path(get_chromedriver_path(latest_release_file))
    else:
        download_chromedriver(latest_release_web)

        set_latest_release_file(latest_release_web)
        latest_release_file = get_latest_release_file()

        updating_path(get_chromedriver_path(latest_release_file))
