'''
Script to create anki vocabulary cards.
'''
from card_creator import create_cards, AnkiObject
from dictionary_parser import dictionary_entry
import argparse, logging, re
logging.basicConfig(level=logging.DEBUG)

class AnkiWord(AnkiObject):

    '''
    Stores vocabulary information.
    '''
    _tag_name = 'vocabulary'

    def __init__(self, dict_entry):
        self.dict_entry = dict_entry
        super(AnkiWord, self).__init__(dict_entry.word)

    def question_text(self):
        # TODO: Add closure and remove word in usage
        word = self.dict_entry.word
        text = self.dict_entry.__str__()
        text = re.sub(word, '{{c1::' + word + '}}', text.decode('utf-8'))
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

def get_args_from_user():
    # SOMEDAY: fix this quick hack
    default_path = '/Users/alexanderlitven/Documents/Anki/User 1/collection.anki2'
    default_deck = 'Knowledge'
    parser = argparse.ArgumentParser(description='Create anki cards from words.')
    parser.add_argument('input', type=str, nargs='+',
        help='List of words or text files to add to anki')
    parser.add_argument('-p', '--collection_path', type=str,
        help='Path to the anki collection',
        default=default_path)
    parser.add_argument('-d', '--deck_name', type=str,
        default=default_deck, help='Name of the deck to add the cards to')
    parser.add_argument('-n', '--num_choices', type=int, default=4,
        choices=range(2,6),
        help='Number of definition choices in a card (default is 4)')

    args = parser.parse_args()
    if not args.collection_path:
        args.collection_path = raw_input('collection path: ')
    if not args.deck_name:
        args.deck_name = raw_input('deck name: ')

    args.words = get_words(args.input)

    return args

def create_anki_words(words):
    anki_words = []
    for word in words:
        entry = dictionary_entry(word,1,3)
        anki_words.append(AnkiWord(entry))

    return anki_words
def main():

    # TODO: Get words from command line or file
    args = get_args_from_user()
    words = args.words
    collection_path = args.collection_path
    deck_name = args.deck_name

    # TODO: Create anki words
    anki_words = create_anki_words(words)

    for word in anki_words:
        logging.debug(word.question_text())

    # TODO: Create anki words
    create_cards(anki_words, deck_name, collection_path)

main()
