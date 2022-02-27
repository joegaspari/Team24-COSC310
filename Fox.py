import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))



#When a user enters a sentence through the UI we first must clean the sentence as jargon is most often used by humans
def clean( sent ):
    '''
    clean will take the sentence and tokenize each of the words. It will also send each character to lower case and then lemmatize the word to find its root
    
    Returns: A list of cleaned words

    '''
    sent_word = nltk.word_tokenize(sent)
    sent_word = [lemmatizer.lemmatize(word.lower()) for word in sent_word]
    return sent_word


#We want to assign a positionality to each of the words found within the sentence inputed by the user