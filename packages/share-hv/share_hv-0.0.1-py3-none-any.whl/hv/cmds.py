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

_JSON_PREFIX = 'INSTRUMENTATION_STATUS: stream={"windows":'
_JSON_STRIP = 'INSTRUMENTATION_STATUS: stream='
_WM_SIZE_RE = re.compile(r'(\d+)x(\d+)')
_HV_URL = 'https://share-hv-test.wn.r.appspot.com/hv/v1/new-hv'

@click.group()
def cli():
    pass

def _adb(cmd):
    '''Run adb in a subprocess'''
    with subprocess.Popen(cmd, universal_newlines=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        stdout, errs = p.communicate()

    if len(errs) > 0:
        raise click.UsageError('''
%s
Please fix this adb error. If you have multiple devices connected,
you can use the --device argument to specify which device to use.
''' % errs)

    return stdout

def _install(adb, apk):
    '''Run adb to install the provided path to the apk'''
    cmd = [adb, 'install', '-t', '-r', apk]
    result = _adb(cmd)
    if result.find('uccess') < 0:
        raise click.UsageError('''
%s
Unable to install instrumention apk '%s'
''' % (result, apk))

def _uninstall(adb, package):
    '''Run adb to install the package'''
    cmd = [adb, 'uninstall', package]
    return _adb(cmd)
    
def _wmsize(adb):
    '''Run adb to get the device size'''
    cmd = [adb, 'exec-out', 'wm', 'size']
    result = _adb(cmd)
    m = re.search(_WM_SIZE_RE, result)
    if not m:
        raise click.UsageError('''
%s
Unable to find window size
''' % result)
    return (m.group(1), m.group(2))

def _instrument(adb):
    '''Run adb to instrument the app'''
    cmd = [adb, 'exec-out', 'am', 'instrument', '-r', '-w', 'com.kbs.hv.test/androidx.test.runner.AndroidJUnitRunner']
    return _adb(cmd)

def _screencap(adb, path):
    '''Capture a screencap to the provided path'''
    cmd = [adb, 'exec-out', 'screencap', '-p']
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        screencap, errs = p.communicate()
    if len(screencap) == 0:
        raise click.UsageError('''
%s
Unable to obtain a screencap!
''' % errs)
    with open(path, 'w+b') as f:
        f.write(screencap)

@cli.command()
@click.option('--device', default='', help='Use device with the given id')
def grab(device):
    '''Grab a snapshot of the currently displayed app.'''
    config = settings.load_settings()
    adb = settings.get_option(config, 'adb')
    if not adb:
        raise click.UsageError('''
Please set the path to your adb binary with
share-hv set adb path/to/adb

The adb binary will usually be at <sdk_root>/platform-tools/adb
''')
    if not Path(adb).is_file:
        raise click.UsageError('''
The path to the adb binary
%s
does not exist. Please correct the path with
share-hv set adb path/to/adb
The adb binary will usually be at <sdk_root>/platform-tools/adb
''' % adb)

    here = os.path.dirname(__file__)
    print('Obtaining window size')
    (dwidth, dheight) = _wmsize(adb)
    print('Setting up instrumentation...')
    _install(adb, os.path.join(here, 'apks', 'app-debug.apk'))
    _install(adb, os.path.join(here, 'apks', 'app-debug-androidTest.apk'))
    print('Capturing layout...')
    lines = _instrument(adb)
    print('Taking screenshot...')
    (fd, screencap) = tempfile.mkstemp(suffix='.png')
    os.close(fd)
    _screencap(adb, screencap)
    print('Cleaning up instrumentation...')
    _uninstall(adb, 'com.kbs.hv')
    _uninstall(adb, 'com.kbs.hv.test')

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

