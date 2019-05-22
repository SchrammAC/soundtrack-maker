# -*- coding: utf-8 -*-
"""
Created on Mon May  6 06:58:45 2019

Remove duplicate songs from scraped lyrics.
First removes straight up duplicates (same artist, title)
Next removes all songs that contain another title from the same artist. (e.g. songtitle kept, songtitle-remix removed)

@author: Anthony Schramm
"""
import pandas as pd

dataFilename = 'trigenre-lyrics-190519.csv'
song_info = pd.read_csv(dataFilename,encoding = "ISO-8859-1")

new_filename = 'trigenre-lyrics-190519-dupremoved.csv'

song_info = song_info.drop_duplicates(subset=['artist', 'song'], keep=False)

unique_artist = song_info.artist.unique()

for artist in unique_artist:
    art_df = song_info[song_info.artist == artist]
    
    #find and remove duplicates from temporary df
    for song in art_df['song']:
        for i in art_df.index:
            if i in art_df.index:
                if ((song in art_df['song'][i]) & (song != art_df['song'][i])):
                    art_df = art_df.drop(i)
    #append to new df / append to new file

    art_df.to_csv(new_filename, mode='a', index=False, header=False)









