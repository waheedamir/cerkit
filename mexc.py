import csv
import time

from scrapy import Selector
from selenium_helper.chrome import SeleniumDriver

f = open('mexc.csv', 'w', encoding='utf-8')
writer = csv.writer(f)
writer.writerow(['Name', 'Short Name', 'Price', '24h change', 'High', 'Low', 'Volume'])
driver = SeleniumDriver(headless=False, cloud_flare=True)
url = 'https://www.mexc.com/markets'
response = driver.process_request(url=url, timeout=10)
response = Selector(text=driver.page_source)
for i in range(60):
    time.sleep(1)
    for tr in response.css('div.marketList_marketList__IY59o > div.marketList_tableRow__1ztCi'):
        data = {
            'Name': tr.css('span.marketList_fullName__ji-kY::text').get(''),
            'Short Name': tr.css('div.marketList_name__Yu3x1::text').get(''),
            'Price': tr.css('div.marketList_col2__1Yy4k > span::text').get(''),
            '24h change': tr.css('div.marketList_changeUp__c8n9f::text').get(''),
            'High': tr.css('div.marketList_col4__3le_K::text').get(''),
            'Low': tr.css('div.marketList_col5__3693j::text').get(''),
            'Volume': tr.css('div.marketList_col6__7aZuQ::text').get(''),
            'timestamp': int(time.time())
        }
        writer.writerow(data.values())

f.close()
