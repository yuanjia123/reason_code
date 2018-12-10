import rsa
import re
import json
import time
import requests
import base64
import urllib3
import binascii
import xlwt
from lxml import etree
import psycopg2
from multiprocessing.pool import ThreadPool   #线程池
import csv
import psycopg2
urllib3.disable_warnings()



class get_location():

    def __init__(self):
        self.headers = {

            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'SINAGLOBAL=686853348606.9484.1541139120819; SCF=AkhFCrKCUq9wsyl3f_fDwgGgFRpQSCclo3gd_NQHuXjdyEEjbRsY9PC-MgFG6xjCDbPu4IOAIOCXyPLirzjFWdo.; SUHB=00xZwj0czv30Gl; Ugrow-G0=56862bac2f6bf97368b95873bc687eef; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; YF-Page-G0=86b4280420ced6d22f1c1e4dc25fe846; YF-V5-G0=a9b587b1791ab233f24db4e09dad383c; wb_view_log_6382564064=1920*10801; _s_tentry=-; Apache=2872156489358.7036.1542848804714; ULV=1542848804736:6:6:3:2872156489358.7036.1542848804714:1542706013869; _T_WM=3e8b91cb0fc1afc6f6b197111618f23a; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9Wh3SFjwsRGoBE8ZBHKOX.cV5JpVF02RehnESKe41h24; SUB=_2AkMsqrpQdcPxrAVSkPoQym_iaolH-jyff9OmAn7uJhMyAxgv7nNeqSVutBF-XJVarBSeGUU5IPLleV-08g-rwQpV; login_sid_t=a2b0e92dbac53ded77a3b3a4328efdaa; cross_origin_proto=SSL; WBStorage=f44cc46b96043278|undefined; UOR=,,login.sina.com.cn; wb_view_log=1920*10801',
            'Host': 'weibo.com',
            'Referer': 'https://weibo.com/2889942201/GFo7omJqz?type=comment',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }


    def get_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                return response.text
            else:
                print(response.status_code)
                time.sleep(0.5)
                return self.get_html(url)
        except requests.ConnectionError as e:
            print('Error', e.args)


    def parse(self, html):  # 解析
        try:
            id = list(set(re.findall('usercard="id=(\d{10})"',html.replace('\\',''))))
            time = re.findall(r'title=\"(\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2})\"',html.replace('\\',''))
        except:
            print("正则匹配有问题")
        return id,time

    def page_parse(self,html):
        try:
            page = int(re.findall("totalpage\":(\d*)\,", html.replace('\\', ''))[0])
        except:
            print("页码匹配有问题")
        return page


class IO_rw(object):

    def __init__(self):
        self.csvfile = open("test.csv", "w")
        self.writer = csv.writer(self.csvfile)

        self.conn = psycopg2.connect(database="postgres", user="postgres", password="123456", host="127.0.0.1", port="5432")
        self.cur = self.conn.cursor()

    def process_item(self):

        self.cur.execute("select * from temp_1")
        rows = self.cur.fetchall()
        id = []
        for row in rows:
            #print("row",row)
            id.append(row[2].split('com/')[1])
        self.cur.close()
        return id

    def cun_item(self,id,m):
        #UPDATE temp_1 SET id = 1 WHERE url = 'https://weibo.com/3341882282'

        self.cur.execute("UPDATE temp_1 SET id = {1} WHERE url like '%{2}'".format(id,m))


    def close_spider(self):
        self.conn.close()
        self.csvfile.close()

if __name__ == '__main__':

    headers_1 = {

        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        #'Cookie': 'SINAGLOBAL=686853348606.9484.1541139120819; SCF=AkhFCrKCUq9wsyl3f_fDwgGgFRpQSCclo3gd_NQHuXjdyEEjbRsY9PC-MgFG6xjCDbPu4IOAIOCXyPLirzjFWdo.; SUHB=00xZwj0czv30Gl; Ugrow-G0=56862bac2f6bf97368b95873bc687eef; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; YF-Page-G0=86b4280420ced6d22f1c1e4dc25fe846; YF-V5-G0=a9b587b1791ab233f24db4e09dad383c; wb_view_log_6382564064=1920*10801; _s_tentry=-; Apache=2872156489358.7036.1542848804714; ULV=1542848804736:6:6:3:2872156489358.7036.1542848804714:1542706013869; _T_WM=3e8b91cb0fc1afc6f6b197111618f23a; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9Wh3SFjwsRGoBE8ZBHKOX.cV5JpVF02RehnESKe41h24; SUB=_2AkMsqrpQdcPxrAVSkPoQym_iaolH-jyff9OmAn7uJhMyAxgv7nNeqSVutBF-XJVarBSeGUU5IPLleV-08g-rwQpV; login_sid_t=a2b0e92dbac53ded77a3b3a4328efdaa; cross_origin_proto=SSL; WBStorage=f44cc46b96043278|undefined; UOR=,,login.sina.com.cn; wb_view_log=1920*10801',
        'Host': 'weibo.com',
        'Referer': 'https://weibo.com/2889942201/GFo7omJqz?type=comment',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    a = get_location()

    sq_id = IO_rw()
    id = sq_id.process_item()
    #print(id)
    print(len(id))
#select * from temp_1

    scouce = {4298971540840704: '法制日报', 4298989816221761: '成都这点事', 4299075702378443: '澎湃新闻', 4299418075146118: '蓝鲸财经记者工作平台',
     4299076473993416: '头条新闻', 4299003476719307: '新京报', 4298998359639309: '新京报我们视频', 4298973378181968: '锋潮科技',
     4299080815406936: '凤凰网视频', 4298982337445859: '老徐时评', 4298996928897636: '环球时报', 4299406599766183: '新京报我们视频',
     4299000293571112: '头条新闻', 4299063618905257: '凯雷', 4299022045365996: '时间视频', 4299009805606128: '成都文理学院',
     4299013086352881: '环球网', 4298641625417843: '直播成都', 4299011664045877: '北京青年报', 4299423812784809: '新京报',
     4299082115420281: '蓝鲸财经记者工作平台', 4298997394909242: '头条新闻', 4299439852536956: '界面', 4298989430127358: '梨视频'}


    dict_kaka = {'4298971540840704':'4298971540840700','4298973378181968':'4298973378181960','4298982337445859':'4298982337445850','4298989430127358':'4298989430127350',
                 '4299075702378443':'4298989816221760','4298996928897636':'4298996928897630','4298997394909242':'4298997394909240','4299000293571112':'4299000293571110',
                 '4299406599766183':'4298998359639300','4299013086352881':'4299001912862650','4299423812784809':'4299003476719300','4299009805606128':'4299009805606120',
                 '4299011664045877':'4299011664045870','4299011664045877':'4299011664045870','4299022045365996':'4299022045365990','4299063618905257':'4299063618905250',
                 '4299075702378443':'4299075702378440','4299080815406936':'4299080815406930','4299082115420281':'4299082115420280','4299406599766183':'4299406599766180',
                 '4299082115420281':'4299418075146110','4299406599766183':'4299423812784800','4299439852536956':'4299439852536950'}

    #重点微博大咔
    #dirt_id = {'4299423812784809': '4307760998861888', '4298641625417843': '4310355239287474', '4298989816221761': '4304012913833423', '4299080815406936': '4310928705430116', '4299439852536956': '4300603800872111', '4298998359639309': '4308205515941261', '4299003476719307': '4299701576388896', '4299406599766183': '4300644934158879'}
    dirt_id = {'4299418075146118': '4299846586743814', '4299423812784809': '4307760998861888',
               '4298996928897636': '4310362948039865', '4299009805606128': '4310566774816676',
               '4298982337445859': '4308161407894835', '4299022045365996': '4309604827130660',
               '4298641625417843': '4310355239287474', '4299013086352881': '4299307195064641',
               '4298989816221761': '4304012913833423', '4298971540840704': '4299716550047906',
               '4299080815406936': '4310928705430116', '4299075702378443': '4303543387120975',
               '4299063618905257': '4305250707383790', '4299439852536956': '4300603800872111',
               '4298973378181968': '4308019552712965', '4299082115420281': '4299577743524389',
               '4299076473993416': '4303495751918534', '4298998359639309': '4308205515941261',
               '4298989430127358': '4311085508508944', '4298997394909242': '4311251749949443',
               '4299003476719307': '4299701576388896', '4299000293571112': '4300423923977119',
               '4299406599766183': '4300644934158879', '4299011664045877': '4299105578278556'}

    url = "https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id={}&max_id={}"
    url_page = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id={}&max_id={}&page={}'   #拼接下一页评论的url
    oneself = 'https://weibo.com/{}'

    try:
        for i in dirt_id.keys():
            url1 = url.format(i,dirt_id[i])    #拼接每一个博主的 url
            print("每一个博主的url, 一般是首页。为了拿到一共有多少页面。",url1)
            page = a.page_parse(a.get_html(url1))   #拿到每一个博主的页码总数。
            print("每一个微博 博主的转发了页数",page)

            for j in range(1,page + 1):  #拿到页面 数以后进行遍历。
                page_url = url_page.format(i,dirt_id[i],j)             #循环拼接每一页。
                print("每一页的id的url:",page_url)
                id_list,time_list = a.parse(a.get_html(page_url))   #每一页有20个左右的用户id、拿到每一个用户的id。
                print("每一个微博 博主的转发了页数,上面的id", id_list)
                for i in id_list:
                    for m in id:
                        print("i***********",i)
                        print("m----------------",m)
                        # if i == m:
                            #print(m,dict_kaka.get(i))
                            #sq_id.cun_item(m,dict_kaka.get(i))
    except:
        pass