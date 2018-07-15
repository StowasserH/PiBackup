from setuptools import setup

setup(
    name='pibackup',
    version='0.0.1',
    description='Create easily a backup solution for your RaspbianPi',
    license='MIT',
    author='Harald Stowasser',
    author_email='lcars@stowasser.tv',
    packages=['pibackup'],
    keywords=['backup','raspbian','pi'],
    url='https://github.com/StowasserH/pibackup',
    entry_points={
        'console_scripts': [
            'pibackup = pibackup.__main__:main'
        ]
    })