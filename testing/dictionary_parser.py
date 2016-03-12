'''Searches for a word and prints a nicely formatted definition'''

import sys
sys.path.append('/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC')
from DictionaryServices import DCSCopyTextDefinition

def format_dictionary_definition(result):
    '''Create a formatted definition from the dictionary lookup'''
    return result

def word_definition(word):
    word_range = (0, len(word))
    dictionary_result = DCSCopyTextDefinition(None, word, word_range)
    if not dictionary_result:
        print "{} not found in Dictionary.".format(word)
    else:
        return format_dictionary_definition(dictionary_result)

def main():
    try:
        word = sys.argv[1]
    except IndexErro:
        print 'You did not enter a word to look up.'
        sys.exit()

    print word_definition(word)

if __name__ == '__main__':
    main()
