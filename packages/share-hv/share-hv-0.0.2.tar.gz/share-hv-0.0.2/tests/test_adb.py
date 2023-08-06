from hv.adb import Adb

def _mockrun(mp, str):
    mp.setattr(Adb, "_run", lambda a,b: str)

def test_wmsize(monkeypatch):
    _mockrun(monkeypatch, "Physical size: 1080x2340\n")
    adb = Adb('foo')
    (w, h) = adb.wmsize()
    assert w == '1080' and h == '2340'

def test_packageInfo(monkeypatch):
    _mockrun(monkeypatch, '''
    versionCode=1 minSdk=21 targetSdk=29
    versionName=1.0
''')
    adb = Adb('foo')
    (name, code) = adb.packageInfo('bar')
    assert name == '1.0' and code == '1'
