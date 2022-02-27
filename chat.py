import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random


#This python file is responsible for loading the 

# our intents file holds all of the predefined patterns and responses that may occur within the conversation
data_file = open('intents.json').read()
intents = json.loads(data_file)


#We begin to iterate through the patterns found in our intents file. These patters will be tokenized into individual words, these words are then added to our words list.
#We also build our list of classes by scraping the class tag from each of the pattern - response blocks

words=[]
classes = []
documents = []
ignore_words = ['?', '!']
    

for intent in jFile['intents']:
    for pattern in jFile['patterns']:
         #We tokenize the words found within the patterns defined in the intents file
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        #add documents in the corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmatize, lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
    
# sort classes
classes = sorted(list(set(classes)))

#We then save the words and classes generated after the cleaning process
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))
    

#Build our training Data
train = []

#We must build an array to store the output of the split
out_E = [0] * len(classes)

for doc in documents:
    # create a bag of words 
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    
    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(out_E)
    output_row[classes.index(doc[1])] = 1
    
    train.append([bag, output_row])
# shuffle our features and turn into np.array
random.shuffle(train)
training = np.array(train)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created, split maintained")

#We now have to create the Keras neural network that will be used to predict the best response based upon the user's messages. The package requires us to build a set of neuron layers that follow a 128, 64 and
# X pattern. Where x is the number of classes that were generated via the intents json file. 
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model 
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('FOX_model.h5', hist)

print("model created")