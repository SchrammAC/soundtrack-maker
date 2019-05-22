# -*- coding: utf-8 -*-
"""
Created on Mon May  6 06:58:45 2019
What does this all mean?
@author: night
"""
import pandas as pd
import re

from sklearn.feature_extraction.text import CountVectorizer
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
cv = CountVectorizer(stop_words='english')
data=cv.fit_transform(total_vocab)
vocab = cv.get_feature_names()
dist = np.sum(data,axis=0)
freq = dist / (np.sum(dist))

#Get most disproportionate titles for each cluster
cv0 = CountVectorizer(vocabulary=cv.vocabulary_,stop_words='english')
data0 = cv0.fit_transform(clean_rock)
dist_0 = np.sum(data0,axis=0)
freq_0 = dist_0 / (np.sum(dist_0))
rel_freq_0 = np.array(freq_0 - freq)
top10_0 = rel_freq_0.argsort()[0][-10:]

cv1 = CountVectorizer(vocabulary=cv.vocabulary_,stop_words='english')
data1 = cv1.fit_transform(clean_hiphop)
dist_1 = np.sum(data1,axis=0)
freq_1 = dist_1 / (np.sum(dist_1))
rel_freq_1 = np.array(freq_1 - freq)
top10_1 = rel_freq_1.argsort()[0][-10:]

cv2 = CountVectorizer(vocabulary=cv.vocabulary_,stop_words='english')
data2 = cv2.fit_transform(clean_country)
dist_2 = np.sum(data2,axis=0)
freq_2 = dist_2 / (np.sum(dist_2))
rel_freq_2 = np.array(freq_2 - freq)
top10_2 = rel_freq_2.argsort()[0][-10:]

#print('Most overrepresented words in rock:')
#for ind in top10_0:
#    print(vocab[ind])
#    
#print('')    
#print('Most overrepresented words in Hip Hop / R&B:')
#for ind in top10_1:
#    print(vocab[ind])
#
#print('')    
#print('Most overrepresented words in Country:')
#for ind in top10_2:
#    print(vocab[ind])

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
for Product, category_id in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == category_id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
  print("# '{}':".format(Product))
  print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
  print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))