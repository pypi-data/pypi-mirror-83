"""
Contains utils such as update checker

"""
from distutils.version import StrictVersion

import pkg_resources
import requests

PYPI_URL = "https://pypi.python.org/pypi/{}/json"


def _compare_version(pypi_version, pkg_name):
    pypi_version = StrictVersion(pypi_version)
    try:
        local_version = pkg_resources.get_distribution(pkg_name).version
    except pkg_resources.DistributionNotFound:
        local_version = "0.0.0"

    try:
        my_version = StrictVersion(local_version)
    except ValueError:
        print(f"Version '{local_version}' seems to be a dev version, assuming up-to-date")
        return

    if my_version < pypi_version:
        print(
            f"\nThere is a new version available! (yours: {my_version}, available: {pypi_version})"
            f"\nTo upgrade:\n\t$ pip install --upgrade {pkg_name}"
        )
    else:
        print(f"Up-to-date! (version {my_version})")


def check_pypi(pkg_name, timeout=5):
    print(f"\nChecking pypi for latest release of {pkg_name}...")

    pkg_data = {}
    try:
        response = requests.get(PYPI_URL.format(pkg_name), timeout=timeout)
        response.raise_for_status()
        pkg_data = response.json()
    except requests.exceptions.Timeout:
        print("Unable to reach pypi quickly, giving up.")
    except requests.exceptions.HTTPError as e:
        print("Error response from pypi: ", e.errno, e.message)
    except ValueError:
        print("Response was not valid json, giving up.")

    try:
        pypi_version = pkg_data["info"]["version"]
    except KeyError:
        print("Unable to parse version info from pypi")
    else:
        _compare_version(pypi_version, pkg_name)
    print("\n")
