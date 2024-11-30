import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient



items=[{
    "Name":"生乳捲","url":"https://www.yannick.com.tw/shop/productlist?Item1=06&Item2=6-16","maxpage":2},{
    "Name":"美式派塔","url":"https://www.yannick.com.tw/shop/productlist?Item1=06&Item2=6-10","maxpage":1},{
    "Name":"切片點心","url":"https://www.yannick.com.tw/shop/productlist?Item1=06&Item2=6-11","maxpage":2},{
    "Name":"生日蛋糕","url":"https://www.yannick.com.tw/shop/productlist?Item1=06&Item2=6-6","maxpage":1
    }
   ]
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

datas=[]


for item in items:
   for page in range(item.get('maxpage')):
    url=item.get('url')+"&Page="+str(page+1)
    res=requests.get(url,headers=headers)
    soup=BeautifulSoup(res.text,'lxml')#bs4網頁解析
    lists=soup.select('.js_box')

    for list in lists:
        name=list.find("div",class_='js_item').select('p')[0].text
        price=list.find("div",class_='js_item').select('span')[0].text
        link=list.select('img')[0]['src']
        datas.append({
           "Name":name,
           "Price":price,
           "Link":link
        })

client=MongoClient('mongodb://localhost:27017')
db=client['yannick']
collection=db['ykproduct']

if datas:
    collection.insert_many(datas)
    print(f"{len(datas)}插入數據成功")
else:
    print("插入數據失敗")
        

        