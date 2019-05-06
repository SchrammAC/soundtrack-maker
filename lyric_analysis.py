# -*- coding: utf-8 -*-
"""
Created on Mon May  6 06:58:45 2019
What does this all mean?
@author: night
"""
import pandas as pd
import re

import numpy as np
from wordcloud import WordCloud, STOPWORDS

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2

import matplotlib.pyplot as plt

dataFilename = 'mini_lyricset.csv'
song_info = pd.read_csv(dataFilename,encoding = "ISO-8859-1")


def clean_lyrics(lyr):
    flat_list = []
    for song in lyr:
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
    return(flat_list)
    

rock_lyrics = []
hiphop_lyrics = []
country_lyrics = []

raw_rock_lyrics = song_info.loc[song_info.Genre == 'rock'].loc[:,'Lyrics']
raw_hiphop_lyrics = song_info.loc[song_info.Genre == 'hiphop'].loc[:,'Lyrics']
raw_country_lyrics = song_info.loc[song_info.Genre == 'country'].loc[:,'Lyrics']

clean_rock = clean_lyrics(raw_rock_lyrics)
clean_hiphop = clean_lyrics(raw_hiphop_lyrics)
clean_country = clean_lyrics(raw_country_lyrics)

total_vocab = clean_rock+clean_hiphop+clean_country

rock_text = " ".join(word for word in clean_rock)
hiphop_text = " ".join(word for word in clean_hiphop)
country_text = " ".join(word for word in clean_country)

stopwords = set(STOPWORDS)
stopwords.update(["chorus","verse","oh",'outro','know','yeah'])


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


tfidf = TfidfVectorizer(sublinear_tf=True, min_df=3, norm='l2', encoding='latin-1', ngram_range=(1,2), stop_words='english')
features = tfidf.fit_transform([rock_text,hiphop_text, country_text]).toarray()
labels = ['rock', 'hiphop', 'country']
features.shape

N = 2
for i in range(0,3):
  features_chi2 = chi2(features, i)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
  print("# '{}':".format(labels[i]))
  print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
  print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))