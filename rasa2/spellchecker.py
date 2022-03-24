from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

from spellchecker import SpellChecker
spell = SpellChecker()

##########################################################################################
# for the spellchecker to work, you must include it in your PYTHONPATH by including the path to the file spellchecker.py
# This allows the config file to acess the python file without having the components of the spellchecker installed in the python folder
###########################################################################################

class CorrectSpelling(Component):

    name = "Spell_checker"
    provides = ["message"]
    requires = ["message"]
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(CorrectSpelling, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Not needed, because the the model is pretrained"""
        pass

    def process(self, message, **kwargs):
        """Retrieve the text message, do spelling correction word by word,
        then append all the words and form the sentence,
        pass it to next component of pipeline"""

        textdata = message.text
        textdata = textdata.split()
        new_message = ' '.join(spell.correction(w) for w in textdata)
        message.text = new_message

    def persist(self, file_name, model_dir):
        """Pass because a pre-trained model is already persisted"""
        pass