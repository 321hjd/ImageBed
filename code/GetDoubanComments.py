# -*- coding: utf-8 -*-
"""
Function:   Crawl comments on douban
Author:     hjd
Date:       2021.8.1
Update:     2021.8.4 22:41
Reference:  
"""

import re
import requests
from bs4 import BeautifulSoup
from time import sleep


class GetDoubanComments:
    
    def __init__(self, url, path, pages):
        self.url = url
        self.path = path
        self.pages = pages
        
    def GetHtmlText(self, url):
        # 根据传入的url请求网站，并返回得到的数据
        try:
            # 模拟浏览器拉取数据，防止被识别为爬虫并禁掉
            user_agent = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
            html_text = requests.get(url, headers = user_agent)
            html_text.encoding = html_text.apparent_encoding
            html_text.raise_for_status()
        except Exception:
            print('网页获取失败：', html_text.status_code)
            return None
        return html_text
    
    def GetNextPageAndCompleUrls(self, url):
        # 1.获取下一页评论的链接
        # 2.获取完整评论的链接
        
        # 获取主页信息，并且获取下一页评论的尾部链接
        soup = BeautifulSoup(self.GetHtmlText(url).text, "html.parser")
        tag_next = soup.find('span', {'class':'next'})
        match = re.search('href="(.*?)"', str(tag_next))
        next_page = self.url + match.group(0)[6:-1]        # 拼接下一页url如"?start=20"
        
        # 获取该页所有评论的完整评论链接
        tag_main = soup.find_all('div', {'class':'main-bd'})
        comple_urls = re.findall('<a href="(.*?)">', str(tag_main))
        return next_page, comple_urls
    
    def SaveComments(self, url):
        # 爬取所有评论并储存
        
        count = 1                           # 评论条数
        for i in range(self.pages):
            source = self.GetNextPageAndCompleUrls(url)
            url = source[0]                     # 下一页的链接
            comple_urls = source[1]             # 所有的评论链接,是一个大小为20的列表
            
            for comple_url in comple_urls:
                soup = BeautifulSoup(self.GetHtmlText(comple_url).content.decode('utf-8'), "html.parser")
                # 获取评论相关信息
                tag_article = soup.find('div', {'class':'article'})
                # 作者
                author = re.search('<span>(.*?)</span>',str(tag_article)).group(0)[6:-7]
                # 时间
                time = re.findall('<span class="main-meta".*?>(.*?)</span>', str(tag_article))[0]
                # 标题
                title = re.findall('<span property="v:summary">(.*?)</span>', str(tag_article))[0]
                # 正文
                content = re.findall('<p data-page="0">(.*?)</p>', str(tag_article), re.S)
                # 拼接并存储
                head = "标题: " + title + '\n' + "作者: " + author + '\n' + "日期: " + time + '\n'
                content = '\n'.join(content)
                article = head + content
                with open(self.path, 'a') as f:
                    f.write('--------------第{}条评论-----------------------\n'.format(count))
                    f.write(article)
                    f.write('\n\n')
                    print("写入第{}条评论".format(count))
                    count += 1
                    sleep(0.5)
                   

def main():
    url = 'https://movie.douban.com/subject/30174085/reviews'     
    path = 'E:/学习资料/Python/code/豆瓣评论/comments.txt'  
    pages = 3
    getDoubanComments = GetDoubanComments(url, path, pages)
    getDoubanComments.SaveComments(url)
        
    
if __name__ == '__main__':
    main()
    
    