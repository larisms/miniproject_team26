from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests


client = MongoClient('15.164.170.238', 27017, username="test", password="test")
db = client.dbhomework_week1

driver = webdriver.Chrome('./chromedriver')

url = "https://m.map.naver.com/search2/search.naver?query=%EC%95%A0%EA%B2%AC%20%EC%9C%A0%EC%B9%98%EC%9B%90&sm=shistory&style=v5"

driver.get(url)
time.sleep(5)

for i in range(1):
    try:
        btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
        btn_more.click()
        time.sleep(5)
    except NoSuchElementException:
        break

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

places = soup.select("#ct > div.search_listview._content._ctList > ul > li")
#ct > div.search_listview._content._ctList > ul > li

# print(places)

for place in places:
    title = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_info > a.a_item.a_item_distance._linkSiteview > div > strong").text
    address = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_info > div.item_info_inn > div > a").contents[1].strip()
    image = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_info > a.item_thumb._itemThumb > img")
    category = place.select_one("#ct > div.search_listview._content._ctList > ul > li > div.item_info > a.a_item.a_item_distance._linkSiteview > div > em").text
    # show, episode = place.select_one("div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)
    print(title, address, category, image)

    headers = {
        "X-NCP-APIGW-API-KEY-ID": "va9dugepnd",
        "X-NCP-APIGW-API-KEY": "19elOrPT3s9FZzfmjFf8raXwxU0sX2lhya2f5Kam"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
    response = r.json()
    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])
            print(title, address, category, x, y)
            doc = {
                "title": title,
                "address": address,
                "category": category,
                # "show": show,
                # "episode": episode,
                "mapx": x,
                "mapy": y}
            db.matjips.insert_one(doc)


        else:
            print(title, "좌표를 찾지 못했습니다")

