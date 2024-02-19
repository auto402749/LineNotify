import requests
from bs4 import BeautifulSoup
import schedule
import time


def sendline():
  gas_url = 'https://gas.goodlife.tw/'
  gas_web = requests.get(gas_url)   #爬取網頁資料
  gas_web.encoding = 'utf-8'
  soup = BeautifulSoup(gas_web.text, "html.parser")
  msg=""

  #找到價格區間
  updown = soup.find(id='gas-price')
  datas = soup.find(id='cpc')

  #print(updown)
  #print(datas)
  #調漲期間
  title = updown.find('p')
  title2 = datas.find('h2')
  msg += '\n'
  msg += title.text
  #print(title.text,end="")

  #漲跌狀況
  price = updown.find('h2')
  msg += price.text + '\n'
  #print(price.text)


  msg += "--------------------------------------------"+'\n'
  #print("--------------------------------------------")

  msg += title2.text + ":"+"\n"
  msg += '\n'
  #print(title2.text + ":")
  #print()

  items = datas.find_all('li')

  for i in range(len(items)):

    #print(items[i].text,end="")
    h3_item = items[i].find("h3")
    msg += h3_item.text.strip()
    #print(h3_item.text.strip(),end="")      #strip():移除字串頭尾指定的字符(默認為空格)
    h3_item.extract()                        #extract():把不要的標籤淬出或是移除
    msg += items[i].text.strip()+" 元/升"+"\n"
    msg += "\n"
    #print(items[i].text.strip()+" 元/升")
    #print()
  print(msg)


  #Line Notify權杖設定
  url = 'https://notify-api.line.me/api/notify'
  token = 'vvr0RmVaZBqfUHhOohASfxRBqcqNtmntFOhi1JYB3pZ'

  headers = {
    'Authorization': 'Bearer ' + token    # 設定權杖
  }

  data = {
    'message':msg,       # 設定要發送的訊息
    "stickerPackageId":"6325",
    'stickerId':'10979917'
  }
  data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法


schedule.every(2).minutes.do(sendline)
#每個星期日的13:30分執行任務(線上編譯器為GMT時間，台灣為GMT+8，故設定上要-8)
#schedule.every().sunday.at("05:30").do(sendline)
while True:
  schedule.run_pending()
  time.sleep(1)
