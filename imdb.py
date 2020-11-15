#!python3
from enum import Enum
import requests
import re
from bs4 import BeautifulSoup

class SourceSite(Enum):
  IMDB = 1
  YTS = 2
  LEGENDAS_IMDBID =3
  TVSERIES = 4
  UMDIAFUIAOCINEMA = 5
  
  
class imdb:
  def __init__(self, url, source):
    self.url = url
    self.title = ''
    self.data=''
    self.dia=''
    self.hora=''
    self.source = source
    self.fetch()
  
  def saveToFile(self):
    print(f'saving content of url {self.url}')
    #print(f'**saving url content** {self.res.text}')
    with open('url-content.txt', 'wb') as out_file:
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
      if self.source == SourceSite.TVSERIES:
        print('parse tvseries')
    
  def getTitle(self):
    regexToGetTitle=''
    #print('getTitle ')
    #REGEX to get imdb url title
    if self.source == SourceSite.IMDB:
      regexToGetTitle = "<meta property='og:title' content=\"(.*?) \(\d\d\d\d\)"
      regexTitle = re.compile(regexToGetTitle)
      #print(self.res.text)
      refound = regexTitle.search(self.res.text)
      if refound is None:
        regexToGetTitle = "<meta property='og:title' content=\"(.*?) \(TV Series"
        refound = regexTitle.search(self.res.text)
        if refound is None:
          regexToGetTitle = "<meta property='og:title' content=\"(.*?) \(TV Mini-Series"
        
    elif self.source == SourceSite.YTS:
      regexToGetTitle = "<h1 itemprop=\"name\">(.*?)</h1>"
    elif self.source == SourceSite.LEGENDAS_IMDBID:
      #https://www.imdb.com/title/tt4881806
      regexToGetTitle='(https://wwww.imdb.com/title/tt\d{7})'
      print('BeautifulSoup')
      bsObj = BeautifulSoup(self.res.text ,'html5lib')
      table_el =bsObj.find('table',{'class':'forumborder2'})
      #print(f'{repr(table_el)}')
      tr_el=table_el.find_all('tr')
      #print(f'{len(tr_el)}')
      #print(f'{repr(tr_el[6])}')
      imdb_url =  tr_el[len(tr_el)-1].td.b.a['href']
      self.title= imdb_url
      #self.title=imdb_url[imdb_url.rfind('/')+1:] 
      return
    elif self.source == SourceSite.TVSERIES:
      print('BeautifulSoup')
      bsObj = BeautifulSoup(self.res.text ,'html5lib')
      titc =bsObj.find('div',{'class':'titulo left tituloOriginal'})
      self.title = titc.text[titc.text.find('tulo Original')+len('tulo Original'):]
      print(f'title:{titc.text}')
      print(f'title:{self.title}')
      
      canalc=bsObj.find('div',{'class':'detailCanalLogo'})
      #print(f"src attr:{canalc.img.attrs['src']}")
      if canalc.img:
        self.canal = canalc.img.attrs['src'].split('/')[2].split('_')[0]
        print(self.canal)
      else:
        self.canal='not found'
      
      emic =bsObj.find('div',{'class':'detailEmissao'})
      print(f'emissao:{emic.text}')
      self.emissao=emic.text
      emicAr = emic.text.split('-')
      self.dia=emicAr[0].strip()
      self.data=emicAr[1].strip()
      self.hora=emicAr[2].strip()
      self.emissao='_'+self.dia+'_'+'-'+self.data+'-'+self.hora
      print(f'dia:{self.dia}')
     
      print(f'data:{self.data}')
      regdiames = '(\d\d)([A-Za-z]{3})'
      regexdiame = re.compile(regdiames)
      refound = regexdiame.search(self.data)
      if refound is not None:
        print(refound.group(1))
        self.dianum = refound.group(1)
        print(refound.group(2))
        mes={}
        mes['Jan']='01'
        mes['Fev']='02'
        mes['Mar']='03'
        mes['Abr']='04'
        mes['Mai']='05'
        mes['Jun']='06'
        mes['Jul']='07'
        mes['Ago']='08'
        mes['Set']='09'
        mes['Out']='10'
        mes['Nov']='11'
        mes['Dez']='12' 
        self.mesnum= mes[refound.group(2)]
        print(f'mesnum:{self.mesnum}')
        
        #calculate time from now till specidies date
        import datetime
        now = datetime.datetime.now()
        show_year = now.year if int(self.mesnum)  >= now.month else now.year +1
        print(f'year calc:{show_year}')
        showtime = datetime.datetime(show_year,int(self.mesnum),int(self.dianum),23,00,00)
        self.duedate = (showtime - now).total_seconds()
        print(f'duedate:{self.duedate}')
        print(f'date diff:{(showtime - now)}')
      print(f'hora:{self.hora}')
      sinopsec=bsObj.find('div',{'class':'detailSinopse'})
      print(f'detailSinopse:{sinopsec.text}')
      self.sinopse=sinopsec.text
      
      self.emissao= self.emissao.replace('h',' ')#para evitar a deteccao de hora no Due
      print(f'emissao:{self.emissao}')
      
      return
    elif self.source == SourceSite.UMDIAFUIAOCINEMA:
      print('UMDIAFUIAOCINEMA')
      return 
    #extract with regex
    regexTitle = re.compile(regexToGetTitle)
    #print(self.res.text)
    refound = regexTitle.search(self.res.text)
    if refound is not None:
      print(refound.group(1))
      self.title = refound.group(1)
  
  def getDueDate(self):
    return self.duedate

def main():
  
  #url_imdb = 'https://www.imdb.com/title/tt2245988/'
  #url_imdb='https://www.imdb.com/title/tt4912910/'
  #url_imdb='https://www.imdb.com/title/tt2798920/'
  #url_imdb='https://www.legendasdivx.pt/modules.php?name=Downloads&d_op=viewdownloaddetails&lid=279813'
  
  #url_imdb='https://www.legendasdivx.pt/modules.php?name=Downloads&d_op=viewdownloaddetails&lid=309827'
  
  #url_imdb='https://www.legendasdivx.pt/modules.php?name=Downloads&d_op=viewdownloaddetails&lid=309827'
  
  #serie
  url_imdb='https://www.imdb.com/title/tt10048342/'
  #deveria encontrar https://www.imdb.com/title/tt4881806
  im = imdb(url_imdb,SourceSite.IMDB)
  print('title extracted:',im.title)
if __name__ == '__main__':
  main()
