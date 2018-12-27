import os
import requests
from bs4 import BeautifulSoup
import re
from subprocess import call

path = "./back_up/"
url = "https://www.cnblogs.com/yunlambert/p/"
model = 'http://equations.online/'

def download(DownUrl,DownPath,OutPutFileName):
    IDM=r'D:\yun_install_software\IDM\IDMan.exe'
    DownPath=r'E:\workstation\Github\Blog_Pictures'
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
        print('访问 http 发生错误... ')
        return None

def get_article_url():
    pass

def main():
    folder=os.path.exists(path)
    if not folder:
        os.makedirs(path)
    html=get_url(url)
    soup=BeautifulSoup(html,"lxml")

    
    post_page_1 = soup.find_all(name='div', attrs={"class": "Pager"})
    post_pages=post_page_1.a.get('href')
    Dictionary_post_page = {}

    for i in range(0,len(post_page)) :
        link=post_page[i]

    i = 0
    for posts in post_page:
        # 去除标题的前后空格
        title = post[i].h2.get_text()
        subject = re.sub("\A\s+", "", title)
        post_title = re.sub("\s+\Z", "", subject)

        post_url = model + post[i].a.get('href')
        Dictionary_post[post_title] = post_url
        i += 1

    # 解析每一篇博客段落中的图片
    img_url_list = []
    for key, value in Dictionary_post.items():
        print(key + ':' + value)
        all_html = get_one_page(value)
        soup = BeautifulSoup(all_html, "lxml")

        replace_pattern = r'<[img|IMG].*?/>'  # img标签的正则式
        img_url_pattern = r'.+?src="(\S+)"'  # img_url的正则式

        # 只在段落中查找图片
        need_replace_list = re.findall(replace_pattern, str(soup.find_all('p')))  # 找到所有的img标签
        for tag in need_replace_list:
            if re.findall(img_url_pattern, tag) != []:
                if re.findall(img_url_pattern, tag)[0][1:4] != "img":  # 这里去除掉引用相对路径的图片，因为这些图片在我的仓库里，不需要备份
                    mkdir(r"equation_blog" + '\\' + key)  # 按博客标题生成文件夹
                    download_path = '\\' + key + '\\'
                    download_name = re.findall(img_url_pattern, tag)[0].split('/')[-1]
                    download_IDM(re.findall(img_url_pattern, tag)[0], download_path, download_name)
                    print(re.findall(img_url_pattern, tag)[0])
                    img_url_list.append(re.findall(img_url_pattern, tag)[0])  # 找到所有的img_url


if __name__ == "__main__":
    main()