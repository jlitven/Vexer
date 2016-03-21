#!/usr/local/bin/python

'''
Wrapper objects for mac osx dictionary entries.
'''
from collections import defaultdict
import pdb

class DictionaryEntry(defaultdict):
    '''
    Wrapper for a dictionary entry in mac osx.
    '''
    def __init__(self, word):
        super(DictionaryEntry, self).__init__(list)
        self.word = word

    def add_definition(self, part_of_speech, definition):
        self[part_of_speech].append(definition)

    def __str__(self):
        string = self.word + u'\n'
        for part_of_speech, definitions in self.iteritems():
            string += part_of_speech + u'\n'
            for definition in definitions:
                string += definition.__str__()
            string += u'\n'
        return string

class Definition(object):
    '''
    Wrapper for a definition, which consists of a description and usages.
    '''
    def __init__(self, description, usages):
        self.description = description
        self.usages = usages

    def __str__(self):
        description_string = self.description
        usage_string = u'\n'.join(self.usages)
        definition = u'defn:\n{}\nusage:\n{}\n'.format(description_string, usage_string)
        return definition
