##cosine similarity of books based on series,author and annotation

import csv
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import math
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#import threading


#function to remove stopwords
def annotation_to_words(raw_ann):
    letters_only=re.sub("[^a-zA-Z]"," ",raw_ann)
    #convert to lower case and split into individual words
    lower_case=letters_only.lower()
    words=lower_case.split()
    #remove stopwords
    stops=set(stopwords.words('english'))
    words_nostop=[w for w in words if not w in stops]
    #join the words back into a sentence
    return("  ".join(words_nostop))

data=pd.read_csv('book.csv')
data.columns=['','ISBN','Title','Series','Author','PubDate','Language','Bisac','Audience','Annotation']
data.drop(['','Title','PubDate', 'Language', 'Bisac', 'Audience'],axis=1,inplace=True)

#handling missing values
data.Annotation = data.Annotation.fillna('')
data.Series = data.Series.fillna('')
data.Author = data.Author.fillna('')

num=data['Annotation'].size
#print num

#removal of stop words from annotation data
modified_annotation=[]
for i in range(0,num):
    ann= annotation_to_words(data['Annotation'][i])
    modified_annotation.append(annotation_to_words(ann))
print "Removed stopwords"

#create tf-idf for annotation only
sklearn_tfidf = TfidfVectorizer(max_features=20000)
tf_idf_matrix = sklearn_tfidf.fit_transform(modified_annotation)
#print(tf_idf_matrix.shape)

#create vector representations of Series and Author data
vectorizer=CountVectorizer()
series_mat=vectorizer.fit_transform(data['Series'])
#print (series_mat.shape)
author_mat=vectorizer.fit_transform(data['Author'])
#print (author_mat.shape)

#calculate similarity for series
simiseries=cosine_similarity(series_mat)
#print(simiseries.shape)

#calculate similarity for annotation
annsim=cosine_similarity(tf_idf_matrix)
#print(annsim.shape)

#calculate similarity for author
simiauthor=cosine_similarity(author_mat)
#print(simiauthor.shape)

#create a data frame to store result
df = pd.DataFrame(columns=['ISBN1', 'ISBN2', 'SeriesSimilarity','AuthorSimilarity', 'AnnotationSimilarity'])

#appending data to a data frame
for i in range(100):
    for j in range(i+1,100):
        
        df = df.append({'ISBN1':data['ISBN'][i],'ISBN2':data['ISBN'][j],'SeriesSimilarity':simiseries[i][j],'AuthorSimilarity': simiauthor[i][j],'AnnotationSimilarity':annsim[i][j]}, ignore_index=True)

#inserting data to a csv file
df.to_csv('similarity.csv')
print "Printed file"

#inserting data into a mongodb collection
import pymongo
from pymongo import MongoClient
mng_client = MongoClient('localhost', 27017)
# Connection to the database
db = mng_client.similarity
# Connection to the collection
collection = db.cosine
collection.insert_many(df.to_dict('records'))

print "Program ends!"
