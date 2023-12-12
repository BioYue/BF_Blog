from pathlib import Path
import requests


def spider_bing():
    res = requests.get('https://www.bing.com/hp/api/model?mkt=zh-CN')
    url_suffix = res.json()['MediaContents'][0]['ImageContent']['Image']['Wallpaper']

    img_url = 'https://www.bing.com' + url_suffix
    bing_bg_img = requests.get(img_url).content

    base_dir = Path(__file__).resolve().parent.parent

    with open(base_dir.joinpath(f'app/blog/static/imgs/bing_bg.jpg'), 'wb') as f:
        f.write(bing_bg_img)
