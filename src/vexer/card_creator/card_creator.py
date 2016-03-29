#! /usr/bin/python

'''
Anki card creator.
'''
import os, pdb, csv, random, re, sys
from anki import Collection
from anki.importing import TextImporter
from abc import ABCMeta, abstractmethod, abstractproperty

class HTML(object):

    '''
    Helper methods for creating HTML styling.
    '''
    @staticmethod
    def add_div_tag(text, class_name=None, id_name=None):
        return HTML.add_tag(text, 'div', class_name, id_name)

    @staticmethod
    def add_span_tag(text, class_name=None, id_name=None):
        return HTML.add_tag(text, 'span', class_name, id_name)

    @staticmethod
    def add_tag(text, tag_name, class_name=None, id_name=None):
        class_text = u''
        id_text = u''
        if class_name:
            class_text = u'class="{}"'.format(class_name)
        if id_name:
            id_text = u'id="{}"'.format(id_name)
        return u'<{} {} {}> {} </{}>'.format(tag_name,
                                            class_text,
                                            id_text,
                                            text,
                                            tag_name)
    @staticmethod
    def substitute_clozure(text, word):
        text = re.sub(word, u'{{{{c1::{}}}}}'.format(word), text, flags=re.I)
        return text


class AnkiObject(object):

    '''
    Stores information used to create an anki card.
    '''
    __metaclass__  = ABCMeta

    @abstractproperty
    def tag_name(self):
        pass

    @abstractproperty
    def model_name(self):
        pass

    def __init__(self, answer):
        self.answer = answer

    @abstractmethod
    def question_text(self):
        pass

    @abstractmethod
    def styling_text(self):
        pass

def get_delimiter():
    return '\t'

def get_question_index():
    return 1

def get_answer_index():
    return 0

def get_card_ids(collection, tag_name):
    ids = collection.findCards('tag:{}'.format(tag_name))
    return ids

def get_answers_from_collection(collection, ids):
    answers = []
    for id in ids:
        card = collection.getCard(id)
        note = card.note()
        answer = note.fields[get_answer_index()]
        answers.append(answer)
    return answers

def get_all_answers_from_collection(collection, tag_name):
    ids = get_card_ids(collection, tag_name)
    return get_answers_from_collection(collection, ids)

def sample_answers_from_collection(collection, tag_name, num_samples):
    ids = get_card_ids(collection, tag_name)
    error_msg = "Need at least {} in collection.".format(num_samples)
    assert len(ids) >= num_samples, error_msg
    sampled_ids = random.sample(ids, num_samples)

    return get_answers_from_collection(collection, sampled_ids)

def sample_answers_from_objects(anki_objects, num_samples):

    assert len(anki_objects) >= num_samples, "Not enough samples."

    sample_objects = random.sample(anki_objects,
                                         num_samples)
    samples = map(lambda anki_object : anki_object.answer,
                  sample_objects)
    return samples

def create_csv_row(anki_object, anki_objects, tag_name, collection,
                   num_choices=4):

    question = anki_object.question_text()
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
    random.shuffle(choices)
    letters = u'abcde'
    choices_text = ['{}) {}'.format(letter, choice)
                for (letter, choice) in zip(letters, choices)]
    choices_text = [HTML.add_div_tag(choice, class_name="choice")
                for choice in choices_text]

    choices_text = u''.join(choices_text)
    answer_text = choices_text
    answer_text = re.sub(answer,
                         u'<b>{}</b>'.format(answer),
                         choices_text)

    row = [answer, question, choices_text, answer_text]
    return row

def write_to_csv(anki_objects, tag_name, file_path, collection,
                 num_choices):

    with open(file_path, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=get_delimiter())

        for anki_object in anki_objects:
            answer = anki_object.answer
            if answer in get_all_answers_from_collection(collection,
                                                         tag_name):
                print '"{}" already in collection. Skipping.'.format(answer)
                continue
            row = create_csv_row(anki_object, anki_objects,
                                 tag_name, collection, num_choices)
            # convert back to bytes
            row = [cell.encode('utf-8') for cell in row]
            writer.writerow(row)

def set_model(model_name, deck_name, collection):
    did = collection.decks.id(deck_name)
    collection.decks.select(did)
    model = collection.models.byName(model_name)
    deck = collection.decks.get(did)
    deck['mid'] = model['id']
    collection.decks.save(deck)

def create_fields(collection):
    models = collection.models
    field_names = ['Value', 'Question', 'Choices', 'Answers']
    fields = map(lambda field_name:models.newField(field_name),
                 field_names)
    return fields

def create_templates(collection):
    models = collection.models
    template = models.newTemplate(u'Card 1')

    # SOMEDAY: Make fields not hard-coded
    question_text = '{{cloze:Question}}{{Choices}}'
    answer_text = '{{cloze:Question}}{{Answers}}'
    template['qfmt'] = question_text
    template['afmt'] = answer_text
    return [template]

def create_model(anki_object, deck_name, collection):
    model_name = anki_object.model_name
    model = collection.models.byName(model_name)
    if model is None:
        print 'Creating model: {}'.format(model_name)

        models = collection.models
        model = models.new(model_name)
        models.add(model)

        for field in create_fields(collection):
            models.addField(model, field)

        for template in create_templates(collection):
            models.addTemplate(model, template)

        model['css'] = anki_object.styling_text

        collection.models.update(model)

    set_model(model_name, deck_name, collection)


def run_importer(file_path, tag_name, deck_name, collection):
    if not os.stat(file_path).st_size > 0:
        print "Nothing to import!"
        sys.exit()
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

    run_importer(file_path, tag_name, deck_name, collection)

def get_csv_file_path(data_dir):
    file_name = 'import_dump.csv'
    return os.path.join(data_dir, file_name)

def get_collection(collection_path):
    assert os.path.exists(collection_path), "No collection found."
    # BUGFIX: Opening collection changes the cwd.
    cwd = os.getcwd()
    collection = Collection(collection_path)
    os.chdir(cwd)
    return collection

def create_cards(anki_objects, deck_name, collection_path,
                 data_dir, num_choices):

    collection = get_collection(collection_path)
    csv_file_path = get_csv_file_path(data_dir)
    tag_name = anki_objects[0].tag_name

    write_to_csv(anki_objects, tag_name, csv_file_path, collection,
                 num_choices)
    create_model(anki_objects[0], deck_name, collection)
    import_to_anki(csv_file_path, tag_name, deck_name, collection)

    collection.close()

