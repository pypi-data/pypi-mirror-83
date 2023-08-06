import click
import io
import json
import os
import re
import requests
import hv.settings as settings
import subprocess
import sys
import tempfile
from pathlib import Path
from hv.adb import Adb

_JSON_PREFIX = 'INSTRUMENTATION_STATUS: stream={"windows":'
_JSON_STRIP = 'INSTRUMENTATION_STATUS: stream='
_HV_URL = 'https://share-hv-test.wn.r.appspot.com/hv/v1/new-hv'
_APK_PKG = 'com.kbs.hv'
_APK_TEST_PKG = 'com.kbs.hv.test'
_APK_VERSION = '0.0.1'
_APK_VERSION_CODE = '1'

@click.group()
def cli():
    pass

@cli.command()
@click.option('--device', default='', help='Use device with the given id')
def grab(device):
    '''Grab a snapshot of the currently displayed app.'''
    config = settings.load_settings()
    adbPath = settings.get_option(config, 'adb')
    if not adbPath:
        raise click.UsageError('''
Please set the path to your adb binary with
share-hv set adb path/to/adb

The adb binary will usually be at <sdk_root>/platform-tools/adb
''')
    if not Path(adbPath).is_file:
        raise click.UsageError('''
The path to the adb binary
%s
does not exist. Please correct the path with
share-hv set adb path/to/adb
The adb binary will usually be at <sdk_root>/platform-tools/adb
''' % adbPath)

    adb = Adb(adbPath)
    print('Obtaining window size')
    (dwidth, dheight) = adb.wmsize()
    print('Setting up instrumentation...')
    shouldUninstall = False
    shouldInstall = False
    info = adb.packageInfo(_APK_PKG)
    infoTest = adb.packageInfo(_APK_TEST_PKG)
    if info is None:
        shouldInstall = True
    else:
        (name, code) = info
        if name != _APK_VERSION or code != _APK_VERSION_CODE:
            shouldInstall = True
            shouldUninstall = True
    if shouldUninstall:
        adb.uninstall(_APK_PKG)
        adb.uninstall(_APK_TEST_PKG)
    if shouldInstall:
        here = os.path.dirname(__file__)
        adb.install(os.path.join(here, 'apks', 'app-v{}.apk'.format(_APK_VERSION)))
        adb.install(os.path.join(here, 'apks', 'app-debug-androidTest.apk'))

    print('Capturing layout...')
    lines = adb.instrument(_APK_TEST_PKG)
    print('Taking screenshot...')
    (fd, screencap) = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    adb.screencap(screencap)

    jsonString = None
    for line in io.StringIO(lines):
        if line.startswith(_JSON_PREFIX):
            jsonString = line[len(_JSON_STRIP):]
            break

    if jsonString is None:
        raise click.UsageError('Unable to dump hierarchy, sorry %s' % lines)

    hvJson = json.loads(jsonString)
    hvJson['width'] = dwidth
    hvJson['height'] = dheight

    print('Uploading...')
    r = requests.post(_HV_URL, data = '{"version":1}')
    r.raise_for_status()
    upload = r.json()
    with open(screencap, 'rb') as f:
        r = requests.put(upload['screencap_url'], headers={'content-type': 'image/png'}, data=f)
        r.raise_for_status()
    os.remove(screencap)
    r = requests.put(upload['hv_url'], headers={'content-type': 'application/json'}, data=json.dumps(hvJson))
    r.raise_for_status()
    print('\nYour snapshot is ready at %s\n%s' % (upload['url'], upload['message']))

@cli.command()
@click.argument('name')
@click.argument('value')
def set(name, value):
    '''Saves a key-value pair in the settings.'''
    config = settings.load_settings()
    settings.set_option(config, name, value)
    settings.replace_settings(config)

