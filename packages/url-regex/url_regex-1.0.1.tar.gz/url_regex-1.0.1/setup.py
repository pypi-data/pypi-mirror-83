import re

from setuptools import setup

version = ''
with open('url_regex/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.md', encoding='utf-8') as f:
    readme = f.read()


if not version:
    raise RuntimeError('version is not set')


setup(
    name='url_regex',
    author='AlexFlipnote',
    url='https://github.com/AlexFlipnote/url_regex',
    license='GPLv3',
    version=version,
    packages=['url_regex'],
    description='Regular expression for matching URLs in Python',
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
