# 调用的requests库和BeautifulSoup库中的bs4工具
import requests
from bs4 import BeautifulSoup

# 定义条数的初始值
num = 0
for page in range(20):
    # 定义爬取网页的start变量值
    start_value = page * 20
    # 定义变量存储爬取网页的url
    url="https://movie.douban.com/subject/27119724/comments?start=%s&limit=20&sort=new_score&status=P" %str(start_value)
    # 获取request对象
    req = requests.get(url, {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'})
    # 生成一个BeautifulSoup对象，用以后边的查找工作
    soup = BeautifulSoup(req.text, 'lxml')
    # 找到所有p标签中的内容并存放在xml这样一个类似于数组队列的对象中
    xml = soup.find_all('span', class_='short')

    # 利用循环将xml[]中存放的每一条打印出来
    for i in range(len(xml)):
        msg = xml[i].string
        if not msg is None:
            num += 1
        print('第', num, '条', msg)