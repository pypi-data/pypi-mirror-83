
from setuptools import setup, find_packages
from letsformat.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='letsformat',
    version=VERSION,
    description='Simple File Format Converter',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Matthew Holden',
    author_email='matthewholden01@gmail.com',
    url='https://github.com/matthewholden01/letsformat',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'letsformat': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        letsformat = letsformat.main:main
    """,
    install_requires=['exifread', 'pyyaml', 'colorlog', 'astropy', 'pillow']
)