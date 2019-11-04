import re
import json
import requests

def get_game_metadata(url):
    cookies = {'birthtime': '568022401'}

    scrape = ''
    try:
        scrape = requests.get(url, cookies=cookies, timeout=60).text
    except:
        return None
    
    rating = re.search(r'<span class="game_review_summary.*>(.*?)</span>', scrape)
    out_rating = 'No user reviews'
    if rating:
        out_rating = rating.group(1)
    
    tags = re.search(r'\[\{"tagid":.*\]', scrape)
    out_tags = []
    if tags:
        tags = json.loads(tags.group())
        count = 0
        for tag in tags:
            if count >= 5:
                break
            else:
                out_tags.append(tag['name'])
            count += 1
    
    dlc = re.search(r'<div class=\"content\">(.*?)<h1>Downloadable Content</h1><p>', scrape, re.DOTALL)
    out_dlc = False
    if dlc:
        out_dlc = True

    return (out_rating, out_tags, out_dlc)