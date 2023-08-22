import requests
from bs4 import BeautifulSoup
import schedule
import time


def sendline():
  gas_url = 'https://gas.goodlife.tw/'
  gas_web = requests.get(gas_url)  #爬取網頁資料
  gas_web.encoding = 'utf-8'
  soup = BeautifulSoup(gas_web.text, "html.parser")

  #找到價格區間
  gas_datas = soup.find(id='gas-price')
  #調漲期間
  gas_title = gas_datas.find('p')
  #漲跌狀況
  gas_price = gas_datas.find('h2')
  msg = str(gas_title.text)+str(gas_price.text)
  print(msg)
  print(time.ctime(time.time()))




  #Line Notify權杖設定
  url = 'https://notify-api.line.me/api/notify'
  token = 'vvr0RmVaZBqfUHhOohASfxRBqcqNtmntFOhi1JYB3pZ'

  headers = {
    'Authorization': 'Bearer ' + token    # 設定權杖
  }

  data = {
    'message':msg,       # 設定要發送的訊息
    "stickerPackageId":"789",
    'stickerId':'10856'
  }
  data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法


#schedule.every(1).minutes.do(sendline)
# 每個星期日的13:10分執行任務

schedule.every(1).minutes.do(sendline)
while True:
    schedule.run_pending()
    time.sleep(1)