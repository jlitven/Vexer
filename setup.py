from setuptools import setup

setup(
    name = 'vexer',
    version = '0.2',
    description = 'Vocabulary expander using anki and mac osx dictionary.',
    url = 'https://github.com/jlitven/vexer',
    download_url = 'https://github.com/jlitven/vexer/archive/v0.2-alpha.tar.gz',
    keywords = ['anki', 'english', 'vocabulary'],
    author = 'Joshua Litven',
    author_email = 'jlitven@gmail.com',
    license = 'MIT',
    packages = ['vexer', 'anki', 'vexer.card_creator', 'anki.importing',
    'anki.template'],
    package_dir = {'vexer': 'src/vexer',
                    'anki': 'src/anki',
                    'vexer.card_creator': 'src/vexer/card_creator',
                    'anki.importing': 'src/anki/importing',
                    'anki.template': 'src/anki/template'},
    entry_points={
        'console_scripts': [
            'vexer = vexer.vocabulary_creator:main',
        ],
    },
)
