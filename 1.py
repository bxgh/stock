# -*- coding:utf-8 -*-
import requests
import json
import time
import re
from selenium import webdriver
from itchat import proxy_mine
 
class BaiduYunTransfer:
 
    headers = None
    bdstoken = None
    pro = proxy_mine.Proxy()
 
    def __init__(self,bduss,stoken,bdstoken):
        self.bdstoken = bdstoken
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '161',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'BDUSS=%s;STOKEN=%s;' % (bduss, stoken),
            'Host': 'pan.baidu.com',
            'Origin': 'https://pan.baidu.com',
            'Referer': 'https://pan.baidu.com/s/1dFKSuRn?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0',
            'User-Agent': self.pro.get_user_agent(),
            'X-Requested-With': 'XMLHttpRequest',
        }
 
    def transfer(self,share_id,uk,filelist_str,path_t_save):
        # 通用参数
        ondup = "newcopy"
        async = "1"
        channel = "chunlei"
        clienttype = "0"
        web = "1"
        app_id = "250528"
        logid = "你的logid"
 
        url_trans = "https://pan.baidu.com/share/transfer?shareid=%s" \
                    "&from=%s" \
                    "&ondup=%s" \
                    "&async=%s" \
                    "&bdstoken=%s" \
                    "&channel=%s" \
                    "&clienttype=%s" \
                    "&web=%s" \
                    "&app_id=%s" \
                    "&logid=%s" % (share_id, uk, ondup, async, self.bdstoken, channel, clienttype, web, app_id, logid)
 
        form_data = {
            'filelist': filelist_str,
            'path': path_t_save,
        }
 
        proxies = {'http': self.pro.get_ip(0, 30, u'国内')}
 
        response = requests.post(url_trans, data=form_data, proxies = proxies,headers=self.headers)
        print(response.content)
 
        jsob = json.loads(response.content)
 
        if "errno" in jsob:
            return jsob["errno"]
        else:
            return None
 
    def get_file_info(self,url):
        driver = webdriver.Chrome()
        print ("初始化代理...")
        driver = self.pro.give_proxy_driver(driver)
 
        print ("初始化代理...")
        driver.get(url)
        time.sleep(1)
        print ("初始化代理...")
        driver.get(url)
        print ("初始化代理...")
        script_list = driver.find_elements_by_xpath("//body/script")
        innerHTML = script_list[-1].get_attribute("innerHTML")
 
        pattern = 'yunData.SHARE_ID = "(.*?)"[\s\S]*yunData.SHARE_UK = "(.*?)"[\s\S]*yunData.FILEINFO = (.*?);[\s\S]*'  # [\s\S]*可以匹配包括换行的所有字符,\s表示空格，\S表示非空格字符
        srch_ob = re.search(pattern, innerHTML)
 
        share_id = srch_ob.group(1)
        share_uk = srch_ob.group(2)
 
        file_info_jsls = json.loads(srch_ob.group(3))
        path_list_str = u'['
        for file_info in file_info_jsls:
            path_list_str += u'"' + file_info['path'] + u'",'
 
        path_list_str = path_list_str[:-1]
        path_list_str += u']'
 
        return share_id, share_uk, path_list_str
 
    def transfer_url(self,url_bdy,path_t_save):
        try:
            print ("初始化代理...")
            share_id, share_uk, path_list = self.get_file_info(url_bdy)
        except:
            print ("初始化代理.ddd..")
        else:
            error_code = self.transfer(share_id, share_uk, path_list, path_t_save)
            if error_code == 0:
                print ("初始化代理...")
            else:
                print (str(error_code))
 
bduss = '你的BDUSS'
stoken = '你的STOKEN'
bdstoken = "你的bdstoken"
bdy_trans = BaiduYunTransfer(bduss,stoken,bdstoken)
 
# url_src = "https://pan.baidu.com/s/1jImSOXg"
# path = u"/电影"
 
# bdy_trans.transfer_url(url_src,path)