from io import open
from os.path import dirname, join

from setuptools import setup


with open(join(dirname(__file__), 'README.md'), "rt") as fp:
    long_description = fp.read()


setup(
    name='tornado_m2crypto',
    use_scm_version=True,
    description="Extension for running tornado with M2Crypto instead of the standard python SSL module",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DIRACGrid/tornado_m2crypto',
    setup_requires=['setuptools_scm'],
    install_requires=[
        'enum34; python_version < "3.4"',
        'm2crypto',
        'tornado',
    ],
    packages=['tornado_m2crypto', 'tornado_m2crypto.test'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    keywords='dirac ',
    python_requires='>=2.7',
    extras_require={
        'testing': ['requests'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/DIRACGrid/tornado_m2crypto/issues',
        'Source': 'https://github.com/DIRACGrid/tornado_m2crypto/',
    },
)
