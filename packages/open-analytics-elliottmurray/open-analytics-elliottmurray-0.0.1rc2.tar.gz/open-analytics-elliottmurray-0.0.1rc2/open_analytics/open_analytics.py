"""Open Analytics main file."""

import os
import platform
import sys
import tarfile
import requests
import pkg_resources
import uuid

DEFAULT_ENDPOINT = 'https://astut.io/capture'
INSTALL = 'install'
START = 'start'
END = 'end'
UUID = str(uuid.uuid4())


def install_start_event(project_id, package_name, **kwargs):
    project_id = str(project_id)  # need to make this an int maybe?
    print("Sending {}".format(project_id))
    endpoint = os.environ.get('OA_CAPTURE_ENDPOINT', DEFAULT_ENDPOINT)

    version = kwargs.get('version')
    if(version is None):
        version = pkg_resources.get_distribution(package_name).version

    event = {
        "project_id": project_id,
        "event_type": INSTALL,
        "event_subtype": START,
        "uuid": UUID,
        "platform": determine_platform(),
        "language": "python",
        "language_version": sys.version.split()[0],
        "package_name": package_name,
        "package_version": version,
        "metadata": {
            "ruby_version": kwargs.get('PACT_STANDALONE_VERSION', None),
        },
    }
    r = requests.post(endpoint, json=event)
    return r


def install_end_event(project_id, package_name, **kwargs):
    project_id = str(project_id)  # need to make this an int maybe?
    print("Sending {}".format(project_id))
    endpoint = os.environ.get('OA_CAPTURE_ENDPOINT', DEFAULT_ENDPOINT)

    version = kwargs.get('version')
    if(version is None):
        version = pkg_resources.get_distribution(package_name).version

    event = {
        "project_id": project_id,
        "event_category": INSTALL,
        "event_type": INSTALL,
        "event_subtype": END,
        "uuid": UUID,
        "platform": determine_platform(),
        "language": "python",
        "language_version": sys.version.split()[0],
        "package_name": package_name,
        "package_version": version,
        "metadata": {
            "ruby_version": kwargs.get('PACT_STANDALONE_VERSION', None),
        },
    }
    r = requests.post(endpoint, json=event)
    return r



def determine_platform():
    target_platform = platform.platform().lower()
    if 'darwin' in target_platform or 'macos' in target_platform:
        target_platform = 'osx'
    elif 'linux' in target_platform and IS_64:
        target_platform = 'linux-x86_64'
    elif 'linux' in target_platform:
        target_platform = 'linux-x86'
    elif 'windows' in target_platform:
        target_platform = 'win32'
    return target_platform
