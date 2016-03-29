from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name = 'vexer',
    version = '0.2.1',
    description = 'Learn Vocabulary using Anki and Mac OS X dictionary.',
    long_description = long_description,
    url = 'https://github.com/jlitven/vexer',
    download_url = 'https://github.com/jlitven/vexer/releases/download/v0.2.1-alpha/vexer-0.2.1.tar.gz',
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
