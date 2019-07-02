# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

#获取每本书的章节内容
def get_chapter(url):
    # 获取网页的源代码
    html = urllib.request.urlopen(url)
    content = html.read().decode('utf8')
    html.close()
    # 将网页源代码解析成HTML格式
    soup = BeautifulSoup(content, "lxml")
    title = soup.find('h1').text    #获取章节的标题
    text = soup.find('div', id='htmlContent')    #获取章节的内容
    #处理章节的内容，使得格式更加整洁、清晰
    content = text.get_text('\n','br/').replace('\n', '\n    ')
    content = content.replace('　　', '\n　　')
    return title, '    '+content

def main():
    # 书本
    book = '笑傲江湖'
    order = 5
    for num in range(185,225):
        # 构造爬取地址
        url = "http://jinyong.zuopinj.com/%s/%s.html"%(order,num)
        # 错误处理机制
        try:
            title, chapter = get_chapter(url)
            # 写入文件
            with open('./笑傲江湖.txt', 'a', encoding='utf8') as f:

                print(book+':'+title+'-->写入成功！')
                f.write(title+'\n\n\n')
                f.write(chapter+'\n\n\n')
        except Exception as e:
            print(e)
    print('全部写入完毕!')

main()