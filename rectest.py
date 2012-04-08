# -*- coding: utf-8 -*- 
import nltk
import wheel
import twitter_util as twitt
import greader_util as greader

tws = [({'word':w}, 'like') for w in twitt.cleaning(twitt.words_of_timeline_of_usr("dankogai"))]
classifier = nltk.NaiveBayesClassifier.train(tws)
print nltk.classify.accuracy(classifier, [({'word':u'居た'},'dislike')])
