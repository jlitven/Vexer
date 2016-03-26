"""A module to create vocbulary flash cards using Anki.
Multiple-choice cards are automated from a list of words.
Words are taken from the mac osx dictionary.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a vocabulary_flash_cards_creatorconsistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='english-anki-cards',

    version='1.0.0',

    description='Create vocabulary flash cards using anki and the mac dictionary.',

    url='https://github.com/jlitven/vocabulary_flash_cards_creator',

    author='Joshua Litven',
    author_email='jlitven@gmail.com',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Users',
        'Topic :: Education',
        'Environment :: MacOS X',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='anki vocabulary english',
    packages=['english_anki_cards', 'anki'],
    package_dir = {'english_anki_cards': 'src/english_anki_cards',
                    'anki': 'src/anki'},

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'english_anki_cards = english_anki_cards.__main__:main',
        ],
    },
)
