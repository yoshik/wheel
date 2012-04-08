# -*- coding: utf-8 -*-
import sys
import re
# python-twitter module
import twitter
from wheel import mecab_wrapper, ngram_trie

TARGET_TWITTER_NAME = "dankogai"

rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
at_patterns = re.compile(r"@[a-zA-Z0-9_]+", re.IGNORECASE)
uname_patterns = re.compile(r"[a-zA-Z0-9_]+", re.IGNORECASE)

def timeline_of_usr(uname):
  twitter_api = twitter.Api()
  tl = twitter_api.GetUserTimeline(id=uname, count=198)
  return [t for t in tl]

def texts_of_timeline_of_usr(uname):
  twitter_api = twitter.Api()
  tl = twitter_api.GetUserTimeline(id=uname, count=198)
  return [t.text for t in tl]
 
def words_of_timeline_of_usr(uname):
  analyzer = mecab_wrapper.MorphologicalAnalyzer()
  return [ w \
  for t in texts_of_timeline_of_usr(uname) \
    for w in analyzer.split(t.encode("utf-8")) if w != None ]

def cleaning(words):
  wl = []
  prev = None
  for w in words:
    if len(at_patterns.findall(w)) == 0:
      if prev != None and prev == "@" and len(uname_patterns.findall(w)) > 0:
        prev = None
      else:
        if prev == None or prev == u" " or prev == u"　" or len(prev) == 0:
	  pass
	else:
          wl.append(prev)
        prev = w
    else:
      prev = None
  if prev == None or prev == u" " or prev == u"　" or len(prev) == 0:
    pass
  else:
    wl.append(prev)
  return wl   
  
def sample__ngramtrie_word_from_twitter(uname):
  t = ngram_trie.NgramTrie(3)
  wl = cleaning(words_of_timeline_of_usr(uname))
  t.train(wl)
  return t.sample_stream(1000, [])

def twitter_ngramtrie():
  for w in sample__ngramtrie_word_from_twitter(TARGET_TWITTER_NAME):
    sys.stdout.write(w)
