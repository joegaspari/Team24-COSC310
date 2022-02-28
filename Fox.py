import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('FOX_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

#FOX.py is responsible for:
#
#
#

#When a user enters a sentence through the UI we first must clean the sentence as jargon is most often used by humans
def clean( sent ):
    '''
    clean will take the sentence and tokenize each of the words. It will also send each character to lower case and then lemmatize the word to find its root
    
    Returns: A list of cleaned words

    '''
    sent_word = nltk.word_tokenize(sent)
    sent_word = [lemmatizer.lemmatize(word.lower()) for word in sent_word]
    return sent_word


#We want to assign a positionality to each of the words found within the sentence inputed by the user. Thus we create a bag of words matrix that will mark the position of each word.

def bag_words( sent, words, show_details=True):
    #send our sentence to be cleaned by the method clean
    sentW = clean(sent)
    
    #we then create an array of zeros that is equal length to the number of words in the sentence
    bag = [0] * len(words)
    
    for w in sentW:
        for i, s in enumerate(words):
            if s == w:
                #if the words match then we mark this position as 1 within the matrix
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))


#We now can use the word positioning and our model generated in chat.py to predict the class label of the statement made by the user

def predict_label( sent, model):
    
    #build our word position matrix 
    mat = bag_words( sent, words, show_details=False)
    
    #modelres will store the prediction, we want to identify a threshold from which predictions should be eliminated from consideration
    ER_Thresh = 0.25
    modelres = model.predict(np.array([mat]))[0]
    
    results = [[i,r] for i,r in enumerate(modelres) if r>ER_Thresh]
    # sort by highest probability 
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    
    #Return list now contains a sorted set of intents based on their probability score, the highest score will sit at the front of the array
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list



#We now need to extract the response from the intent file

def getResponse( ints, jFile):
    '''
    Getresponse : takes (ints) produced by the model prediction and the json file holding the patterns and responses as arguments
    '''
    #we want to capture the class tag from which the has the highest probability of being the type of response required 
    tag = ints[0]['intent']
    list_intents = jFile['intents']
    for i in list_intents:
        #once we find a tag match we can extract a random response from the json file to send to the user
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
        
    return result


def FOX_response(msg):
    '''
    FOX_response takes the user message and predicts the response class, it then uses the class tag to get a response
    
    Returns: Response 
    '''
    prediction = predict_label( msg, model)
    results = getResponse(prediction, intents)
    return results