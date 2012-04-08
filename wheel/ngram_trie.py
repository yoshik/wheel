import random
import container

class NgramTrie:
  def __init__(self, howgram=1):
    if howgram < 1:
      howgram = 1  #
    self.root = TrieNode()
    self.count = 0
    self.howgram = howgram
  def insert(self, wordlist, value=1):
    self.root.insert(wordlist, value)
  def remove(self, wordlist, value=1):
    self.root.remove(wordlist, value)

  def train(self, wordstream):
    for k in range(0, len(wordstream)-self.howgram+1):
      #print wordstream[k]
      self.root.insert(wordstream[k:k+self.howgram])

  def sample_one(self, wordlist=[]):
#    if len(wordlist) == 0:
#      return None
    n = self.root.find(wordlist)
    if n != None:
      return n.sample()
    else:
      return self.sample_one(wordlist[1:])

  def sample_stream(self, outlen, wordlist=[]):
    out = []
    q = wordlist
    for i in range(0, outlen):
      if len(q) < self.howgram:
        s = self.sample_one(q)
        s = s if s != None else u" "
        q.append(s)
      else:
        s = self.sample_one(q)
        s = s if s != None else u" "
        q.append(s)
        out.append(q.pop(0))
    if len(q) > 0:
      for w in q:
        out.append(w)
    return out

  def inference(self, wordlist=[]):
    pass

  def dump(self):
    self.root.dump()

#keylist must be string or tuple
class TrieNode:
  def __init__(self):
    self.nodes = {}
    self.value = 0
    self.childsum = 0

  def has_member(self):
    return len(self.nodes) > 0

  def find(self, keylist):
    if len(keylist) == 0:
      return self
    k = keylist[0]
    if self.nodes.has_key(k):
      if len(keylist) == 1:
        return self.nodes[k]
      else:
        return self.find(keylist[1:])
    else:
      return None
    
  def insert(self, keylist, value=1):
    if len(keylist) > 0:
      key = keylist[0]
      if not self.nodes.has_key(key):
        self.nodes[key] = TrieNode()
      self.nodes[key].insert(keylist[1:])
      self.value += value
      if len(keylist) != 1:
        self.childsum += value
    else:
        self.value += value
	return True

  def remove(self, keylist, value=1):
    key = keylist[0]
    if len(keylist) == 1:
      if self.nodes.has_key(key):
        if self.nodes[key].value != 0: 
          self.nodes[key].value -= value 
          if not self.nodes[key].has_member() and self.nodes[key].value == 0:
	    del self.nodes[key]
	    return True
      return False
    else:
      if self.nodes.has_key(key):
        if self.nodes[key].remove(keylist[1:]):
	  self.value -= value
	  self.childsum -= value
          if not self.nodes[key].has_member():
	    del self.nodes[key]
            return True
      return False

  def sample(self):
    r = random.randint(0, self.childsum)
    s = 0
    for k, v in self.nodes.items():
      s += v.value
#      print k,v.value,s,r
      if r <= s:
        return k
    return None

  def inference(self, keylist):
    pass

  def dump(self, tab=0):
    for k, v in self.nodes.items():
      print " "*tab + str(self.childsum) + "{" + k + ":" + str(v.value)
      v.dump(tab+1)
      print " "*tab + "}"

