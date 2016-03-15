#!/usr/bin/env python

'''
Anki card creator.
'''
import os, pdb, csv, random, re
from anki import Collection
from anki.importing import TextImporter

class AnkiObject(object):

    '''
    Stores information used to create an anki card.
    '''

    # TODO: Make this abstract.
    tag_name = ''

    def __init__(self, answer):
        self.answer = answer

    def question_text():
        # TODO: make this an abstract method
        pass

def get_delimiter():
    return '\t'

def get_question_index():
    return 0

def get_card_ids(collection, tag_name):
    ids = collection.findCards('tag:{}'.format(tag_name))
    return ids

def html_answer(text):
    beginning_tag = '<font color="blue"><b>'
    ending_tag = '</b></font>'
    return unicode(beginning_tag + text + ending_tag).encode('utf-8')

def sample_answers_from_collection(collection, tag_name, num_samples):

    ids = get_card_ids(collection, tag_name)
    error_msg = "Need at least {} in collection.".format(num_samples)
    assert len(ids) >= num_samples, error_msg
    sampled_ids = random.sample(ids, num_samples)

    samples = []
    for id in sampled_ids:
        card = collection.getCard(id)
        note = card.note()
        question_text = note.fields[get_question_index()]
        answer_regex = re.compile(r'{{c1::(.*?)}}')
        match = answer_regex.search(question_text)
        answer = match.group(1)
        samples.append(answer)
    return samples

def sample_answers_from_objects(anki_objects, num_samples):

    assert len(anki_objects) >= num_samples, "Not enough samples."

    sample_objects = random.sample(anki_objects,
                                         num_samples)
    samples = map(lambda anki_object : anki_object.answer,
                  sample_objects)
    return samples

def create_csv_row(anki_object, anki_objects, tag_name, collection,
                   num_choices=4):

    # TODO: understand why this works
    question = unicode(anki_object.question_text()).encode('utf-8')
    answer = anki_object.answer

    other_objects = list(anki_objects)
    other_objects.remove(anki_object)

    num_from_objects = min(num_choices - 1, len(other_objects))
    object_samples = sample_answers_from_objects(other_objects,
                                                 num_from_objects)

    num_from_collection = num_choices - 1 - num_from_objects
    collection_samples = sample_answers_from_collection(collection,
                                                 tag_name,
                                                 num_from_collection)

    choices = object_samples + collection_samples
    choices += [anki_object.answer]
    choices = [unicode(choice).encode('utf-8') for choice in choices]
    random.shuffle(choices)
    letters = 'abcde'
    choices_text = ['{}) {}'.format(letter, choice)
                for (letter, choice) in zip(letters, choices)]
    choices_text = '<br>'.join(choices_text)

    answer_text = re.sub(answer, html_answer(answer), choices_text)

    row = [question, choices_text, answer_text]
    return row

def write_to_csv(anki_objects, tag_name, file_path, collection):
    # TODO: Make sure there are enough anki objects

    with open(file_path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=get_delimiter())

        for anki_object in anki_objects:
            row = create_csv_row(anki_object, anki_objects,
                                 tag_name, collection)
            writer.writerow(row)

def set_model(model_name, deck_name, collection):
    did = collection.decks.id(deck_name)
    collection.decks.select(did)
    # TODO: Create model if doesn't exist
    model = collection.models.byName("Multiple Choice")
    deck = collection.decks.get(did)
    collection.decks.save(deck)

def run_importer(file_path, tag_name, deck_name, collection):
    ti = TextImporter(collection, file_path)
    ti.delimiter = get_delimiter()
    ti.allowHTML = True
    ti.tagsToAdd = [tag_name]
    ti.initMapping()
    ti.run()

    # BUGFIX: anki doesn't add to selected deck
    did = collection.decks.id(deck_name)
    num_cards_added = ti.total
    ids = get_card_ids(collection, tag_name)
    ids = sorted(ids, reverse=True)
    for id in ids[:num_cards_added]:
        collection.db.execute("update cards set did = ? where id = ?",
                              did, id)

def import_to_anki(file_path, tag_name, deck_name, collection):

    assert deck_name in collection.decks.allNames(), "No deck named " + deck_name

    set_model("Cloze", deck_name, collection)
    run_importer(file_path, tag_name, deck_name, collection)

def get_csv_file_path():
    file_name = 'temp.csv'
    # TODO: Fix hack
    dir_name = ('/Users/alexanderlitven/Projects/'
                'vocabulary_flash_cards_creator')
    return os.path.join(dir_name, file_name)

def get_collection(collection_path):
    assert os.path.exists(collection_path), "No collection found."
    return Collection(collection_path)

def create_cards(anki_objects, deck_name, collection_path):

    collection = get_collection(collection_path)
    csv_file_path = get_csv_file_path()
    tag_name = anki_objects[0].tag_name

    write_to_csv(anki_objects, tag_name, csv_file_path, collection)

    import_to_anki(csv_file_path, tag_name, deck_name, collection)

    collection.close()

