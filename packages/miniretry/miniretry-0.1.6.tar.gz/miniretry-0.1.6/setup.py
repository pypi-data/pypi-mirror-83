from setuptools import setup

setup(
    name="miniretry",
    version="0.1.6",
    description="Retry helpers",
    author="Martin Czygan",
    author_email="martin.czygan@gmail.com",
    url="http://github.com/miku/miniretry",
    packages=['miniretry'],
    entry_points={
        'console_scripts': [
            'miniretry=miniretry.main:main'
        ]
    },)
