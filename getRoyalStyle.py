import schedule
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


def royalStyle():
    URL = 'https://maplestory.nexon.com/Guide/CashShop/Probability/RoyalStyle'
    req = requests.get(URL)
    soup = bs(req.text, 'html.parser')
    table = soup.select_one('table.my_page_tb2')

    items = []
    percentage = []
    count = 0

    # 로얄스타일 데이터 뽑기
    for i in table.find_all('td'):
        # print(i.get_text())
        if count == 0:
            pass

        elif count % 2 == 0:
            percentage.append(i.get_text())

        else:
            items.append(i.get_text())

        count += 1
        
    # 데이터 csv화
    df = pd.DataFrame({
        '아이템명': items,
        '획득확률': percentage
    })

    # print(df)
    df.set_index('아이템명', inplace=True)
    df.to_csv('royal.csv')


# 매주 목요일 12:00시에 실행
schedule.every().thursday.at("12:00").do(royalStyle)

while True:
    schedule.run_pending()
    time.sleep(1)



