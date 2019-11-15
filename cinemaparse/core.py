import requests
from bs4 import BeautifulSoup 
class CinemaParser:
    def __init__(self, city):
        self.city= city
        self.content= None
        
        
    def extract_raw_content(self):
        request_url = "https://" + self.city + ".subscity.ru/"
        req =requests.get(request_url)
        self.content = req.text
        
        
    def print_raw_content(self):
        if not self.content:
            self.extract_raw_content()
        soup = BeautifulSoup(self.content)
        print(soup.prettify())
        
        
    def get_films_list(self):
        if not self.content:
            self.extract_raw_content()
        soup = BeautifulSoup(self.content)
        s = soup.find_all('div', {'class': 'movie-plate'})
        a = []
        for i in s:
            a.append(i['attr-title'])
        return a
      
      
    def get_film_nearest_session(self, name):
        if not self.content:
            self.extract_raw_content()
        self.name = name
        soup = BeautifulSoup(self.content)
        s = soup.find("a", string=name)
        r_url = "https://" + self.city + ".subscity.ru/" + s['href']
        reqst =requests.get(r_url)
        content = reqst.text
        soup = BeautifulSoup(content)
        s = soup.find("table",{'class':"table table-bordered table-condensed table-curved table-striped table-no-inside-borders"})
        a = []
        b = []
        for i in s:
            seans = i.find('td',{'class':'text-center cell-screenings'})
            b.append(seans)
            a.append(seans['attr-time'])
        ind = a.index(min(a))
        cin_names =s.find_all('div',{'class':'cinema-name'})
        return cin_names[ind].string, b[ind].a.string
