#!python3

import ui
import appex
import urllib
from imdb import imdb
from imdb import SourceSite
from objc_util import nsurl,UIApplication

'''appex.get_text()
u'The Strain: Noite Absoluta - The Worm Turns [S04E01]'
>>> appex.get_url()
u'http://ishowsapp.com/share/episode/5966172

shate da legenda do filme  seleccionado

>>> appex.get_url()
u'https://www.legendasdivx.pt/modules.php?name=Downloads&file=jz&imdbid=4481414&form_cat=28'



share do feed um dia fui ao cinema
appex.get input devolve listq
l[-1]['title']
u'The Great Raid'

https://zooqle.com/search?q=Orphan.s01e05


'''

#https://torrentz2.eu/search?f=Ozark.s01

#https://pirateproxy.cam/mobileproxy/search/Ozark.s01/0/0/0




legpt=''
legbr=''
tor=''
title =''

from enum import Enum
class Site(Enum):
  Legendas = 1
  Torrent = 2
  IShows = 3
  TorSearchZ2 = 4
  TorSearchPBay = 5
  TorSearchZooqle = 6
  ImdbSearch = 7

class Lingua(Enum):
  PT = 1
  BR = 2
  ALL = 3

def geturl(title,lingua,site):
  print(title)
  if lingua is not None:
    print(lingua.name)
  print(site.name)
  legendasdivxUrlLang ="http://www.legendasdivx.com/modules.php?name=Downloads&file=jz&d_op=search_next&order=&page=1&query={0}{1}"

  legendasdivxUrl ='http://www.legendasdivx.com/modules.php?name=Downloads&file=jz&d_op=search_next&order=&page=1&query={0}'

  torrentUrl='https://yts.ag/browse-movies/{0}/all/all/0/latest'
  
  torrSearchZ2Url = 'https://torrentz2.eu/search?f={}'
  
  torrSearchPBayUrl = 'https://pirateproxy.cam/mobileproxy/search/{}/0/0/0'
  
  torrSearchZooqleUrl='https://zooqle.com/search?q={}'
  
  imdb_search='imdb:///find?q={}'
  title_new = urllib.parse.quote_plus(title)
  
  url = ''
  if site == Site.Legendas:
    if lingua == Lingua.ALL:
      url = legendasdivxUrl
      url = url.format(title_new)
    else:
      url = legendasdivxUrlLang
      if lingua == Lingua.PT:
        url=url.format(title_new,'&form_cat=28')
      if lingua ==Lingua.BR:
        url=url.format(title_new,'&form_cat=29')
  elif site ==Site.Torrent:
    url=torrentUrl.format(title_new)
  elif site ==Site.TorSearchZ2:
    url=torrSearchZ2Url.format(title_new)
  elif site ==Site.TorSearchPBay:
    url=torrSearchPBayUrl.format(title_new)
  elif site ==Site.TorSearchZooqle:
    url=torrSearchZooqleUrl.format(title_new)
  elif site ==Site.ImdbSearch:
    url=imdb_search.format(title_new)
    
  return url
def viewEnabled(v):
  return view[v].enabled == True
  
def disableSwitch(sender):
  print('name:{} value: {}'.format(sender.name,sender.value))
  if sender.value == False:
    return
  if sender.name != 'switchPt':
    if viewEnabled('switchPt'):
      view['switchPt'].value=not sender.value
  if sender.name != 'switchBr':
    if viewEnabled('switchBr'):
      view['switchBr'].value=not sender.value
  #view['switchBr'].value=False
  if sender.name != 'switchTor':
    if viewEnabled('switchTor'):
      view['switchTor'].value=not sender.value
  if sender.name != 'switchTorzPBay':
    if viewEnabled('switchTorzPBay'):
      view['switchTorzPBay'].value=not sender.value  
  if sender.name != 'switchTorZ2':
    if viewEnabled('switchTorZ2'):
      view['switchTorZ2'].value=not sender.value
  if sender.name != 'switchTorZooqle':
    if viewEnabled('switchTorZooqle'):
      view['switchTorZooqle'].value=not sender.value
  if sender.name != 'switchImdb':
    if viewEnabled('switchImdb'):
      view['switchImdb'].value=not sender.value
  #view['switchTor'].value=False

def disableSearchTorrent():
  view['switchTz2'].enabled = False
  view['lblTorTz2'].enabled = False
  view['switchPBay'].enabled = False
  view['lblTorPBay'].enabled = False
  view['lblTorZooqle'].enabled = False
  view['switchZooqle'].enabled = False
  
  
def disableTorrent():
  view['switchTor'].enabled = False
  view['lblTor'].enabled = False
  
def disableLegendas():
  view['switchPt'].enabled = False
  view['lblLegPt'].enabled = False
  view['switchBr'].enabled = False
  view['lblLegBr'].enabled = False
  view['switchPt'].value = False
  view['switchTor'].value = True
  
def disableSearchImdb():
  view['switchImdb'].enabled = False
  
def disableTorrentSearch(s):
  print(type(s.sender))

def tor_action(sender):
#  if view['switchTor'].value:
#    view['switchPt'].value=False
#    view['switchBr'].value=False
  disableSwitch(sender)

  
def leg_pt_action(sender):
#  if view['switchPt'].value:
#    view['switchTor'].value=False
  disableSwitch(sender)

    
def leg_br_action(sender):
#  if view['switchBr'].value:
#    view['switchTor'].value=False
  disableSwitch(sender)

def torzPBay_action(sender):
  disableSwitch(sender)

def TorZ2_action(sender):
  disableSwitch(sender)
  
def imdb_action(sender):
  disableSwitch(sender)

def torZooqle_action(sender):
  disableSwitch(sender)

def search_action(sender):
  #get swichs state
  global legbr, legpt, tor
  #, legendasdivxUrl, legendasdivxUrlLang, title, torrentUrl
  
  legpt = view['switchPt'].value
  legbr = view['switchBr'].value
  tor = view['switchTor'].value
  torSearchZ2 = view['switchTorZ2'].value
  torSearchPBay = view['switchTorzPBay'].value
  torSearchZooqle = view['switchTorZooqle'].value
  imdbSearch=view['switchImdb'].value
  if legbr and legpt:
    url = geturl(title,Lingua.ALL,Site.Legendas)
  elif legbr or legpt:
    if legbr:
      url = geturl(title,Lingua.BR,Site.Legendas)
    else:
      url = geturl(title,Lingua.PT,Site.Legendas)
  
  if tor:
    url = geturl(title,None,Site.Torrent)
  elif torSearchPBay:
    url = geturl(title,None,Site.TorSearchPBay)
  elif torSearchZ2:
    url = geturl(title,None,Site.TorSearchZ2)
  elif torSearchZooqle:
    url = geturl(title,None,Site.TorSearchZooqle)
  elif imdbSearch:
    url = geturl(title,None,Site.ImdbSearch)
  
  print('url: ',url)
  app = UIApplication.sharedApplication()
  app.openURL_(nsurl(url))
  #view.close()


def main():
  global title
  im = None
  url_imdb = u'http://www.imdb.com/title/tt3263904/'
  
  url_imdb = 'https://yts.ag/movie/the-boss-baby-2017'
  url_imdb = 'https://yts.ag/browse-movies/Enigma/all/all/0/latest'
  
  #url_imdb = u'http://ishowsapp.com/share/episode/5966172'
  
  #url_imdb = u'https://www.legendasdivx.pt/modules.php?name=Downloads&file=jz&imdbid=4481414&form_cat=28'
  
  #url_imdb = 'https://www.legendasdivx.pt/modules.php?name=Downloads&d_op=viewdownloaddetails&lid=258522'
  
  if appex.is_running_extension():
    url_imdb = appex.get_url()
    input_text = appex.get_text()
    print('url:',url_imdb)
    print('text:',appex.get_text())
  else:
    #url_imdb=' http://ishowsapp.com/share/episode/5665645'
    input_text = 'Jigsaw'
  if url_imdb and  url_imdb.startswith('https://yts.ag/movie/'):
    print('yts detected')
    disableTorrent()
    im = imdb(url_imdb,SourceSite.YTS)
  elif url_imdb and  url_imdb.startswith('http://ishowsapp.com'):
    title=''
    input_text=''
    if appex.is_running_extension():
      input_text=appex.get_text()
      print(input_text)
    else:
      input_text = u'The Strain: Noite Absoluta - The Worm Turns [S04E01]'
    ep=None
    print('input_text:{}'.format(input_text))
    if input_text.rfind(']')+1== len(input_text):
      title = input_text[:input_text.rfind(' - ')] 
      ep = input_text[input_text.rfind('[')+1:input_text.rfind(']')]
      title = title + ' ' + ep 
    elif input_text.rfind(' - ') >0:
      title = input_text[:input_text.rfind(' - ')]  
    else:
      title = input_text 
    #
  if title == '':
    title = input_text
    print('title from {} is {}'.format(input_text,title))
    
    disableTorrent()
    
  elif url_imdb and url_imdb.startswith('https://www.legendasdivx.pt/modules.php?name=Downloads&file=jz&imdbid='):
    #get it indb id
    imdburl=u'http://www.imdb.com/title/{0}/'
    print('legendas divx detected with imdb in url - not supportee yet')
    #ttid = url_imdb.rfind
  elif  url_imdb and url_imdb.startswith('https://www.legendasdivx.pt/modules.php?name=Downloads&d_op=viewdownloaddetails&lid='):
    im = imdb(url_imdb,SourceSite.LEGENDAS_IMDBID)
    url_imdb = im.title
    im = imdb(url_imdb,SourceSite.IMDB)
    disableLegendas()
    print('legendas divx detected')
  elif url_imdb and  url_imdb.startswith(u'http://www.imdb.com/title/tt'):
    print('imdb detected')
    im = imdb(url_imdb,SourceSite.IMDB)
    
  if im is not None:
    print('tittle is:' + im.title)
    if len(title) ==0:
      title = im.title
  
  #print (sheet_text)
  
  view.present('sheet')
  
#app = UIApplication.sharedApplication()
#URL = 'https://www.google.co.uk/  searchbyimage?&image_url='
#app.openURL_(nsurl(URL))
view = ui.load_view()
main()
