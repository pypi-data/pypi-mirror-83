import hv.settings as s
from pathlib import Path

def test_read(tmpdir):
    d = Path(tmpdir / 'config')
    if not d.is_dir():
        d.mkdir(parents=True)
    p = Path(d, 'settings.ini')
    p.write_text('''
[common]
adb = /a/b/c
''')
    config = s.load_settings(p)
    assert s.get_option(config, 'adb') == '/a/b/c'

def test_replace(tmpdir):
    d = Path(tmpdir / 'config')
    if not d.is_dir():
        d.mkdir(parents=True)
    p = Path(d, 'settings.ini')
    config = s.load_settings(p)
    assert s.get_option(config, 'abc') == None
    s.set_option(config, 'abc', 'def')
    s.replace_settings(config, p)
    config = s.load_settings(p)
    assert s.get_option(config, 'abc') == 'def'
