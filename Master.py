import requests
from lxml import etree
import ReqMold

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
        # func = lambda x:[{i.xpath('@title'):i.xpath("@href")} for i in x.xpath('li/a')]
        # inf= [{name_items[i]:info_items[i]} for i in range(len(name_items))]
        # aaa = [{j.xpath('@title'):j.xpath('@href')} for j in info_items[2].xpath('li/a')]
        print(info_items)
        aaa = info_items[2].xpath('li/a')

        # inf= [{name_items[i]:[{j.xpath('@title'):j.xpath('@href')} for j in info_items[i].xpath('li/a')]} for i in range(len(name_items))]
        print(aaa)
        # test_list = []
        # test = map(func,test_list)
        # print(test)





if __name__ == '__main__':
    m = Master_Spider()
    m.mainbbs_parse()



