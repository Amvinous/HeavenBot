import requests as rq


def emotions(emotion):
    response = rq.get(f'https://api.waifu.pics/sfw/{emotion}')
    url = response.text[8:-3]
    return url
