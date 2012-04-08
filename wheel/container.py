import math

BOS = '$BOS$'
EOS = '$EOS$'

class Document:
  def __init__(self, raw=None):
    self.raw = raw
    self.splitted = None
    self.is_splitted = false

class DocList:
  def __init__(self):
    self.docs = []
  def __iter__(self):
    for doc in self.docs:
      yield doc
  def append(self, doc):
    self.docs.append(doc)

class DocumentTermCount:
  def __init__(self):
    self.total = 0
    self.term_count = {}

  def add(self, term):
    self.total += 1
    if self.term_count.has_key(term):
      self.term_count[term] += 1
    else:
      self.term_count[term] = 1

