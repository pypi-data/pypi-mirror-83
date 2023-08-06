#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import subprocess,sys

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'paho-mqtt==1.5.1', 'spidev', 'sockets', 'RPi.GPIO', 'adafruit-circuitpython-dht']
# production program requirements. eg ADC libraries, etc that i will use.
# requirements has debug n dev tools etc what u will include in venv

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Kudzai Chris Kateera",
    author_email='kckateera@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Smart, Iot-enabled greenhouse monitoring and control API",
    entry_points={
        'console_scripts': [
            'smartagro=smartagro.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='smartagro',
    name='smartagro',
    packages=find_packages(include=['smartagro', 'smartagro.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/chris-kck/smartagro',
    version='0.2.0',
    zip_safe=False,
)
