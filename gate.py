import csv
import time

from scrapy import Selector
from selenium_helper.chrome import SeleniumDriver

f = open('gate.csv', 'w')
writer = csv.writer(f)
writer.writerow(['Name', 'Short Name', 'Price', '24h change', 'High', 'Low', 'Volume', 'Market Cap'])
driver = SeleniumDriver(headless=False, cloud_flare=True)
url = 'https://www.gate.io/marketlist?tab=usdt'
response = driver.process_request(url=url, timeout=10)
response = Selector(text=driver.page_source)
for i in range(60):
    time.sleep(1)
    for tr in response.css('#mianBox > table > tbody > tr'):
        data = {
            'Name': tr.css('a.coin-name::attr(title)').get(''),
            'Short Name': ''.join(tr.css('span.name-con > b > span::text, span.name-con > b > i::text, span.name-con > b > em::text').extract()),
            'Price': tr.css('td:nth-child(2) > span::text').get(''),
            '24h change': tr.css('td:nth-child(3) > span::text').get(''),
            'High': tr.css('td:nth-child(4)::text').get(''),
            'Low': tr.css('td:nth-child(5)::text').get(''),
            'Volume': tr.css('td:nth-child(6)::text').get(''),
            'Market Cap': tr.css('td:nth-child(7)::text').get(''),
            'timestamp': int(time.time())
        }
        writer.writerow(data.values())

print(response)
