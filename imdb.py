import requests
import re

class imdb:
  def __init__(self, url):
    self.url = url
    self.title = ''
    self.fetch()

  def fetch(self):
    self.res = requests.get(self.url)
    if self.res.status_code  == requests.codes.ok:
                #print self.res.text
                #self.title = self.getTitle()
      self.getTitle()
                #launch exception case error

  def getTitle(self):
    #print('getTitle ')
    #REGEX to get imdb url title
    regexToGetTitle = "<meta property='og:title' content=\"(.*?) \(\d\d\d\d\)"

    #extract with regex
    regexTitle = re.compile(regexToGetTitle)
    #print(self.res.text)
    refound = regexTitle.search(self.res.text)
    if refound is not None:
      #print(refound.group(1))
      self.title = refound.group(1)

