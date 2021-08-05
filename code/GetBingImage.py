# -*- coding: utf-8 -*-
"""
Function:   Get Bing daily wallpaper from https://bing.ioliu.cn/
Author:     hjd
Date:       2021.7.29
Update:     2021.7.29
Reference:  https://blog.csdn.net/HelloWorldTM/article/details/107049627
Improvement:
    1. Encapsulated functions as classes.
    2. Added the function of judging and skipping crawled pictures.
    3. Handled the exception that failed to download pictures. I just skiped the image. 
"""

import re
import requests
from bs4 import BeautifulSoup
from time import sleep
import os


class GetBingImage:
    
    def __init__(self, url, pic_path):
        self.url = url
        self.pic_path = pic_path
        
    def GetHtmlText(self, url):
        # 根据传入的url请求网站，并返回得到的数据
        try:
            # 模拟浏览器拉取数据，防止被识别为爬虫并禁掉
            user_agent = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
            html_text = requests.get(url, headers = user_agent)
            html_text.encoding = html_text.apparent_encoding
            html_text.raise_for_status()
        except:
            print('网页获取失败：', html_text.status_code)
            return None
        return html_text
    
    def GetMaxPageCount(self):
        # 获取主页信息，并且获取网站的最大页数 
        soup = BeautifulSoup(self.GetHtmlText(self.url).text, "html.parser")
        tag_page = soup.find('div', {'class':'page'})
        page_txt = None
        for tag_child in tag_page.children:
            if(tag_child.name == 'span'):
                page_txt = tag_child.string
                match = re.search(r'(?<=1 / )\d*', page_txt)
                max_page_count = int(match.group(0))
        return max_page_count
        
    def SavePictureInUrl(self, pic_url, pic_name):
        # 根据传入的url链接获取图片的二进制数据，并且根据传入的路径和文件名将文件写入到对应的路径中
        source = self.GetHtmlText(pic_url)
        if source == None:
            return 
        file_name = '{}.jpg'.format(pic_name)
        try:
            with open(self.pic_path+file_name, 'wb') as f:
                f.write(source.content)
            sleep(0.005)
        except OSError:
            print("此图片下载失败！")
            

    def GetOnePageJpg(self, page_count):
        # 从返回的网页数据中获取每张图片的相关信息以及图片下载的url，然后调用相关函数下载图片
        url = 'https://bing.ioliu.cn/?p={}'.format(page_count)
        soup = BeautifulSoup(self.GetHtmlText(url).text, 'html.parser')
        tag_container = soup.find_all('div', {'class':'container'})
        tag_item = tag_container[1]
        for tag_pic in tag_item.children:
            # 获取图片的标题和日期信息并且拼接成图片名
            tag_title = tag_pic.find('h3')
            text_title = tag_title.string
            a = re.findall(r'[^\*"/:?\\|<>]', text_title, re.S)      #剔除某些不能作为文件名的特殊字符
            text_title = ''.join(a)
            tag_calendar = tag_pic.find('p', {'class':'calendar'})
            tag_em = tag_calendar.find('em')
            text_calendar = tag_em.string
            text_pic_name = text_calendar + '__' + text_title
            if(os.path.exists(self.pic_path+text_pic_name+'.jpg')):
                continue
            # 获取图片的下载url
            tag_download = tag_pic.find('a', {'class':'ctrl download'})
            pic_url = self.url + tag_download['href']
            #信息保存到图片中
            self.SavePictureInUrl(pic_url, text_pic_name)
            print('.', end='', flush=True)        #输出进度信息

    def GetAllPageJpg(self):
        # 爬取所有的图片，并保存在输入的路径参数下
        max_page_count = self.GetMaxPageCount()
        for page_index in range(1, max_page_count):
            self.GetOnePageJpg(page_index)
            print('\r', '正在获取，已完成：{:.2f} %'.format(page_index/max_page_count*100), end = '', flush=True)      #输出进度信息


def main():
    url = 'https://bing.ioliu.cn/'     
    pic_path = 'E:/学习资料/Python/code/必应每日壁纸/'  
    getBingImg = GetBingImage(url, pic_path)
    getBingImg.GetAllPageJpg()
        
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    