#! /usr/bin/python

'''
Searches for a word and prints a nicely formatted definition.
'''
import sys, re, pdb
# needed for mac osx dictionary
sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC')
from DictionaryServices import DCSCopyTextDefinition
from dictionary_wrappers import DictionaryEntry, Definition

def add_period(string):
    if not string[-1] == '.':
        return string + '.'
    else:
        return string

def first_word(string):
    return string.split(' ', 1)[0]

def create_dictionary_entry(result,
                            num_definitions,
                            num_parts_of_speech):
    '''
    Create a dictionary entry from a dictionary lookup.
    '''
    word = first_word(result)

    # Remove all pronounciation
    pronounciation_regex = r'|*?|'

    symbol = u'\u25b6'
    capital_words = ['PHRASES', 'DERIVATIVES', 'ORIGIN']

    # Create separator regex
    separator = '(' + '|'.join(capital_words + [symbol]) + ')'
    regex = separator + r'(.*?)' + separator
    separated_text = re.split(regex, result)

    # Get parts of speech text
    parts_of_speech_text = []
    if len(separated_text) == 1:
        # no split occured
        symbol_index = result.find(symbol)
        parts_of_speech_text.append(result[symbol_index+1:])
    else:
        for index, text in enumerate(separated_text):
            if symbol in text:
                parts_of_speech_text.append(separated_text[index+1])

    dict_entry = DictionaryEntry(word)
    for text in parts_of_speech_text:

        part_of_speech = first_word(text)

        # Get rid of () pattern following the part of speech
        bracket_regex = part_of_speech + r' \(.*?\)'
        text = re.sub(bracket_regex, '', text, count=1)

        # Split the text by numbers, otherwise by first word
        split_text = re.split(r' \d ', text)
        if len(split_text) == 1:
            split_text = text.split(' ', 1)

        for definitions in split_text[1:]:

            # Only grab first definition
            dot = u'\u2022'
            dot_index = definitions.find(dot)
            if dot_index > 0:
                definition_text = definitions[:dot_index]
            else:
                definition_text = definitions
            colon_index = definition_text.find(':')
            if colon_index > 0:
                description = definition_text[:colon_index].strip()
            else:
                description = definition_text
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

def raw_entry(word):
    word_range = (0, len(word))
    dictionary_result = DCSCopyTextDefinition(None, word, word_range)
    if not dictionary_result:
        print "{} not found in Dictionary.".format(word)
        return None
    else:
        return dictionary_result

def dictionary_entry(word, num_definitions=1, num_parts_of_speech=3):
    '''Returns a dictonary entry of the word'''
    dictionary_lookup = raw_entry(word)
    if dictionary_lookup:
        return create_dictionary_entry(dictionary_lookup,
                                       num_definitions,
                                       num_parts_of_speech)

def main():
    try:
        word = sys.argv[1]
    except IndexError:
        print 'You did not enter a word to look up.'
        sys.exit()

    print dictionary_entry(word)

if __name__ == '__main__':
    main()
