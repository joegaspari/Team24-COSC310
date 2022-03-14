import rasa_nlu
import rasa_core
import spacy

from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

training_data = load_data("data/nlu.yml")
trainer = Trainer(config.load("config.yml"))