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


'''


legpt=''
legbr=''
tor=''
title =''

from enum import Enum
class Site(Enum):
  Legendas = 1
  Torrent = 2
  IShows = 3

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
    
  return url

def tor_action(sender):
  if view['switchTor'].value:
    view['switchPt'].value=False
    view['switchBr'].value=False
  
def leg_pt_action(sender):
  if view['switchPt'].value:
    view['switchTor'].value=False
    
def leg_br_action(sender):
  if view['switchBr'].value:
    view['switchTor'].value=False

def search_action(sender):
  #get swichs state
  global legbr, legpt, tor
  #, legendasdivxUrl, legendasdivxUrlLang, title, torrentUrl
  legpt = view['switchPt'].value
  legbr = view['switchBr'].value
  tor = view['switchTor'].value
  if legbr and legpt:
    url = geturl(title,Lingua.ALL,Site.Legendas)
  elif legbr or legpt:
    if legbr:
      url = geturl(title,Lingua.BR,Site.Legendas)
    else:
      url = geturl(title,Lingua.PT,Site.Legendas)
  
  if tor:
    url = geturl(title,None,Site.Torrent)
    
  print('url: ',url)
  app = UIApplication.sharedApplication()
  app.openURL_(nsurl(url))
  view.close()

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
def main():
  global title
  im = None
  url_imdb = u'http://www.imdb.com/title/tt3263904/'
  
  url_imdb = 'https://yts.ag/movie/the-boss-baby-2017'
  
  url_imdb = u'http://ishowsapp.com/share/episode/5966172'
  
  url_imdb = u'https://www.legendasdivx.pt/modules.php?name=Downloads&file=jz&imdbid=4481414&form_cat=28'
  
  url_imdb = 'https://www.legendasdivx.pt/modules.php?name=Downloads&d_op=viewdownloaddetails&lid=258522'
  
  if appex.is_running_extension():
    url_imdb = appex.get_url()
    print('url:',url_imdb)
    #sheet_text = appex.get_text()
  if url_imdb.startswith('https://yts.ag/movie/'):
    print('yts detected')
    disableTorrent()
    im = imdb(url_imdb,SourceSite.YTS)
  elif url_imdb.startswith('http://ishowsapp.com'):
    input_text=''
    if appex.is_running_extension():
      input_text=appex.get_text()
    else:
      input_text = u'The Strain: Noite Absoluta - The Worm Turns [S04E01]'
    title = input_text[:input_text.rfind(' - ')] 
    disableTorrent()
  elif url_imdb.startswith('https://www.legendasdivx.pt/modules.php?name=Downloads&file=jz&imdbid='):
    #get it indb id
    imdburl=u'http://www.imdb.com/title/{0}/'
    print('legendas divx detected with imdb in url - not supportee yet')
    #ttid = url_imdb.rfind
  elif url_imdb.startswith('https://www.legendasdivx.pt/modules.php?name=Downloads&d_op=viewdownloaddetails&lid='):
    im = imdb(url_imdb,SourceSite.LEGENDAS_IMDBID)
    url_imdb = im.title
    im = imdb(url_imdb,SourceSite.IMDB)
    disableLegendas()
    print('legendas divx detected')
  elif url_imdb.startswith(u'http://www.imdb.com/title/tt'):
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
