import string
from collections import Counter
import os
import matplotlib.pyplot as plt
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy

nlp = spacy.load('de_core_news_md')

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

def load_emotion_words(emotion_file, encoding='utf-8'):
    with open(emotion_file, 'r', encoding=encoding, errors='replace') as file:
        emotion_words = [line.strip().lower() for line in file]
    return emotion_words

def process_text(text_file, encoding='utf-8'):
    with open(text_file, encoding=encoding, errors='replace') as file:
        text = file.read().lower()
        doc = nlp(text)
        text = ' '.join([x.lemma_ for x in doc])

    cleaned_text = text.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = word_tokenize(cleaned_text, "german")

    final_words = []
    for word in tokenized_words:
        if word not in stopwords.words('german'):
            final_words.append(word)
    return final_words

def analyze_emotions(text_file, emotion_files):
    final_words = process_text(text_file)

    emotion_list = []
    for emotion_file in emotion_files:
        emotions = load_emotion_words(emotion_file)
        for word in final_words:
            if word in emotions:
                emotion_list.append(os.path.splitext(os.path.basename(emotion_file))[0])

    return emotion_list

def plot_emotion_distribution(emotion_list):
    w = Counter(emotion_list)

    fig, ax1 = plt.subplots()
    ax1.bar(w.keys(), w.values())
    fig.autofmt_xdate()
    plt.savefig('graph.png')
    plt.show()

if __name__ == "__main__":
    text_file = 'read.txt'
    emotion_files = ['Freude.txt','Trauer.txt','Ueberraschung.txt','Verachtung.txt','Wut.txt','Ekel.txt','Furcht.txt']

    emotion_list = analyze_emotions(text_file, emotion_files)
    print(emotion_list)

    plot_emotion_distribution(emotion_list)
