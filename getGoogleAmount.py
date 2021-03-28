import requests
from bs4 import BeautifulSoup



def getNumOfResults(searchTerm):
    initialHeaders = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    }
    plussedSearchTerm = searchTerm.replace(' ','+')
    r = requests.get('https://www.google.com/search?q='+plussedSearchTerm+'&oq='+plussedSearchTerm+'&aqs=chrome..69i57j33i160.3301j0j7&sourceid=chrome&ie=UTF-8', headers=initialHeaders)

    soup = BeautifulSoup(r.text)

    numOfResults = soup.find('div',{"id": "result-stats"}).text.replace('About ','').split(' results')[0].replace(',','')
    return int(numOfResults)