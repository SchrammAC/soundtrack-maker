# -*- coding: utf-8 -*-
"""
Created on Mon May  6 06:58:45 2019
Initial build of genre prediction model.
Parses 

@author: night
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import NearestNeighbors
from joblib import load

dataFilename = 'trigenre-lyrics-190519-dupremoved.csv'
song_info = pd.read_csv(dataFilename,encoding = "ISO-8859-1")


raw_rock_lyrics = song_info.loc[song_info.genre == 'rock'].loc[:,'lyrics']
raw_hiphop_lyrics = song_info.loc[song_info.genre == 'hip-hop'].loc[:,'lyrics']
raw_country_lyrics = song_info.loc[song_info.genre == 'country'].loc[:,'lyrics']

count_vect = CountVectorizer()
count_matrix = count_vect.fit_transform(song_info.lyrics)
clf = load('models/genre-class.joblib')
X_train, X_test, y_train, y_test = train_test_split(song_info['lyrics'], song_info['genre'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)

query_name = 'forrest gump'
mediaFilename = 'media-descriptors.csv'
media_info = pd.read_csv(mediaFilename,encoding = "ISO-8859-1")
query_str = media_info.loc[media_info.name == query_name].iloc[0]['words']
#query_str = "The world is falling apart. Four diseases are sweeping the planet and your team is on the front lines. Worse yet, one disease has shown signs that it may become resistant to any treatment."
print(query_name)
print(query_str)
print(clf.predict_proba(count_vect.transform([query_str])))
best_genre = clf.predict(count_vect.transform([query_str]))
print(best_genre)


#Define the TFIDF vectorizer that will be used to process the data
tfidf_vectorizer = TfidfVectorizer()
#Apply this vectorizer to the genre dataset to create normalized vectors
lyrics_plus=song_info.loc[:,['lyrics']][song_info.genre==best_genre[0]]
artist_index=song_info.loc[:,['artist','song']][song_info.genre==best_genre[0]]
#Add query to dataframe
next_num = lyrics_plus.index[-1]+1
lyrics_plus = lyrics_plus.append(pd.DataFrame({'lyrics':query_str},index=[next_num]))
tfidf_matrix = tfidf_vectorizer.fit_transform(lyrics_plus.lyrics)

#Get the features of genre + query
features = tfidf_vectorizer.get_feature_names() 

nbrs = NearestNeighbors(n_neighbors=10).fit(tfidf_matrix)

def get_closest_neighs(t_str,art_index):
    row = lyrics_plus.index.get_loc(t_str)
    distances, indices = nbrs.kneighbors(tfidf_matrix.getrow(row))
    artist_similar = pd.Series(indices.flatten()[1:]).map(art_index.reset_index()['artist'])
    song_similar = pd.Series(indices.flatten()[1:]).map(art_index.reset_index()['song'])
    result = pd.DataFrame({'artist':artist_similar, 'name':song_similar})
    return result

print( get_closest_neighs(next_num,artist_index))
