#  -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 22:14:39 2019

@author: BOSS
"""

from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
# Using TensorFlow backend.
import os
import re     # import regular expression to remove html tag
# Chap 14
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.embeddings import Embedding

def rm_tags(text):
    re_tag = re.compile(r'<[^>]+>')
    return re_tag.sub('', text)
    
def read_files(filetype):
    path = "data/aclImdb/"
    file_list=[]
    positive_path=path + filetype+"/pos/"
    for f in os.listdir(positive_path):
        file_list+=[positive_path+f]
    
    negative_path=path + filetype+ "/neg/"
    for f in os.listdir(negative_path):
        file_list+=[negative_path+f]
            
    print('read',filetype, 'files:',len(file_list))
    all_labels = ([1] * 12500 + [0] * 12500)
    all_texts  = []
    for fi in file_list:
        with open(fi,encoding='utf8') as file_input:
            all_texts += [rm_tags(" ".join(file_input.readlines()))]
    return all_labels,all_texts

# Chap 13.5
y_train,train_text=read_files("train")
y_test,test_text=read_files("test")
token = Tokenizer(num_words = 2000)
token.fit_on_texts(train_text)
print(token.document_count)
# Chap 13.6
x_train_seq = token.texts_to_sequences(train_text)
x_test_seq = token.texts_to_sequences(test_text)
print(train_text[0])
print(x_train_seq[0])

# Chap 13.7
x_train = sequence.pad_sequences(x_train_seq, maxlen = 100)
x_test = sequence.pad_sequences(x_test_seq, maxlen = 100)

# Chap 14.3/14.4
model = Sequential()
model.add(Embedding(output_dim=32,input_dim=2000,input_length=100))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(units=256,activation='relu'))
model.add(Dropout(0.35))
model.add(Dense(units=1,activation='sigmoid'))
# model.summary()

# Chap 14.5
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
train_history = model.fit(x_train, y_train, batch_size=100, epochs=10,
                          verbose=2, validation_split=0.2)



