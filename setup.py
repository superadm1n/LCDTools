from distutils.core import setup

description = '''This module is designed to act as a library to easily interact with an LCD display
while using the minimal amount of pins and maintaining the maximum functionality'''

setup(
    name='LCDTools',
    version='1.0.0',
    keywords='LCD Liquid Crystal Display Library Driver Tools',
    url='https://github.com/superadm1n/LCDTools',
    license='MIT',
    author='Kyle Kowalczyk',
    author_email='kowalkyl@gmail.com',
    description='Library for interacting with LCD Display',
    long_description=description,
    install_requires=['RPi.GPIO==0.6.3', 'RPLCD==1.1.0'],
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ]
)