#! /usr/bin/python

'''
Script to create anki vocabulary cards.
'''
from card_creator.card_creator import create_cards, AnkiObject, HTML, get_collection
from dictionary_parser import dictionary_entry
from collections import namedtuple
import argparse, logging, re
from ConfigParser import SafeConfigParser
import os, sys, pdb

# SOMEDAY: Fix vocab definitions for 'fiduciary'

class AnkiWord(AnkiObject):

    '''
    Stores vocabulary information.
    '''
    tag_name = 'vocabulary'
    model_name = 'Vocabulary'

    styling_text = '''
.card {
 font-family: baskerville;
 font-size: 25px;
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
 font-size: 30px;
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
                text += '<br>'


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

def get_data_dir():
    dir_name = 'vexer'
    path = os.getenv("HOME")
    dir_path = os.path.join(path, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def get_config_file_path():
    file_name = 'config.ini'
    dir = get_data_dir()
    return os.path.join(dir, file_name)

def get_config_file():
    user = 'user settings'
    cards = 'card settings'
    config = SafeConfigParser()
    config.read(get_config_file_path())
    if not config.sections():
        config.add_section(user)
        config.add_section(cards)
        print 'Creating config file at {}'.format(get_config_file_path())
    return config

# SOMEDAY: Make these functions more beautiful
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

def get_from_config_or_default(config, section, key, default,
                               is_int=False):
    try:
        if is_int:
            value = config.getint(section, key)
        else:
            value = config.get(section, key)
    except:
        print 'Setting {} to {}.'.format(key, default)
        config.set(section, key, str(default))
        value = default
    return value

def get_args():

    user_args = get_args_from_user()

    words = get_words(user_args.input)
    num_choices = user_args.num_choices
    num_definitions = user_args.num_defs

    user = 'user settings'
    cards = 'card settings'
    config = get_config_file()

    # SOMEDAY: Make this a gui
    collection_path = get_from_config_or_user(config,
                                              user,
                                              'collection_path')
    try:
        collection = get_collection(collection_path)
        collection.close()
    except:
        raise
        print 'No collection found at "{}".'.format(collection_path)
        config.remove_option(user, 'collection_path')
        sys.exit()

    deck_name = get_from_config_or_user(config,
                                        user,
                                        'deck_name')

    if not deck_name in collection.decks.allNames():
        print 'No deck named "{}".'.format(deck_name)
        config.remove_option(user, 'deck_name')
        sys.exit()

    num_choices_default = 4
    if not num_choices:
        num_choices = get_from_config_or_default(config,
                                                 cards,
                                                 'num_choices',
                                                 num_choices_default,
                                                 is_int=True)

    num_definitions_default = 1
    if not num_definitions:
        num_definitions = get_from_config_or_default(config,
                                                     cards,
                                                     'num_definitions',
                                                     num_definitions_default,
                                                     is_int=True)

    num_parts_of_speech = 5

    with open(get_config_file_path(), 'w') as f:
        config.write(f)

    args = namedtuple('Args',
                      ['words',
                      'collection_path',
                      'deck_name',
                      'num_choices',
                      'num_parts_of_speech',
                      'num_definitions'])
    return args(words,
                collection_path,
                deck_name,
                num_choices,
                num_parts_of_speech,
                num_definitions)

def get_args_from_user():
    parser = argparse.ArgumentParser(description=
                                     'Create anki cards from words.')
    parser.add_argument('input', type=str, nargs='+',
        help='List of words or text files to add to anki')

    help = 'Number of choices in a card'
    parser.add_argument('-n_c', '--num_choices', type=int,
                        choices=range(2,6),
                        help=help)

    help = 'Number of definitions for each part of speech'
    parser.add_argument('-n_d', '--num_defs', type=int,
                        help=help)

    args = parser.parse_args()

    return args

def get_failed_words_file_path():
    file_name = 'failed_words.txt'
    dir_path = get_data_dir()
    return os.path.join(dir_path, file_name)

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
    args = get_args()
    collection_path = args.collection_path
    deck_name = args.deck_name
    num_choices = args.num_choices
    num_parts_of_speech = args.num_parts_of_speech
    num_definitions = args.num_definitions
    words = args.words

    anki_words = create_anki_words(words, num_parts_of_speech,
                                   num_definitions)

    create_cards(anki_words, deck_name, collection_path,
                 get_data_dir(), num_choices)

if __name__ == '__main__':
    main()
