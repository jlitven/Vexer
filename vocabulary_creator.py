'''
Script to create anki vocabulary cards.
'''
from card_creator import create_cards, AnkiObject, HTML
from dictionary_parser import dictionary_entry
import argparse, logging, re
logging.basicConfig(level=logging.DEBUG)

# SOMEDAY: Fix vocab definitions for 'groovy', 'party', 'pumpkin'

class AnkiWord(AnkiObject):

    '''
    Stores vocabulary information.
    '''
    tag_name = 'vocabulary'
    model_name = 'Vocabulary'

    styling_text = '''
.card {
 font-family: baskerville;
 font-size: 20px;
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

h2 {
 font-size: 25px;
}

.answer, .cloze {
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
                text += description_text + u'<br>'

                for usage in usages:
                    usage_text = HTML.add_div_tag(u'e.g.' + usage,
                                                            "usage")
                    text += usage_text + u'<br>'


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

def get_args_from_user():
    # HACK: fix this quick hack
    default_path = '/Users/alexanderlitven/Documents/Anki/User 1/' + \
                    'collection.anki2'
    default_deck = 'vocabulary'
    parser = argparse.ArgumentParser(description=
                                     'Create anki cards from words.')
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
        entry = dictionary_entry(word, num_definitions=1,
                                 num_parts_of_speech=5)
        anki_words.append(AnkiWord(entry))

    return anki_words
def main():

    args = get_args_from_user()
    words = args.words
    collection_path = args.collection_path
    deck_name = args.deck_name

    anki_words = create_anki_words(words)
    create_cards(anki_words, deck_name, collection_path)
if __name__ == '__main__':
    main()
