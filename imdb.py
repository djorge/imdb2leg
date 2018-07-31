#!python3
from enum import Enum
import requests
import re

class SourceSite(Enum):
  IMDB = 1
  YTS = 2
  LEGENDAS_IMDBID =3
  
  
  
class imdb:
  def __init__(self, url, source):
    self.url = url
    self.title = ''
    self.source = source
    self.fetch()
  
  def saveToFile(self):
    print(f'saving content of url {self.url}')
    #print(f'**saving url content** {self.res.text}')
    with open('imdb-content.txt', 'wb') as out_file:
      out_file.write(self.res.text.encode('utf-8'))
      
    #file = open('benfas_site_html.html', 'wb')
    #file.write(req.text.encode('utf-8'))
    #file.close()
    return True

  def fetch(self):
    
    self.res = requests.get(self.url,verify=False)
    if self.res.status_code  == requests.codes.ok:
                #print self.res.text
                #self.title = self.getTitle()
      #if self.source == SourceSite.IMDB
      #self.saveToFile()
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
      regexToGetTitle = "<h1 itemprop=\"name\">(.*?)</h1>"
    elif self.source == SourceSite.LEGENDAS_IMDBID:
      regexToGetTitle='(http://www.imdb.com/title/tt\d{7})'

    #extract with regex
    regexTitle = re.compile(regexToGetTitle)
    #print(self.res.text)
    refound = regexTitle.search(self.res.text)
    if refound is not None:
      #print(refound.group(1))
      self.title = refound.group(1)

def main():
  
  #url_imdb = 'https://www.imdb.com/title/tt2245988/'
  #url_imdb='https://www.imdb.com/title/tt4912910/'
  url_imdb='https://www.imdb.com/title/tt2798920/'
  im = imdb(url_imdb,SourceSite.IMDB)
  print('title extracted:',im.title)
if __name__ == '__main__':
  main()
