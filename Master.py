import requests
from lxml import etree
import ReqMold
import time
import re
import json
from functools import reduce
import logging
logging.basicConfig(level=logging.INFO)

START_URL = "https://club.autohome.com.cn/#pvareaid=103419"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}
CAR_ID = ["1522733408317","1522733407861","1522733407141","1522733406653","1522733406246","1522733405126","1522733404515","1522733404070","1522733403654","1522733403193","1522733402753","1522733402350","1522733401907","1522733401335","1522733400406","1522733399943","1522733399461","1522733398969","1522733398551","1522733398006","1522733397574","1522733397160","1522733396704","1522733396047","1522733395434"]

class Master_Spider():
    def __init__(self):
        self.req = ReqMold.Req()
    def mainbbs_res(self):
        res = self.req.common_get(START_URL)
        return res
    def mainbbs_parse(self):
        html = etree.HTML(self.mainbbs_res())
        name_items = html.xpath('//div[@class="forum-brand-box"]/p/text()')
        info_items = html.xpath('//div[@class="forum-brand-box"]/ul')
        print(name_items)
        print(info_items)
        nam_info = dict(zip(name_items,info_items))
        dic2list = []
        for i,j in nam_info.items():
            a = dict()
            logging.info(j.xpath('li/a/text()'))
            b = [{k:l} for (k,l) in zip(j.xpath('li/a/text()'),j.xpath('li/a/@href'))]
            logging.info(b)
            a[i] = b
            logging.info(a)
            dic2list.append(a)
        return dic2list
    def car_bbs_req(self,urls):
        html_list = self.req.MT_run(urls)
        f = open("cat.html","w",encoding="utf-8")
        f.write(html_list[0])
        return html_list
    def car_bbs_parse(self,html_list):
        car_bbs_data = dict()
        etr_html_list = (etree.HTML(i) for i in html_list)
        for j in etr_html_list:
            a = j.xpath('//div[@id="subcontent"]/dl[@class="list_dl"]')
            id_list = []
            data_pool = []
            for k in a:
                title = k.xpath('dt/a[1]/text()')
                url = k.xpath('dt/a[1]/@href')
                post_time = k.xpath('dd[1]/span/text()')
                lang_id = k.xpath('dd[2]/@lang')
                latest_post = k.xpath('dd[3]/span/text()')
                data = {"title":title,"link":url,"post_time":post_time,"lang_id":lang_id,"latest_post":latest_post}
                data_pool.append(data)
                id_list.extend(lang_id)
            logging.info(data_pool)
            logging.info(len(data_pool))
            id_data=self.reply_view(id_list)
            logging.info(id_data)
            logging.info(len(id_data))
            self.data_process(data_pool,id_data)
            logging.info(data_pool)
            return data_pool
    def data_process(self,raw_data,id_data):
        for i in id_data:
            for j in raw_data:
                if i["topicid"] == int(j["lang_id"][0]):
                    j["re_vi_num"] = [i["replys"],i["views"]]
                else:
                    continue
    def reply_view(self,lang_id_list):
        url = "https://clubajax.autohome.com.cn/topic/rv?fun=jsonprv&callback=jsonprv&ids={ids}&r={timeid}+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&callback=jsonprv&_={time_chuo}"
        param_id = [i + "%2C" for i in lang_id_list]
        ids = reduce(lambda x, y: x + y, param_id)
        ctim = time.asctime(time.localtime(time.time())).split()
        ctim[-2], ctim[-1] = ctim[-1], ctim[-2]
        ctim[-1] = "%3A".join(ctim[-1].split(":"))
        timeid = "+".join(ctim)
        time_chuo = str(int(time.time() * 1000))
        revi_url = url.format(ids=ids, timeid=timeid, time_chuo=timeid)
        resp = requests.get(revi_url)
        revi_data = eval(re.findall(r'onprv(.*?)$', resp.text)[0])
        return revi_data
if __name__ == '__main__':
    m = Master_Spider()
    test_urls = ["https://club.autohome.com.cn/bbs/forum-c-66-2.html?orderby=dateline&qaType=-1#pvareaid=101061","https://club.autohome.com.cn/bbs/forum-c-66-3.html?orderby=dateline&qaType=-1#pvareaid=101061"]
    aa = m.car_bbs_req(test_urls)
    bb = m.car_bbs_parse(aa)



