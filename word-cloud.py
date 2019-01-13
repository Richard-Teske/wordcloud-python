import matplotlib.pyplot as plt
import pandas as pd 
import os
from collections import Counter


file_path = os.path.dirname(__file__)
file_name = 'trump-tweets.csv'

df = pd.read_csv(file_name, sep=',', header=0)
df = df.drop(columns='Client Simplified')

import re

stopWords = open('stopwords.txt','r').read().split('\n')

tweets = []

for rows in df['Tweet']:
    
    tweet = [word.upper() for word in rows.split() if word.lower() not in stopWords]
    tweet = ' '.join(tweet)
    tweet = re.sub('[^a-zA-Z0-9 ]+','',tweet)
    tweets.append(tweet)

font = 'Calibri.ttf'
fontpath = os.path.join('fonts',font)

def save(wordCloud, name):
    plt.figure(figsize=(30,15))
    plt.axis('off')
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.savefig(name)

import wordcloud

wc = wordcloud.WordCloud(font_path=fontpath,
    width=1600, height=800,
    background_color='black',
    max_words=1000,
    max_font_size=1000
).generate(' '.join(tweets))

save(wc, 'wc-default.png')

import numpy as np

def grey_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl(10,0%%, %d%%)" % np.random.randint(30,100))

wc.recolor(color_func=grey_color_func)
save(wc, 'wc-grey.png')

from PIL import Image

from wordcloud import ImageColorGenerator

img_usa = 'usa-flag.png'
usa_mask = np.array(Image.open(os.path.join(file_path, img_usa)))

wc = wordcloud.WordCloud(font_path=fontpath,
    mask=usa_mask,
    background_color='black',
    width=1600, height=800,
    max_words=1000,
    max_font_size=1000
).generate(' '.join(tweets))

image_colors = ImageColorGenerator(usa_mask)
wc.recolor(color_func=image_colors)
save(wc, 'wc-usa.png')

import multidict

img_thumb = 'thumbs-up.jpg'
thumb_mask = np.array(Image.open(os.path.join(file_path, img_thumb)))

words = multidict.MultiDict()
for i in range(100):
    words.add('Obrigado', np.random.randint(1, 10))

wc = wordcloud.WordCloud(font_path=fontpath,
    mask=thumb_mask,
    background_color='white',
    width=1600, height=800,
    max_font_size=1000).generate_from_frequencies(words)

def green_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return("hsl(120,100%%, %d%%)" % np.random.randint(20,40))

image_colors = ImageColorGenerator(thumb_mask)
wc.recolor(color_func=green_color_func)
save(wc, 'obrigado.png')

print('All images saved!')