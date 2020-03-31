from selenium import webdriver
import time
import re
import openpyxl as xl

browser = webdriver.Chrome()


# 存取爬的每一条微博的所有内容
contents = []


# log in the weibo website using mobile edition
def log_weibo(username, password):
    browser.get('https://passport.weibo.cn/signin/login')
    time.sleep(3)

    browser.find_element_by_id("loginName").send_keys(username)
    browser.find_element_by_id("loginPassword").send_keys(password)
    browser.find_element_by_id("loginAction").click()


# get the info of a specific user by user's id
def user_info(user_id):
    browser.get('http://weibo.cn/' + user_id)

    print('********************')
    print('用户资料')

    # 1.用户id
    print('用户id:' + user_id)

    # 2.用户昵称
    str_name = browser.find_element_by_xpath("//div[@class='ut']")
    strlist = str_name.text.split(' ')
    nickname = strlist[0]
    print('昵称:' + nickname)

    # 3.微博数、粉丝数、关注数
    str_cnt = browser.find_element_by_xpath("//div[@class='tip2']")
    pattern = r"\d+\.?\d*"  # 匹配数字，包含整数和小数
    cnt_arr = re.findall(pattern, str_cnt.text)
    print(str_cnt.text)
    print("微博数：" + str(cnt_arr[0]))
    print("关注数：" + str(cnt_arr[1]))
    print("粉丝数：" + str(cnt_arr[2]))

    print('\n********************')
    # 4.将用户信息写到文件里
    # with open("userinfo.txt", "w", encoding="gb18030") as file:
    #     file.write("用户ID：" + user_id + '\r\n')
    #     file.write("昵称：" + nickname + '\r\n')
    #     file.write("微博数：" + str(cnt_arr[0]) + '\r\n')
    #     file.write("关注数：" + str(cnt_arr[1]) + '\r\n')
    #     file.write("粉丝数：" + str(cnt_arr[2]) + '\r\n')


# # search weibos by the specific keywords and a period
# # all keywords contained -- &
# def search_by_keywords_and_date(keywords, date):
#     browser.get("https://weibo.cn/search/mblog?advanced=mblog&f=s")
#     key_input = browser.find_element_by_name('keyword')
#     for keyword in keywords:
#         key_input.send_keys(keyword + " ")
#     start_input = browser.find_element_by_name('starttime')
#     end_input = browser.find_element_by_name('endtime')
#     # the default end time is not empty
#     end_input.clear()
#     start_input.send_keys(date[0])
#     end_input.send_keys(date[1])
#     weibo_btn = browser.find_element_by_name('smblog')
#     weibo_btn.click()
#     # return the number of all blog
#     return browser.find_element_by_class_name('cmt').text


def search(keywords, date):
    url = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={0}&advancedfilter=1&hasori=1&starttime={1}&endtime={" \
          "2}&sort=time&page=1"
    keyword_url = ""
    # 嵌入关键词们和搜索的起止日期
    for keyword in keywords:
        keyword_url = keyword_url + keyword + "+"
    keyword_url = keyword_url[:-1]
    start_time = date[0]
    end_time = date[1]
    url = url.format(keyword_url, start_time, end_time)
    # 进入搜索页的第一页
    browser.get(url)
    return url


# 获取搜索结果中的信息
def get_info(url, file, sheet):
    # 设置url
    url = url[:-1]
    url += "{0}"
    # 获取当前页数/全部页数字符串
    page_text = browser.find_element_by_xpath("//div[@class='pa']")
    # print(page_text.text)
    # 匹配数字
    pattern = r"\d+\d*"
    page_array = re.findall(pattern, page_text.text)
    total_pages = int(page_array[1])
    # print(total_pages)

    # 当前爬取数据的页面
    curr_page = 1
    # 获取第一页
    browser.get(url.format(curr_page))
    # 微博内容至少从第4个class为c的div开始，保险起见设为3，之前发现cookie中有返回上一界面的记录
    # 其实就算有记录，也应该至少4没问题对吧
    # 可我就喜欢这样 我说3就3
    curr_wb = 3
    # 一条微博的x_path的格式
    content_xpath = "//div[@class='c'][{0}]"
    # 用户名的x_path的格式
    username_xpath = ".//a[@class='nk']"
    # 微博正文的x_path的格式
    weibo_xpath = ".//span[@class='ctt']"
    # 时间的x_path的格式
    time_xpath = ".//span[@class='ct']"

    while curr_page <= 198:
        curr_content = browser.find_element_by_xpath(content_xpath.format(curr_wb))
        # 有内容的div是有id的
        curr_id = curr_content.get_attribute("id")
        if curr_id is not "":
            content = []
            curr_username = curr_content.find_element_by_xpath(username_xpath).text
            curr_weibo = curr_content.find_element_by_xpath(weibo_xpath).text[1:]
            curr_time = curr_content.find_element_by_xpath(time_xpath).text.split()
            curr_time = curr_time[0] + " " + curr_time[1]
            content.append(curr_username)
            content.append(curr_time)
            content.append(curr_weibo)
            sheet.append(content)
            file.save("data_weibo.xlsx")
            print(curr_username)
            print(curr_weibo)
            print(curr_time)
            print("")

        # 到底了，此页已经没有微博了，开始爬下一页儿
        if "设置:皮肤.图片.条数.隐私" in curr_content.text:
            print("第 ", curr_page, " 页完成")
            curr_page += 1
            curr_wb = 3
            # 等待20s避免被封号
            # time.sleep(1)
            browser.get(url.format(curr_page))
            continue
        curr_wb += 1


# def get_and_num(keywords):
#
#
#
# # 微博似乎没有或搜索，于是考虑使用容斥原理求数目
# # 由于我很懒 所以只求三个关键词的情况
# # A∪B∪C = A + B + C - A∩B - B∩C - C∩A + A∩B∩C
# def get_or_num(keywords):
# 由于我太懒了， 这个暂时也不写了


def run_and_write(keywords, date):
    file = xl.load_workbook("data_weibo.xlsx")
    title = ""
    for keyword in keywords:
        title = title + keyword + "_"
    file.create_sheet(title=title)
    sheet = file[title]
    url = search(keywords, date)
    get_info(url, file, sheet)


if __name__ == '__main__':
    log_weibo("15986931557", "8mv067ulsj")
    time.sleep(3)
    # # user_info("1191220232")  查看用户信息
    keywords = ["追我吧"]
    date = ["20191127", "20191227"]
    run_and_write(keywords, date)