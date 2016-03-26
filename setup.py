from setuptools import setup, find_packages

setup(
    name = 'vex',
    version = '0.1',
    description = 'Vocabulary expander using anki and mac osx dictionary',
    url = 'https://github.com/jlitven/vex',
    keywords = ['anki', 'english', 'vocabulary'],
    author = 'Joshua Litven',
    author_email = 'jlitven@gmail.com',
    license = 'MIT',
    packages = ['vex', 'anki', 'vex.card_creator', 'anki.importing',
    'anki.template'],
    package_dir = {'vex': 'src/vex',
                    'anki': 'src/anki',
                    'vex.card_creator': 'src/vex/card_creator',
                    'anki.importing': 'src/anki/importing',
                    'anki.template': 'src/anki/template'},
    entry_points={
        'console_scripts': [
            'vex = vex.vocabulary_creator:main',
        ],
    },
)
