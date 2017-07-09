# -*- coding: utf-8 -*-
import requests
import MySQLdb
from lxml import etree
import time
import random
import urllib, urllib2, cookielib, socket
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def deleteSameRecord(conn):
    cursor = conn.cursor()
    print '消重前数量为：'+str(cursor.execute("""select * from `tb_renthouse` """))
    cursor.execute("""create  temporary table temp as select min(id) as MINID from `tb_renthouse` group by name;""")
    cursor.execute("""delete from `tb_renthouse` where id not in (select minid from temp);""")
    print '消重后数量为：'+str(cursor.execute("""select * from `tb_renthouse` """))
    print '消重完成！'

def insert(conn,name,price,address,houseType,time,meters,region,towards,url):
    cursor = conn.cursor()
    cursor.execute("""use lianjiaspider;""")
    cur = conn.cursor()
    cur.execute(
        "insert into tb_renthouse(name,price,address,houseType,time,meters,region,towards,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (
            name,price,address,houseType,time,meters,region,towards,url
        )
    )
    conn.commit()


if __name__ == "__main__":
    conn = MySQLdb.connect(host='localhost', user='root', passwd='franksun1992', charset='utf8')
    cursor = conn.cursor()
    # 'jiangning','jianye', 'qinhuai',, 'pukou', 'liuhe', 'lishui', 'gaochun'], 'yuhuatai'
    houseUrls = ['xuanwu',]
    params = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
              "Accept-Language": "zh-CN,zh;q=0.8", "Host": "nj.lianjia.com",
              "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
              "Cookie": "all-lj=492291e11daf53bf34d39f84cc442d11; lianjia_uuid=a12fbf9c-12b2-47e8-bd19-9fdcef594d44; UM_distinctid=15d1fe945cbdd4-018137f4b627eb-30667808-1aeaa0-15d1fe945ccafb; select_city=320100; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _smt_uid=59603bb7.954ba75; CNZZDATA1253492138=1518052315-1499478520-https%253A%252F%252Fwww.baidu.com%252F%7C1499584761; CNZZDATA1254525948=1570011814-1499475836-https%253A%252F%252Fwww.baidu.com%252F%7C1499586761; CNZZDATA1255633284=428379147-1499476209-https%253A%252F%252Fwww.baidu.com%252F%7C1499584235; CNZZDATA1255604082=1744293943-1499474094-https%253A%252F%252Fwww.baidu.com%252F%7C1499583817; _ga=GA1.2.1302735199.1499478969; _gid=GA1.2.1959352430.1499478969; lianjia_ssid=ea9e2b06-982c-48cf-be49-c9d9f17f085c"}
    urls = []
    for district in houseUrls:
        for i in range(1, 3):
            urls.append("https://nj.lianjia.com/zufang/pg" + str(i))
    for url in urls:
        print url
        req = urllib2.Request(url, headers=params)
        page = urllib2.urlopen(req)
        dom_tree = etree.HTML(page.read())
        links = dom_tree.xpath('//ul[@class="house-lst"]/li')

        for j in links:
            try:
                url = j.xpath('.//a/@href')[0]
                name = j.xpath('.//a/@title')[0]
                price = j.xpath('.//div[@class="price"]/span/text()')[0]
                address = j.xpath('.//div[@class="con"]/a/text()')[0].replace('租房', '')
                houseType = j.xpath('.//div[@class="con"]/text()')[0]
                time = j.xpath('.//div[@class="con"]/text()')[1]
                meters = j.xpath('.//span[@class="meters"]/text()')[0].replace('平米', '')
                region = j.xpath('.//span[@class="region"]/text()')[0]
                zone = j.xpath('.//div[@class="where"]/span/text()')[0]
                towards = zone = j.xpath('.//div[@class="where"]/span/text()')[-1]

                print name
                print price
                print address
                print houseType
                print time
                print meters
                print region
                print towards
                print url

                insert(conn,name,price,address,houseType,time,meters,region,towards,url)
            except (Exception),e:
                print e
    print '执行完毕！'
    print '开始进行消重！'
    deleteSameRecord(conn)
    conn.close()
