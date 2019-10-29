# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 11:30:43 2019

@author: NDH00360
"""
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
dfVlogsFinal=pd.DataFrame()
for videoId in videoId_list:#from CaptionSentiments.py
    try:
        text=YouTubeTranscriptApi.get_transcript(videoId)
        print(videoId)
        dfVlogs=pd.DataFrame(text)
        dfVlogs1=pd.DataFrame(dfVlogs['text'])
        dfVlogsFinal=dfVlogsFinal.append(dfVlogs1)
    except:
        print ("e")
        

dfVlogs.to_csv('C:\\Users\\NDH00360\\Desktop\\VloggersAltimaComments.csv')
dfVlogs=pd.read_csv(r"C:\Users\NDH00360\Desktop\YoutubeSentimets Data\videoCommentDataAltima.csv")
my_lst_str = ' '.join(map(str, dfVlogs['text']))

df1=dfVlogs

from nltk.tokenize import sent_tokenize
tokenized_text=sent_tokenize(my_lst_str)
print(tokenized_text)
dfVlogs=pd.DataFrame(tokenized_text)
from textblob import TextBlob
df1["polarity_score"] = df1['corpus'].apply(lambda x: TextBlob(x).sentiment.polarity)


from nltk.tokenize import word_tokenize
tokenized_word=word_tokenize(my_lst_str)


from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))


from sklearn.feature_extraction.text import TfidfVectorizer
tf=TfidfVectorizer()
text_tf= tf.fit_transform(df1['text'])


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    text_tf, df1['Polarity'], test_size=0.1, random_state=2)



from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
# Model Generation Using Multinomial Naive Bayes
clf = MultinomialNB().fit(X_train, y_train)
predicted= clf.predict(X_test)
print("MultinomialNB Accuracy:",metrics.accuracy_score(y_test, predicted))



