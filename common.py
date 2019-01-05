import requests

#公用

header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

def set_url(url, **params):
    response = requests.get(url, **params)
    response.encoding = 'utf-8'
    return response