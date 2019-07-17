import requests
from bs4 import BeautifulSoup
def trans(word):
    url = 'http://m.youdao.com/translate'
    headers = {
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36"
    }
    data = {
            'inputtext': word,
            'type': 'AUTO'
    }
    res = requests.post(url, data=data, headers=headers)
    html1 = BeautifulSoup(res.text, features='html.parser')
    rest = html1.find_all('ul', id='translateResult')
    return rest[0].text