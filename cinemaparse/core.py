import requests
from bs4 import BeautifulSoup 
class CinemaParser:
    def __init__(self, city = 'msk'):
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
        se = soup.find('div', {'attr-title': name})
        if se.find('span', {'class': 'label label-bg label-default normal-font'}).contents[1] == ' сегодня':
            ss= se.find("a",{'class' : 'underdashed'})
            r_url = "https://" + self.city + ".subscity.ru/" + ss['href']
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
        else:
            return None
    def get_soonest_session(self):
        lis = self.get_films_list()
        sea = []
        for i in lis:
            sean = self.get_film_nearest_session(i)
            sea.append(sean)
        ind = []
        for i in range(len(sea)):
            if not sea[i]:
                ind.append(i)
        for i in reversed(ind):
            del lis[i]
            del sea[i]
        time = []
        for i in sea:
            time.append(i[1])
        inde = time.index(min(time))
        return sea[inde][0],time[inde], lis[inde]
