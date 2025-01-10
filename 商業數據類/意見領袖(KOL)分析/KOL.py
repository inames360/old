# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 10:56:58 2020

"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

container = pd.DataFrame()
for page in range(1,4):
    url = 'https://tw.noxinfluencer.com/youtube-channel-rank/_influencer-rank?country=tw&category=all&rankSize=100&type=0&interval=weekly&pageNum='+str(page)
    #請求網站
    list_req = requests.get(url)
    #將整個網站的程式碼爬下來
    soup = BeautifulSoup(list_req.content, "html.parser")
    #找到標籤
    getAllName = soup.findAll('span',{'class','kol-name'})
    getAllClass = soup.findAll('a',{'class','category-text'})
    getAllFans = soup.findAll('td',{'class','followerNum'})
    getAllLooked = soup.findAll('td',{'class','avgView'})
    getAllStar = soup.findAll('td',{'class','nox-score'})
    
    #開始整理資料
    theName = []
    theClass = []
    theFans = []
    theLooked = []
    theStar = []
    for i in range(80):#每一頁只有80筆資料
        theName.append(getAllName[i].text)
        theClass.append(getAllClass[i].text.replace(' ',''))
        theFans.append(getAllFans[i].find('span').text.replace(' ','')[:-1])
        theLooked.append(getAllLooked[i].find('span').text.replace(' ','')[:-1])
        theStar.append(getAllStar[i]['data-score'])
        
    data = pd.DataFrame({
        'Youtuber名稱':theName,
        '頻道分類':theClass,
        '訂閱數量':theFans,
        '平均觀看次數':theLooked,
        'Nox評級':theStar
        })
    
    container = pd.concat([container,data])
    time.sleep(3)
    
container['訂閱數量'] = container['訂閱數量'].astype(float)
container['平均觀看次數'] = container['平均觀看次數'].astype(float)
container['Nox評級'] = container['Nox評級'].astype(float)
container.to_csv('HKyoutuber排名.csv', encoding='utf-8-sig', index=False)



#進行資料分析
plt.figure(figsize=(20,10))
colorlist = []
for tx,ty,ab in zip(container['訂閱數量'],container['平均觀看次數'], container['Youtuber名稱']):
    Aavg = container['訂閱數量'].mean()
    Bavg = container['平均觀看次數'].mean()
    
    if (tx < Aavg) & (ty < Bavg):#第三象限
        colorlist.append('#abc4d8')
    elif (tx > Aavg) & (ty < Bavg):
        colorlist.append('#abd8bf')
    elif (tx < Aavg) & (ty > Bavg):
        colorlist.append('#d8bfab')
    else:
        plt.text(tx,ty,ab, fontsize=15)# 加上文字註解
        colorlist.append('#d8abc4')
# 繪製圓點
plt.scatter(container['訂閱數量'],container['平均觀看次數'],
            color= colorlist,
            s=container['Nox評級']**3*50,
            alpha=0.5)

plt.axvline(container['訂閱數量'].mean(), color='c', linestyle='dashed', linewidth=1) # 繪製平均線    
plt.axhline(container['平均觀看次數'].mean(), color='c', linestyle='dashed', linewidth=1) # 繪製平均線 

plt.title("意見領袖分析",fontsize=30)#標題
plt.ylabel('訂閱數量',fontsize=20)#y的標題
plt.xlabel('平均觀看次數',fontsize=20) #x的標題
plt.tight_layout()
# plt.savefig('意見領袖分析.png', dpi=300)
