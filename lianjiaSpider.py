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
    print '消重前数量为：'+str(cursor.execute("""select * from `tb_ershouhouse_new` """))
    cursor.execute("""create  temporary table temp as select min(id) as MINID from `tb_ershouhouse_new` group by name;""")
    cursor.execute("""delete from `tb_ershouhouse_new` where id not in (select minid from temp);""")
    print '消重后数量为：'+str(cursor.execute("""select * from `tb_ershouhouse_new` """))
    print '消重完成！'


def insert(conn, district, name, totalPrice, perPrice, communityName, houseType, area, houseTowards, houseDec,
           hasElevator, positionInfo, followNum, viewTime, publishTime, url):
    cursor = conn.cursor()
    cursor.execute("""use lianjiaspider;""")
    cur = conn.cursor()
    if district == 'jiangning':
        district = '江宁'
    if district == 'gulou':
        district = '鼓楼'
    if district == 'jianye':
        district = '建邺'
    if district == 'qinhuai':
        district = '秦淮'
    if district == 'xuanwu':
        district = '玄武'
    if district == 'yuhuatai':
        district = '雨花台'
    if district == 'qixia':
        district = '栖霞'
    if district == 'pukou':
        district = '浦口'
    if district == 'liuhe':
        district = '六合'
    if district == 'lishui':
        district = '溧水'
    if district == 'gaochun':
        district = '高淳'

    cur.execute(
        "insert into tb_ershouhouse_new(district,name,totalPrice,perPrice,communityName,houseType,area,houseTowards,houseDec,hasElevator,positionInfo,followNum,viewTime,publishTime,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (
            district, name, totalPrice, perPrice, communityName, houseType, area, houseTowards, houseDec, hasElevator,
            positionInfo, followNum, viewTime, publishTime, url
        )
    )
    conn.commit()


if __name__ == "__main__":
    conn = MySQLdb.connect(host='localhost', user='root', passwd='franksun1992', charset='utf8')
    cursor = conn.cursor()
    # 'jiangning','jianye', 'qinhuai',, 'pukou', 'liuhe', 'lishui', 'gaochun'], 'yuhuatai'
    houseUrls = ['xuanwu','jiangning','jianye','qinhuai','pukou','liuhe','lishui','gaochun','yuhuatai']
    params = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
              "Accept-Language": "zh-CN,zh;q=0.8", "Host": "nj.lianjia.com",
              "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
              "Cookie": "all-lj=492291e11daf53bf34d39f84cc442d11; lianjia_uuid=a12fbf9c-12b2-47e8-bd19-9fdcef594d44; UM_distinctid=15d1fe945cbdd4-018137f4b627eb-30667808-1aeaa0-15d1fe945ccafb; select_city=320100; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _smt_uid=59603bb7.954ba75; CNZZDATA1253492138=1518052315-1499478520-https%253A%252F%252Fwww.baidu.com%252F%7C1499584761; CNZZDATA1254525948=1570011814-1499475836-https%253A%252F%252Fwww.baidu.com%252F%7C1499586761; CNZZDATA1255633284=428379147-1499476209-https%253A%252F%252Fwww.baidu.com%252F%7C1499584235; CNZZDATA1255604082=1744293943-1499474094-https%253A%252F%252Fwww.baidu.com%252F%7C1499583817; _ga=GA1.2.1302735199.1499478969; _gid=GA1.2.1959352430.1499478969; lianjia_ssid=ea9e2b06-982c-48cf-be49-c9d9f17f085c"}
    urls = []
    for district in houseUrls:
        for i in range(1, 5):
            urls.append("http://nj.lianjia.com/ershoufang/" + district + "/pg" + str(i))
    for url in urls:
        district = url.split('/')[4]
        print url
        req = urllib2.Request(url, headers=params)
        page = urllib2.urlopen(req)
        dom_tree = etree.HTML(page.read())
        links = dom_tree.xpath('//div[@class="info clear"]')
        for j in links:
            url = j.xpath('.//a[@data-el="ershoufang"]/@href')[0]
            name = j.xpath('.//a[@data-el="ershoufang"]/text()')[0].encode('utf-8')
            totalPrice = j.xpath('.//div[@class="totalPrice"]/span/text()')[0]
            perPrice = j.xpath('.//div[@class="unitPrice"]/span/text()')[0].replace('单价', '').replace('元/平米', '')
            houseInfo = j.xpath('.//a[@data-el="region"]/text()')[0].encode('utf-8') + \
                        j.xpath('.//div[@class="houseInfo"]/text()')[0].encode('utf-8')
            houseInfoDict = houseInfo.replace(' ', '').split('|')
            if len(houseInfoDict) >= 1:
                communityName = houseInfoDict[0]
            if len(houseInfoDict) >= 2:
                houseType = houseInfoDict[1]
            if len(houseInfoDict) >= 3:
                area = houseInfoDict[2].replace('平米', '')
            if len(houseInfoDict) >= 4:
                houseTowards = houseInfoDict[3]
            if len(houseInfoDict) >= 5:
                houseDec = houseInfoDict[4]
            hasElevator = ''
            if len(houseInfoDict) == 6:
                hasElevator = houseInfoDict[5].replace('电梯', '')
            positionInfo = j.xpath('.//a[@target="_blank"]/text()')[0].encode('utf-8') + "|" + \
                           j.xpath('.//div[@class="positionInfo"]/text()')[0].encode('utf-8')
            followInfo = j.xpath('.//div[@class="followInfo"]/text()')[0].encode('utf-8')
            dictFollowInfo = followInfo.replace(' ', '').split('/')
            followNum = dictFollowInfo[0].replace('人', '').replace('关注', '')
            viewTime = dictFollowInfo[1].replace('次带看', '').replace('共', '')
            publishTime = dictFollowInfo[2]
            print name
            insert(conn, district, name, totalPrice, perPrice, communityName, houseType, area, houseTowards, houseDec,
                   hasElevator, positionInfo, followNum, viewTime, publishTime, url)


            # print totalPrice
            # print perPrice
            # print communityName
            # print houseType
            # print area
            # print houseTowards
            # print houseDec
            # print hasElevator
            # print positionInfo
            # print followNum
            # print viewTime
            # print publishTime
            # print url


            # links = dom_tree.xpath('//div[@class="title"]/a')
            # for j in links:
            #     # print j.text,j.attrib['href']
            #     # insertconn,j.text,j.attrib['href'])
            #     insert(conn, j.text, j.attrib['href'])
            # time.sleep(random.uniform(5, 15))
            # print district + '第' + str(i) + '页执行完毕！'
    print '执行完毕！'
    print '开始进行消重！'
    deleteSameRecord(conn)
    conn.close()
