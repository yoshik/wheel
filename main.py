#-*- coding: utf-8 -*-
import feedparser
from wheel import test, container, mecab_wrapper, ngram_trie

RSSURL='http://jp.techcrunch.com/feed'

# word trigram
def sample_ngramtrie_word():
  t = ngram_trie.NgramTrie(3)
  r = feedparser.parse(RSSURL)
  analyzer = mecab_wrapper.MorphologicalAnalyzer()
  for entry in r['entries']:
    print entry['title']
    words = analyzer.split(entry['title'].encode('utf-8'))
    t.train(words)
  print '\ngenerated: '
  print t.sample_stream(1000, [])


# character unigram
def sample_ngramtrie__simple():
  t = ngram_trie.NgramTrie()
  t.insert(u"あだな")
  t.insert(u"あさだ")
  t.insert(u"あなた")
  t.insert(u"あした")
  t.insert(u"あしなが")
  t.insert(u"ありくい")
  print t.sample_stream(30, [])

# character trigram
def sample_ngramtrie():
  t = ngram_trie.NgramTrie(3)
  r = feedparser.parse(RSSURL)
  for entry in r['entries']:
    print entry['title']
    t.train(entry['title'])
  print '\ngenerated: '
  print t.sample_stream(1000, [])

def sample_mecab_wrapper__split():
  dl = DocList()
  analyzer = mecab_wrapper.MorphologicalAnalyzer()

  r = feedparser.parse(RSSURL)
  for entry in r['entries']:
    doc = container.Document(entry['title'])
    dl.append(doc)
  for m in analyzer.split(d.raw.encode("utf-8")):
    print m ,
  print

def sample_mecab_wrapper__extract_pos():
  dl = DocList()
  analyzer = mecab_wrapper.MorphologicalAnalyzer()

  r = feedparser.parse(RSSURL)
  for entry in r['entries']:
    doc = container.Document(entry['title'])
    dl.append(doc)
  for d in dl:
    for m in analyzer.extract_pos(d.raw.encode("utf-8"), [mecab_wrapper.POSType.NOUN]):
      print m+'|',
    print
     
def sample_mecab_wrapper__analyze():
  dl = DocList()
  analyzer = mecab_wrapper.MorphologicalAnalyzer()

  r = feedparser.parse(RSSURL)
  for entry in r['entries']:
    doc = container.Document(entry['title'])
    dl.append(doc)
  analyzer.analyze(d.raw.encode("utf-8"))
  for n in analyzer:
    print n+'|',
  print


if __name__=="__main__":
#  sample_ngramtrie__simple()
#  sample_ngramtrie()
  sample_ngramtrie_word()

