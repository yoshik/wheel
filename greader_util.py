# -*- coding: utf-8 -*-
import xml
import json
import gdata.service

# these are dummy address/password. you need rewrite it.
config = {'Email':'hogefuga@gmail.com', 'Passwd': 'hogefugaspassword' }

def reader_login():
  service = gdata.service.GDataService( \
    account_type="GOOGLE", \
    service = 'reader',
    server = 'www.google.com',
    source = 'MyReaderHoge')

  service.ClientLogin(config['Email'], config['Passwd'])
  token = service.GetClientLoginToken()
  return service

def get_all_tags(service):
  qtag = gdata.service.Query(feed='/reader/api/0/tag/list', params={'output':'json'})
  tags = json.loads(service.Get(qtag.ToUri(), converter=lambda x:x))
  return tags['tags']


# we want to get as json but cannot obtain data as json...
def get_feeds_with_tag(service, tags):
  feeds = []
  for tag in tags:
    qarticle = gdata.service.Query(feed='/reader/atom/' + tag['id'], params={'n': '100', 'output':'json'}) 
    f = service.Get(qarticle.ToUri(), converter=lambda x:x)
    feeds.append(f)
  return feeds

def get_text_from_titlenodes(nodes):
  texts = []
  for node in nodes: 
    child = node.childNodes[0] # FIXME: replace more generalized one
    if child.nodeType == child.TEXT_NODE:
      texts.append(child.data)
  return texts

def get_titlenodes_from_entrynodes(entries):
  titles = []
  for entry in entries:
    title = entry.getElementsByTagName("title")[0] # FIXME: replace more generalized one.
    titles.append(title)
  return titles

def get_entrynodes_from_feednodes(feeds):
  entries = []
  for feed in feeds:
    dom = xml.dom.minidom.parseString(feed)
    #print dom.toprettyxml(indent=" ")
    for entry in dom.getElementsByTagName("entry"):
      entries.append(entry)
  return entries

def get_titles():
  textslist = []
  s = reader_login()
  tags = get_all_tags(s )
  feeds = get_feeds_with_tag(s, tags)
  entries = get_entrynodes_from_feednodes(feeds)
  titles = get_titlenodes_from_entrynodes(entries)
  titletexts = get_text_from_titlenodes(titles)
  return titletexts

def titles_dump():
  for texts in get_titles():
    print texts


#for entry in feeds.entry:
  #dom = xml.dom.minidom.parseString(entry.ToString())
  #print dom.toprettyxml(indent="  ")
  #print "href: %s " % entry.GetHtmlLink().href
  #print "title: %s" % entry.title.text
      
