import MeCab

#unknown??


# These numbers DON'T mean pos-id
class POSType:
  BROKEN = -1
  OTHER,       \
  FILLER,      \
  EXCLAMATION, \
  SIGN,        \
  ADJECTIVE,   \
  PARTICLE,    \
  AUXVERB,     \
  CONJUNCTION, \
  VERB,        \
  ADVERB,      \
  NOUN,        \
  PRENOUN = range(12) 

 
#  Mecab POS ID to our POSType ID
def toGeneralPOSID(id):
  if id == 0:
    return POSType.OTHER
  elif id == 1:
    return POSType.FILLER
  elif id == 2:
    return POSType.EXCLAMATION
  elif id >= 3 and id <= 9:
    return POSType.SIGN
  elif id >= 10 and id <= 12:
    return POSType.ADJECTIVE
  elif id >= 13 and id <= 24:
    return POSType.PARTICLE
  elif id == 25:
    return POSType.AUXVERB
  elif id >= 26 and id <= 30:
    return POSType.CONJUNCTION
  elif id >= 31 and id <= 33:
    return POSType.VERB
  elif id >= 34 and id <= 35:
    return POSType.ADVERB
  elif id >= 36 and id <= 67:
    return POSType.NOUN
  elif id -- 68:
    return POSType.PRENOUN
  else:
    return POSType.BROKEN
  
class MorphologicalAnalyzer:
  def __init__(self):
    self.tagger = MeCab.Tagger("-Ochasen")
    if self.tagger == None:
      raise RuntimeError 
    self.node = None

  def __iter__(self):
    return self

  def __is_member(self, member_list, given):
    for m in member_list:
      if m == given:
        return True
    return False

  def next(self):
    if self.node == None:
      raise StopIteration
      return None
    else:
      n = self.node
      self.node = self.node.next
      return n

  def analyze(self, str):
    self.node = self.tagger.parseToNode(str)

  def split(self, str):
    self.node = None
    self.analyze(str)
    return [n.surface for n  in self]

  def extract_pos(self, str, pos_type_list):
    self.node = None
    self.analyze(str)
    return [n.surface for n in self if self.__is_member(pos_type_list, toGeneralPOSID(n.posid)) ] 
    
