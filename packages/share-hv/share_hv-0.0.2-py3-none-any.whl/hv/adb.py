import subprocess
import click
import re

class Adb:
    _WM_SIZE_RE = re.compile(r'(\d+)x(\d+)')
    _PKG_VERSION_NAME_RE = re.compile(r'versionName=([\d+.]+)')
    _PKG_VERSION_CODE_RE = re.compile(r'versionCode=([\d+.]+)')

    def _run(self, cmd):
        '''Run adb in a subprocess'''
        cmd.insert(0, self._adb)
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

    def __init__(self, adb):
        self._adb = adb

    def install(self, apk):
        '''Run adb to install the provided path to the apk'''
        cmd = ['install', '-t', '-r', apk]
        result = self._run(cmd)
        if result.find('uccess') < 0:
            raise click.UsageError('''
%s
Unable to install instrumention apk '%s'
''' % (result, apk))

    def uninstall(self, package):
        '''Run adb to install the package'''
        cmd = ['uninstall', package]
        return self._run(cmd)
    
    def packageInfo(self, pkg):
        '''Get the version name and code for the package, or None'''
        cmd = ['exec-out', 'dumpsys', 'package', pkg]
        result = self._run(cmd)
        name = re.search(Adb._PKG_VERSION_NAME_RE, result)
        if not name:
            return None
        code = re.search(Adb._PKG_VERSION_CODE_RE, result)
        if not code:
            return None
        return (name.group(1), code.group(1))

    def wmsize(self):
        '''Run adb to get the device size'''
        cmd = ['exec-out', 'wm', 'size']
        result = self._run(cmd)
        m = re.search(Adb._WM_SIZE_RE, result)
        if not m:
            raise click.UsageError('''
%s
Unable to find window size
''' % result)
        return (m.group(1), m.group(2))

    def instrument(self, testPackageId):
        '''Run adb to instrument the app'''
        cmd = ['exec-out', 'am', 'instrument', '-r', '-w', '{}/androidx.test.runner.AndroidJUnitRunner'.format(testPackageId)]
        return self._run(cmd)

    def screencap(self, path):
        '''Capture a screencap to the provided path'''
        cmd = [self._adb, 'exec-out', 'screencap', '-p']
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            screencap, errs = p.communicate()
            if len(screencap) == 0:
                raise click.UsageError('''
%s
Unable to obtain a screencap!
''' % errs)
            with open(path, 'w+b') as f:
                f.write(screencap)

