# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import re
import time
from subprocess import call

path = "./back_up/"
url = "https://www.cnblogs.com/yunlambert/p/"
model = 'http://equations.online/'


def download(DownUrl, DownPath, OutPutFileName):
    IDM = r'D:\yun_install_software\IDM\IDMan.exe'
    DownPath = r'E:\workstation\Github\Blog_Pictures\back_up'
    call([IDM, '/d', DownUrl, '/p', DownPath, '/f', OutPutFileName, '/n'])


def get_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return None
    except:
        print('Error open the page... ')
        return None


def get_pages(post_page):
    pages = []
    while True:
        try:
            post_pages = post_page.find_all(name="a")[-2].get('href')
            temp = get_url("https://www.cnblogs.com" + post_pages)
            post_page = BeautifulSoup(temp, "lxml")
            pages.append("https://www.cnblogs.com" + post_pages)
            # print(post_pages)
        except Exception as e:
            print(Exception, ":", e)
            break
    return pages


def main():
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    html = get_url(url)
    soup = BeautifulSoup(html, "lxml")

    post_page_1 = soup.find(name='div', attrs={"class": "Pager"})
    post_page = get_pages(post_page_1)
    post_page.insert(0, "https://www.cnblogs.com/yunlambert/p/?page=1")
    print(post_page)
    post_article = []

    for i in range(0, len(post_page)):
        link = post_page[i]
        page = BeautifulSoup(get_url(link), "lxml")
        try:
            article = page.find_all(name="div", attrs={"class": "postTitl2"})
            for j in range(0, len(article)):
                post_article.append(article[j].a.get("href"))

        except Exception as e:
            print(Exception, ":", e)
            continue
    print(post_article)

    img_url_list = []
    for i in range(0, len(post_article)):
        print("new article....")
        m = get_url(post_article[i])
        soup_article = BeautifulSoup(m, "lxml")

        replace_pattern = r'<[img|IMG].*?/>'  # img标签的正则式
        img_url_pattern = r'.+?src="(\S+)"'  # img_url的正则式

        # 只在段落中查找图片
        need_replace_list = re.findall(replace_pattern, str(soup_article.find_all('p')))  # 找到所有的img标签
        for tag in need_replace_list:
            if re.findall(img_url_pattern, tag) != []:
                # mkdir(r"equation_blog" + '\\' + key)  # 按博客标题生成文件夹
                download_path = "E:\\workstation\\Github\\Blog_Pictures\\back_up\\"
                # download_name = re.findall(img_url_pattern, tag)[0].split('/')[-6]
                now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
                download_name = now + ".png"
                download(re.findall(img_url_pattern, tag)[0], download_path, download_name)
                print(re.findall(img_url_pattern, tag)[0])
                img_url_list.append(re.findall(img_url_pattern, tag)[0])  # 找到所有的img_url


if __name__ == "__main__":
    main()
