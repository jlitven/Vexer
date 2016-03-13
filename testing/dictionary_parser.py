'''
Searches for a word and prints a nicely formatted definition.
'''

import sys, re
sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC')
from DictionaryServices import DCSCopyTextDefinition
from Wrappers import DictionaryEntry, Definition

def add_period(string):
    if not string[-1] == '.':
        return string + '.'
    else:
        return string

def create_dictionary_entry(result,
                            num_definitions,
                            num_parts_of_speech):
    '''Create a dictionary entry from a dictionary lookup'''

    symbol = u'\u25b6'
    capital_words = ['PHRASES', 'DERIVATIVES', 'ORIGIN']

    # Create separator regex
    separator = '(' + '|'.join(capital_words + [symbol]) + ')'
    regex = separator + r'(.*?)' + separator
    separated_text = re.split(regex, result)

    # Get parts of speech text
    parts_of_speech_text = []
    for index, text in enumerate(separated_text):
        if symbol in text:
            parts_of_speech_text.append(separated_text[index+1])

    dict_entry = DictionaryEntry()
    for text in parts_of_speech_text:

        # Split the text by numbers, otherwise by first word
        split_text = re.split(r' \d ', text)
        if len(split_text) == 1:
            split_text = text.split(' ', 1)

        part_of_speech = split_text[0]

        for definitions in split_text[1:]:

            # Only grab first definition
            dot = u'\u2022'
            dot_index = definitions.find(dot)
            definition_text = definitions[:dot_index]
            colon_index = definition_text.find(':')
            description = definition_text[:colon_index].strip()
            description = add_period(description)

            usages = []
            if colon_index > 0:
                usages = definition_text[colon_index+1:].split('|')
                usages = [add_period(usage.strip())
                          for usage in usages]

            definition = Definition(description, usages)
            dict_entry.add_definition(part_of_speech, definition)
            if len(dict_entry[part_of_speech]) == num_definitions:
                break
        if len(dict_entry.items()) == num_parts_of_speech:
            break
    return dict_entry

def dictionary_entry(word, num_definitions=1, num_parts_of_speech=1):
    '''Returns a dictonary entry of the word'''
    word_range = (0, len(word))
    dictionary_result = DCSCopyTextDefinition(None, word, word_range)
    if not dictionary_result:
        print "{} not found in Dictionary.".format(word)
    else:
        return create_dictionary_entry(dictionary_result,
                                       num_definitions,
                                       num_parts_of_speech)

def main():
    try:
        word = sys.argv[1]
    except IndexErro:
        print 'You did not enter a word to look up.'
        sys.exit()

    print dictionary_entry(word, 1, 10)

if __name__ == '__main__':
    main()
