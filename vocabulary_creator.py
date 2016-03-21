#! /usr/bin/python

'''
Script to create anki vocabulary cards.
'''
from card_creator import create_cards, AnkiObject, HTML
from dictionary_parser import dictionary_entry
from collections import namedtuple
import argparse, logging, re
from ConfigParser import SafeConfigParser
import os, sys

# SOMEDAY: Fix vocab definitions for 'groovy', 'party', 'pumpkin', 'a'

class AnkiWord(AnkiObject):

    '''
    Stores vocabulary information.
    '''
    tag_name = 'vocabulary'
    model_name = 'Vocabulary'

    styling_text = '''
.card {
 font-family: baskerville;
 font-size: 15px;
 text-align: left;
 color: black;
 background-color: white;
}

.description, .usage {
 margin-left: 30px;
}

.usage {
 font-style: italic;
}

h1, h2 {
 font-size: 20px;
 margin: 0px
}

.cloze {
 font-weight: bold;
}
'''

    def __init__(self, dict_entry):
        self.dict_entry = dict_entry
        super(AnkiWord, self).__init__(dict_entry.word)

    def question_text(self):
        word = self.dict_entry.word
        dict_entry = self.dict_entry
        header = u'<h1>{}</h1>'.format(word)
        text = header
        for part_of_speech, definitions in dict_entry.iteritems():
            pos_text = u'<h2>{}</h2>'.format(part_of_speech)
            pos_text = HTML.add_div_tag(pos_text, 'part_of_speech')

            text += pos_text

            for definition in definitions:
                description = definition.description
                usages = definition.usages
                description_text = HTML.add_div_tag(description,
                                                    "description")
                text += description_text

                for usage in usages:
                    usage_text = HTML.add_div_tag(u'e.g. ' + usage,
                                                            "usage")
                    text += usage_text


        text = HTML.substitute_clozure(text, word)
        return text

def get_words(input):
    words = []
    for text in input:
        if not '.' in text:
            words.append(text.lower())
        else:
            with open(text, 'r') as file:
                for line in file:
                    words.extend(line.lower().split())
    return words

def get_config_file_path():
    file_name = 'config.ini'
    dir_name = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_name, file_name)

def get_config_file():
    user = 'user settings'
    cards = 'card settings'
    config = SafeConfigParser()
    config.read(get_config_file_path())
    if not config.sections():
        config.add_section(user)
        config.add_section('card settings')
    return config

def get_from_config_or_user(config, section, key, is_int=False, prompt=""):
    if not prompt:
        prompt = key + ': '
    try:
        if is_int:
            value = config.getint(section, key)
        else:
            value = config.get(section, key)
    except:
        value = raw_input(prompt)
        config.set(section, key, value)
    if is_int:
        value = int(value)
    return value

def get_args():
    user = 'user settings'
    cards = 'card settings'
    config = get_config_file()

    # SOMEDAY: Make this a gui
    collection_path = get_from_config_or_user(config,
                                              user,
                                              'collection_path')
    deck_name = get_from_config_or_user(config,
                                        user,
                                        'deck_name')

    prompt = 'num_choices (default is 4): '
    num_choices = get_from_config_or_user(config,
                                          cards,
                                          'num_choices',
                                          is_int=True,
                                          prompt=prompt)

    prompt = 'num_definitions (default is 1): '
    num_definitions = get_from_config_or_user(config,
                                              cards,
                                              'num_definitions',
                                              is_int=True,
                                              prompt=prompt)

    num_parts_of_speech = 5

    with open(get_config_file_path(), 'w') as f:
        config.write(f)

    args = namedtuple('Args',
                      ['collection_path',
                      'deck_name',
                      'num_choices',
                      'num_parts_of_speech',
                      'num_definitions'])
    return args(collection_path,
                deck_name,
                num_choices,
                num_parts_of_speech,
                num_definitions)

def get_words_from_user():
    parser = argparse.ArgumentParser(description=
                                     'Create anki cards from words.')
    parser.add_argument('input', type=str, nargs='+',
        help='List of words or text files to add to anki')
    args = parser.parse_args()
    words = get_words(args.input)

    return words

def get_failed_words_file_path():
    file_name = 'failed_words.txt'
    dir_name = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_name, file_name)

def create_anki_words(words, num_parts_of_speech, num_definitions):
    anki_words = []
    failed_words = []
    for word in words:
        entry = dictionary_entry(word,
                                 num_definitions=num_definitions,
                                 num_parts_of_speech=num_parts_of_speech)
        if not entry:
            failed_words.append(word)
        else:
            anki_words.append(AnkiWord(entry))

    new_word_failures = []
    failed_words_file_path = get_failed_words_file_path()
    if os.path.isfile(failed_words_file_path):
        with open(failed_words_file_path, 'r') as file:
            words_from_file = file.readlines()
            # Strip newline
            words_from_file = [word.strip() for word in words_from_file]
            for word in failed_words:
                if not word in words_from_file:
                    new_word_failures.append(word)
    else:
        new_word_failures = failed_words
    if new_word_failures:
        print 'The following words were not found:'
        print ' '.join(new_word_failures)
        print 'Saving failed words at: {}'.format(failed_words_file_path)
        with open(failed_words_file_path, 'a') as file:
            file.writelines("\n".join(new_word_failures))
            file.write("\n")

    if not anki_words:
        print 'No words found!'
        sys.exit()

    return anki_words

def main():
    words = get_words_from_user()
    args = get_args()
    collection_path = args.collection_path
    deck_name = args.deck_name
    num_choices = args.num_choices
    num_parts_of_speech = args.num_parts_of_speech
    num_definitions = args.num_definitions

    anki_words = create_anki_words(words, num_parts_of_speech,
                                   num_definitions)

    create_cards(anki_words, deck_name, collection_path, num_choices)

if __name__ == '__main__':
    main()
