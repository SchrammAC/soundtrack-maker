# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:22:06 2019

@author: night
"""

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import pandas as pd
import numpy as np

verts = [
   (-0.5, 0.-0.433),  # left, bottom
   (0., 0.433),  # left, top
   (0.5, -0.433),  # right, top
   (-0.5, 0.-0.433),  # right, bottom
]

codes = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY,
]

path = Path(verts, codes)

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(4,2)
f_ax1 = fig.add_subplot(gs[0,0])
f_ax2 = fig.add_subplot(gs[0,1])
f_ax3 = fig.add_subplot(gs[1:,:])
patch = patches.PathPatch(path, facecolor='none', lw=2, alpha = 0.2)
f_ax3.add_patch(patch)
f_ax3.set_xlim(-0.566, 0.566)
f_ax3.set_ylim(-0.7, 0.7)

artist_file = 'classifications/media_class.csv'
artist_fits = pd.read_csv(artist_file,encoding = "ISO-8859-1")

art_xcoord = np.array(artist_fits.rock)*0.5 - np.array(artist_fits.hiphop)*0.5 
art_ycoord = np.array(artist_fits.rock)*-0.433 - np.array(artist_fits.hiphop)*0.433 + np.array(artist_fits.country)*0.433

color = np.zeros((len(art_xcoord),3))
for i in range(0,len(art_xcoord)):
    r = artist_fits.rock[i]
    g = artist_fits.country[i]
    b = artist_fits.hiphop[i]
    color[i,:] = [r, g, b]

f_ax3.scatter(art_xcoord,art_ycoord,c=color)
f_ax3.set_aspect('equal')
f_ax3.axis('off')
f_ax3.set_title('Media Assignments')
f_ax3.text(art_xcoord[22],art_ycoord[22],'The Wire')
f_ax3.text(art_xcoord[27],art_ycoord[27],'The Sopranos')
f_ax3.text(art_xcoord[19],art_ycoord[19],'Band of Brothers')
f_ax3.text(art_xcoord[30],art_ycoord[30],'The Grapes of Wrath')
f_ax3.text(-0.2,0.55,'Country', color=[0,1,0])
f_ax3.text(0.35,-0.55,'Rock', color=[1,0,0])
f_ax3.text(-0.7,-0.55,'Hip-Hop', color=[0,0,1])

#a;sldkfj;lsakdjfa;lgskj
patch = patches.PathPatch(path, facecolor='none', lw=2, alpha = 0.2)
f_ax2.add_patch(patch)
f_ax2.set_xlim(-0.566, 0.566)
f_ax2.set_ylim(-0.5, 0.5)

artist_file = 'classifications/song_genre_class.csv'
artist_fits = pd.read_csv(artist_file,encoding = "ISO-8859-1")

art_xcoord = np.array(artist_fits.rock)*0.5 - np.array(artist_fits.hiphop)*0.5 
art_ycoord = np.array(artist_fits.rock)*-0.433 - np.array(artist_fits.hiphop)*0.433 + np.array(artist_fits.country)*0.433

color = np.zeros((len(art_xcoord),3))
for i in range(0,len(art_xcoord)):

    if artist_fits.genre[i]=='rock':
        r=1;g=0;b=0;
    if artist_fits.genre[i]=='country':
        g=1;r=0;b=0;
    if artist_fits.genre[i]=='hip-hop':
        b=1;g=0;r=0;
    color[i,:] = [r, g, b]

f_ax2.scatter(art_xcoord,art_ycoord,c=color,alpha=0.2)
f_ax2.set_aspect('equal')
f_ax2.axis('off')
f_ax2.set_title('Song Assignments')

#a;sldkfj;lsakdjfa;lgskj
patch = patches.PathPatch(path, facecolor='none', lw=2, alpha = 0.2)
f_ax1.add_patch(patch)
f_ax1.set_xlim(-0.566, 0.566)
f_ax1.set_ylim(-0.5, 0.5)

artist_file = 'classifications/artist_genre_class.csv'
artist_fits = pd.read_csv(artist_file,encoding = "ISO-8859-1")

art_xcoord = np.array(artist_fits.rock)*0.5 - np.array(artist_fits.hiphop)*0.5 
art_ycoord = np.array(artist_fits.rock)*-0.433 - np.array(artist_fits.hiphop)*0.433 + np.array(artist_fits.country)*0.433

color = np.zeros((len(art_xcoord),3))
for i in range(0,len(art_xcoord)):

    if artist_fits.genre[i]=='rock':
        r=1;g=0;b=0;
    if artist_fits.genre[i]=='country':
        g=1;r=0;b=0;
    if artist_fits.genre[i]=='hip-hop':
        b=1;g=0;r=0;
    color[i,:] = [r, g, b]

f_ax1.scatter(art_xcoord,art_ycoord,c=color,alpha=0.4)
f_ax1.set_aspect('equal')
f_ax1.axis('off')
f_ax1.set_title('Artist Assignments')

#plt.show()
plt.savefig("img/genre-assignments.png", format="png")