#!/usr/bin/env python

'''
Wrapper objects for mac osx dictionary entries.
'''
from collections import defaultdict

class DictionaryEntry(defaultdict):
    '''
    Wrapper for a dictionary entry in mac osx
    '''
    def __init__(self):
        super(DictionaryEntry, self).__init__(list)

    def add_definition(self, part_of_speech, definition):
        self[part_of_speech].append(definition)

    def __str__(self):
        # TODO: understand why this works
        string = ""
        for part_of_speech, definitions in self.iteritems():
            string += part_of_speech + '\n'
            for definition in definitions:
                string += definition.__str__().decode('utf-8')
            string += '\n'
        return string.encode('utf-8')

class Definition(object):
    '''
    Wrapper for a definition, which consists of a description and usages.
    '''
    def __init__(self, description, usages):
        self.description = description
        self.usages = usages

    def __str__(self):
        description_string = self.description.encode('utf-8')
        usage_string = '\n'.join(self.usages)
        definition = 'defn:\n{} \nusage:\n{}\n'.format(description_string,
                                                     usage_string)
        return definition
