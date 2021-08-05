# -*- coding: utf-8 -*-
"""
Function:   Get Baidu Images
Author:     hjd
Date:       2021.7.30
Update:     2021.7.30
Reference:  https://blog.csdn.net/qq_44921056/article/details/114174916
Features:
    1. Website of Baidu pictures have a mechanism of anti-crawler.
    2. Simulated the process of manual retrieval using a browser.
    3. Refer to the Reference link, I tried to grab the request header with the browser's packet capture tool:XHR. 
"""

import re
import requests
import urllib
from time import sleep


class GetBaiduImage:
    
    def __init__(self, url, path, keyword, page):
        self.url = url
        self.path = path
        self.keyword = keyword
        self.page = page
        self.pn = 1                  # pn代表从第几张图片开始获取，百度图片下滑时默认一次性显示30张
        # self.first = 1              # 代表从第几张图片开始获取，必应图片下滑时默认一次性显示30张
        
    def GetHtmlText(self):
        # 根据传入的url请求网站，并返回得到的数据
        param = {
            'tn': 'resultjson_com',
            'logid': ' 7517080705015306512',
            'ipn': 'rj',
            'ct': '201326592',
            'is': '',
            'fp': 'result',
            'queryWord': self.keyword,
            'cl': '2',
            'lm': '-1',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': '',
            'z': '',
            'ic': '',
            'hd': '',
            'latest': '',
            'copyright': '',
            'word': self.keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': '',
            'istype': '',
            'qc': '',
            'nc': '1',
            'fr': '',
            'expermode': '',
            'force': '',
            'cg': 'star',
            'pn': self.pn,
            'rn': '30',
            'gsm': '1e',
            }
    
# =============================================================================
#         # first 参数控制从第 first 张图开始（与百度图片的 pn 参数类似）
#         param = {
#             'q': self.keyword,
#             'first': self.first,
#             'count': '30',
#             'cw': '1177',
#             'ch': '593',
#             'relp': '35',
#             'tsc': 'ImageBasicHover',
#             'datsrc': 'I',
#             'layout': 'RowBased_Landscape',
#             'mmasync': '1',
#             'dgState': '',
#             'IG': '9D7CBFCB39434C9583EA8186FB044DAA',
#             'SFX': '3',
#             'iid': 'images.5571'
#             }
# =============================================================================
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        try:
            # 模拟浏览器拉取数据，防止被识别为爬虫并禁掉
            html_res = requests.get(self.url, headers=header, params=param)
            html_res.encoding = html_res.apparent_encoding
            html_res.raise_for_status()
            # html_res是响应response,text方法返回字符串形式的html,而content方法是直接拉取得到的字节类型数据,还需要手动解码为字符串
            # 当text()显示不正常时使用content.decoding('utf-8/gbk/gbk2312')
            html_text = html_res.content.decode('utf-8')          
        except:
            print('网页获取失败：', html_res.status_code)
            return None
        return html_text

    def GetImageUrls(self):
        html = self.GetHtmlText()
        with open('test.txt', 'w', encoding='utf-8') as f:
            f.write(html)
        # urls = re.findall('murl&quot;:&quot;(.*?)&quot;', html, re.S)     # 必应图片
        urls = re.findall('"thumbURL":"(.*?)"', html, re.S)     # 百度图片
        return urls

    def Download(self):
        name = 1
        for n in range(int(page)):   
            img_urls = self.GetImageUrls()
            for img_url in img_urls:
                try:
                    urllib.request.urlretrieve(img_url, path+'%s.jpg'%name)
                except Exception:
                    print("下载失败！")
                else:
                    sleep(0.5)
                    print('成功下载第%s张图片' % (str(name)))
                    name += 1
            # 下载下一页
            self.pn += 29       # 百度图片
            # self.first += 29    # 必应图片
   
    
if __name__ == '__main__':
    url = 'https://image.baidu.com/search/acjson?'
    path = 'E:/学习资料/Python/code/百度图片/'
    keyword = '风景壁纸'            # 想要搜索的图片
    page = '2'                     # 想要爬取几页
    imgobj = GetBaiduImage(url, path, keyword, page)
    imgobj.Download()
    

    
    
    