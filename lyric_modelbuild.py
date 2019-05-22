# -*- coding: utf-8 -*-
"""
Created on Mon May  6 06:58:45 2019
Initial build of genre prediction model.
Parses 

@author: night
"""
import pandas as pd
import re

import numpy as np
from wordcloud import WordCloud, STOPWORDS

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

import matplotlib.pyplot as plt

from joblib import dump, load

dataFilename = 'trigenre-lyrics-190519-dupremoved.csv'
song_info = pd.read_csv(dataFilename,encoding = "ISO-8859-1")


def clean_genre(lyr):
    flat_list = []
    for song in lyr:
        new_song= []
        song_list = song.replace('-', ' ').split()
        for word in song_list:
            if word.islower():
                r = word
            else:
                r=re.split('([A-Z][a-z]+)', word)   
#                r=re.split('-',r)
            new_song.append(r)
            
        for sublist in new_song:
            if isinstance(sublist, str):
                flat_list.append(sublist)
            else:
                for item in sublist:
                    flat_list.append(item)
    return(flat_list)
    
def clean_songs(song):
    flat_list = []
    new_song= []
    song_list = song.split()
    for word in song_list:
        if word.islower():
            r=word
        else:
            r=re.split('([A-Z][a-z]+)', word)            
        new_song.append(r)
        
    for sublist in new_song:
        if isinstance(sublist, str):
            flat_list.append(sublist)
        else:
            for item in sublist:
                flat_list.append(item)
    song_text = " ".join(word for word in flat_list)
    return(song_text)
    

rock_lyrics = []
hiphop_lyrics = []
country_lyrics = []

raw_rock_lyrics = song_info.loc[song_info.genre == 'rock'].loc[:,'lyrics']
raw_hiphop_lyrics = song_info.loc[song_info.genre == 'hip-hop'].loc[:,'lyrics']
raw_country_lyrics = song_info.loc[song_info.genre == 'country'].loc[:,'lyrics']

for song in song_info.lyrics:
    clean_text = clean_songs(song)
    song = clean_text

clean_rock = clean_genre(raw_rock_lyrics)
clean_hiphop = clean_genre(raw_hiphop_lyrics)
clean_country = clean_genre(raw_country_lyrics)

total_vocab = clean_rock+clean_hiphop+clean_country

rock_text = " ".join(word for word in clean_rock)
hiphop_text = " ".join(word for word in clean_hiphop)
country_text = " ".join(word for word in clean_country)

stopwords = set(STOPWORDS)
#remove some words from model that are irrelevant (song structure words)
stopwords.update(["chorus","verse","oh",'outro','know','yeah','intro'])
raw_artistlist = song_info.artist.drop_duplicates()
artist_wordlist = clean_genre(raw_artistlist)
stopwords.update(artist_wordlist)


# Create and generate a word cloud image:
rockcloud = WordCloud(stopwords=stopwords, background_color="white").generate(rock_text)
hopcloud = WordCloud(stopwords=stopwords, background_color="white").generate(hiphop_text)
countrycloud = WordCloud(stopwords=stopwords, background_color="white").generate(country_text)

f, axarr = plt.subplots(3)
axarr[0].imshow(rockcloud, interpolation='bilinear')
axarr[0].axis('off')
axarr[0].set_title('Rock')
axarr[1].imshow(hopcloud, interpolation='bilinear')
axarr[1].axis('off')
axarr[1].set_title('HipHop / R&B')
axarr[2].imshow(countrycloud, interpolation='bilinear')
axarr[2].axis('off')
axarr[2].set_title('Country')
plt.savefig("img/lyric_clouds.png", format="png")


#tfidf = TfidfVectorizer(sublinear_tf=True, min_df=3, norm='l2', encoding='latin-1', ngram_range=(1,2), stop_words='english')
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=3, norm='l2', encoding='latin-1', ngram_range=(1,2), stop_words=stopwords)
features = tfidf.fit_transform([rock_text,hiphop_text, country_text]).toarray()
features.shape

data = [['rock',rock_text],['hiphop',hiphop_text],['country',country_text]]
lyric_df = pd.DataFrame(data, columns = ['genre','lyrics'])
lyric_df['category_id'] = lyric_df['genre'].factorize()[0]
category_id_df = lyric_df[['genre', 'category_id']].sort_values('category_id')
category_to_id = dict(category_id_df.values)
labels = lyric_df.category_id

N = 4
for genre, category_id in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == category_id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
  print("# '{}':".format(genre))
  print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
  print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))
  

X_train, X_test, y_train, y_test = train_test_split(song_info['lyrics'], song_info['genre'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = MultinomialNB().fit(X_train_tfidf, y_train)

test_str = "TO THE RED COUNTRY and part of the gray country of Oklahoma, the last rains came gently, and they did not cut the scarred earth."
print(test_str)
print(clf.predict(count_vect.transform([test_str])))
print(clf.predict_proba(count_vect.transform([test_str])))

dump(clf, 'models/genre-class.joblib')

unique_artist = song_info.artist.unique()
art_list = []; rockpred = []; hiphoppred=[]; countrypred = [];realgenre = [];
for artist in unique_artist: #get predictions for all artists
    raw_art_lyrics = song_info.loc[song_info.artist == artist].loc[:,'lyrics']
    genre = song_info.loc[song_info.artist == artist].genre.iloc[0]
    clean_art = clean_genre(raw_art_lyrics)
    art_text = " ".join(word for word in clean_art)
    [c,h,r] = clf.predict_proba(count_vect.transform([art_text]))[0]
    art_list.append(artist); rockpred.append(r), countrypred.append(c); hiphoppred.append(h); realgenre.append(genre)
    
pred_data = {'artist':art_list, 'genre':realgenre, 'rock':rockpred, 'hiphop':hiphoppred, 'country':countrypred}
pred_data = pd.DataFrame.from_dict(pred_data)

pred_data.to_csv('classifications/artist_genre_class.csv', index=False, header=True)

art_list = []; song_list = []; rockpred = []; hiphoppred=[]; countrypred = [];realgenre = [];
for song in song_info.lyrics: #get predictions for all artists
    genre = song_info.loc[song_info.lyrics == song].genre.iloc[0]
    artist = song_info.loc[song_info.lyrics == song].artist.iloc[0]
    song_name = song_info.loc[song_info.lyrics == song].song.iloc[0]
#    clean_song = clean_genre(song)
#    song_text = " ".join(word for word in clean_song)
    [c,h,r] = clf.predict_proba(count_vect.transform([song]))[0]
    art_list.append(artist); song_list.append(song_name), rockpred.append(r), countrypred.append(c); hiphoppred.append(h); realgenre.append(genre)
    
pred_data = {'artist':art_list, 'song':song_list, 'genre':realgenre, 'rock':rockpred, 'hiphop':hiphoppred, 'country':countrypred}
pred_data = pd.DataFrame.from_dict(pred_data)

pred_data.to_csv('classifications/song_genre_class.csv', index=False, header=True)


mediaFilename = 'media-descriptors.csv'
media_info = pd.read_csv(mediaFilename,encoding = "ISO-8859-1")
name_list = []; rockpred = []; hiphoppred=[]; countrypred = [];
for item in media_info.name: #get predictions for all media items
    raw_descript = media_info.loc[media_info.name == item].words
    media_type = media_info.loc[media_info.name == item].type.iloc[0]
    clean_descript = clean_genre(raw_descript)
    media_text = " ".join(word for word in clean_descript)
    [c,h,r] = clf.predict_proba(count_vect.transform([media_text]))[0]
    name_list.append(item); rockpred.append(r), countrypred.append(c); hiphoppred.append(h)
    
pred_data = {'name':name_list, 'rock':rockpred, 'hiphop':hiphoppred, 'country':countrypred}
pred_data = pd.DataFrame.from_dict(pred_data)

pred_data.to_csv('classifications/media_class.csv', index=False, header=True)