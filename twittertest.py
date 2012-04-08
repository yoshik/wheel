# -*- coding: utf-8 -*-
import networkx as nx
import re
import nltk
import cPickle
import twitter
import json

def text_words(text=""):
  return [w for w in text.split() ]

def text_word_counting(text=""):
  return len(text_words(text))

def text_unique_word_counting(text=""):
  return len(set(text_words(text)))

def textlist_words(textlist=[]):
  return [w \
    for text in textlist \
      for w in text.encode("utf-8").split() ]
 
def textlist_word_counting(textlist=[]):
  return len(textlist_words(textlist))
 
def textlist_unique_word_counting(textlist=[]):
  return len(set(textlist_words(textlist)))


def twitter_search_results(query):
  twitter_search = twitter.Twitter(domain="search.twitter.com")
  search_results = []
  for page in range(1,6):
    search_results.append(twitter_search.search(q=query, rpp=100, page=page)['result'])
  tweets = [ r['text'] \
    for result in search_results \
      for r in result['results'] ]
  return tweets

def twitter_search_raw_results(query):
  twitter_search = twitter.Twitter(domain="search.twitter.com")
  search_results = []
  for page in range(1,6):
    search_results.append(twitter_search.search(q=query, rpp=100, page=page)['results'])
  return search_results


def freq_test():
  ts = twitter_search_results("twitter!")
  print textlist_word_counting(ts)
  print textlist_unique_word_counting(ts)

def freq_dist():
  textlist_words(twitter_search_results("nonparametric"))
  freq_dist = nltk.FreqDist(w)
  return freq_dist.keys()[:50]

def retweet_search(tweet):
  rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
  return [source.strip() \
    for tuple in rt_patterns.findall(tweet) \
      for source in tuple \
        if source not in ("RT", "via")]

def tweet_graph():
  g = nx.DiGraph()
  for tweet in twitter_search_raw_results("rakuten"):
    for t in tweet:
      rt_sources = retweet_search(t["text"])
      if not rt_sources: continue
      for rt_source in rt_sources:
        g.add_edge(rt_source, t["from_user"], {"tweet_id" : t["id"]})
  print g.number_of_nodes()

tweet_graph()
