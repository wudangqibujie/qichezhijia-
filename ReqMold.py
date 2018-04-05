from selenium import webdriver
import time
import asyncio
import aiohttp
from lxml import etree
import requests
import threading
import logging
import multiprocessing as mp
from queue import Queue
from functools import wraps
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
class Req():
    def browser_get(self,url):
        br = webdriver.Chrome()
        br.get(url)
        time.sleep(10)
        return br.page_source
    #q用于多进程
    def common_get(self,url,q=None):
        logging.info("正在进行常规requests请求")
        try:
            r = requests.get(url)
            logger.info("请求成功！")
            return r.text
        except requests.exceptions.ConnectionError as e:
            logger.info("发生连接错误")
        except requests.exceptions.Timeout as e:
            logger.info("发生连接超时")
        except requests.exceptions.ProxyError as e:
            logger.info("代理IP有问题")
        #元组内捕捉多个异常
        # except (requests.exceptions.ConnectionError ,requests.exceptions.Timeout ,requests.exceptions.ProxyError ):
        #     logging.info("")
        except Exception as e:
            logging.info(e)
        finally:
            if q == None:
                pass
            else:
                q.put(r.text)
    #用多进程的map方法取结果，返回的是一个列表
    def MP_get(self,func,urls):
        pool = mp.Pool()
        res = pool.map(func,urls)
        return res
    #运用apply_async方法获取结果,输进去单个参数
    def multi_pro_get2(self,func,url):
        pool = mp.Pool()
        res = pool.apply_async(func,(url,))
        return res.get()
    #运用apply_async方法，但是输出多个参数
    def multi_pro_get3(self,func,urls):
        pool = mp.Pool()
        multi_list = [pool.apply_async(func,(url,)) for url in urls]
        return (res.get() for res in multi_list)#这里返回的是一个迭代器
    #url放在列表容器
    def MP_run(self,urls):
        res1 = self.MP_get(self.common_get,urls)
        return res1#返回的响应网页代码放在列表容器
    #使用多线程
    def MT_get(self,func,urls,q):
        result = []
        thre_list = [threading.Thread(target=func,args=(url,q)) for url in urls]
        for i in thre_list:
            i.start()
        for i in thre_list:
            i.join()
        for i in thre_list:
            result.append(q.get())
        return result
    #运行多线程,url放在列表容器
    def MT_run(self,urls):
        q = Queue()
        resp = self.MT_get(self.common_get,urls,q)
        return resp#返回的网页源代码放在列表容器
    #使用异步请求
    async def getPage(self,url,page_lists):
        async with aiohttp.ClientSession() as resp:
            async with resp.get(url) as resp:
                page = await resp.text("utf-8","ignore")
                return page
    #输入url列表
    def asyn_run(self,urls):
        page_lists = []
        loop = asyncio.get_event_loop()
        tasks = [self.getPage(host,page_lists) for host in urls]
        loop.run_until_complete(asyncio.wait(tasks))
        return page_lists#返回网页源代码列表

if __name__ == '__main__':



    url = "https://club.autohome.com.cn/bbs/forum-c-66-{}.html?orderby=dateline&qaType=-1#pvareaid=101061"
    urls = [url.format(str(i)) for i in range(1,3)]
    print(urls)
    a = Req()
    p1 = time.time()
    ol=a.asyn_run(urls)
    print("协程用时",time.time()-p1)

    # we = a.MT_run(urls)
    # print(we)


    # p2 = time.time()
    # ll = []
    # for i in urls:
    #     h = a.common_get(i)
    #     # print(h)
    # print("普通用时",time.time()-p2)







