from bs4 import BeautifulSoup
from utils.json_utils import utils_json
import urllib2

class bs4(utils_json):
    def __init__(self,url):
        super(bs4, self).__init__()
        resp = urllib2.urlopen(url)
        self.encoding=resp.info().getparam('charset')
        self.soup = BeautifulSoup(resp, "html.parser", from_encoding=self.encoding)

    def __repr__(self):
        return self.toJSON()

    def get_all_links(self,href=True):
        return self.soup.find_all('a', href=href)



if __name__ == '__main__':
    obj=bs4('http://www.newpct1.com/series-hd/666-park-avenue/1582')
    print obj.toJSON()