#!/usr/bin/env python

'''
Anki card creator.
'''
import os, pdb, csv

class AnkiObject(object):

    '''
    Stores information used to create an anki card.
    '''

    # TODO: Make this abstract.
    _tag_name = ''

    def __init__(self, answer):
        self.answer = answer

    def question_text():
        # TODO: make this an abstract method
        pass


def add_to_collection(anki_objects, file_path,
                      collection, delimiter):
    # TODO: Make sure there are enough anki objects

    # TODO: Write to csv
    with open(file_path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)

        for anki_object in anki_objects:
            # TODO: understand why this works
            row = [unicode(anki_object.question_text()).encode('utf-8')]
            writer.writerow(row)

def import_to_anki(file_path, deck_name, collection):
    pass

def get_csv_file_path():
    file_name = 'temp.csv'
    dir_name = ('/Users/alexanderlitven/Projects/'
                'vocabulary_flash_cards_creator')
    return os.path.join(dir_name, file_name)

def create_cards(anki_objects, deck_name, collection_path):

    # TODO: Get the real collection
    collection = None
    csv_file_path = get_csv_file_path()
    delimiter = '\t'

    add_to_collection(anki_objects, csv_file_path,
                      collection, delimiter)

    # TODO: Import to deck
    import_to_anki(csv_file_path, deck_name, collection)

