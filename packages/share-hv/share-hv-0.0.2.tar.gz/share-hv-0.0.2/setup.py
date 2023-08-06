from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='share-hv',
    version='0.0.2',
    description='Share simple hierarchy-view like screenshots of your Android app',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='KB Sriram',
    author_email='kbsriram@gmail.com',
    url='https://github.com/kbsriram/share-hv-python-client',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Click>=7.1.2',
        'requests>=2.24',
    ],
    extras_require={
        'dev': [
            'pytest >= 3.6',
            'check-manifest',
            'twine',
        ],
    },
    package_dir = {'' : 'src' },
    packages=['hv'],
    package_data={
        'hv' : ['apks/app-debug.apk', 'apks/app-debug-androidTest.apk'],
    },
    entry_points= {
        'console_scripts' : ['share-hv=hv.cmds:cli'],
    },
)
