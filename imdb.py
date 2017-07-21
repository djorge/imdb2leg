#!python3
from enum import Enum
import requests
import re

class SourceSite(Enum):
  IMDB = 1
  YTS = 2
  
class imdb:
  def __init__(self, url, source):
    self.url = url
    self.title = ''
    self.source = source
    self.fetch()

  def fetch(self):
    
    self.res = requests.get(self.url,verify=False)
    if self.res.status_code  == requests.codes.ok:
                #print self.res.text
                #self.title = self.getTitle()
      #if self.source == SourceSite.IMDB
      self.getTitle()
                #launch exception case error
  def parse(self):
      self.getTitle()
    
  def getTitle(self):
    regexToGetTitle=''
    #print('getTitle ')
    #REGEX to get imdb url title
    if self.source == SourceSite.IMDB:
      regexToGetTitle = "<meta property='og:title' content=\"(.*?) \(\d\d\d\d\)"
    elif self.source == SourceSite.YTS:
      regexToGetTitle = "<h1>(.*?)</h1>"

    #extract with regex
    regexTitle = re.compile(regexToGetTitle)
    #print(self.res.text)
    refound = regexTitle.search(self.res.text)
    if refound is not None:
      #print(refound.group(1))
      self.title = refound.group(1)

def main():
  
  url_imdb = 'https://yts.ag/movie/ghost-in-the-shell-2017'
  
  im = imdb(url_imdb,SourceSite.YTS)
  print('title extracted:',im.title)
main()
