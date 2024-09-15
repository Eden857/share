import requests
import asyncio
import aiohttp
import time
import aiofiles
from lxml import etree


def get_list(url):   #常用爬虫获取详情页链接和章节名称
    url_li = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
    }
    # proxies = {
    #     'https':'222.74.73.202'
    # }
    resbans = requests.get(url=url,headers=headers).text
    # re = resbans.encode('iso-8859-1').decode('gbk')  # 处理乱码问题（有效）
    tree = etree.HTML(resbans)
    name = tree.xpath('//*[@id="dir"]/dd/a/@title')
    url_list = tree.xpath('//*[@id="dir"]/dd/a/@href')
    for urls,name_ in zip(url_list,name):
        new_url = 'https://hetushu.com'+urls
        dic = {
            'name':name_,
            'url':new_url
        }
        url_li.append(dic)
    return url_li




async def get_ever(url):  # 异步实现的主要函数（功能函数）
    # time.sleep(0.3)  # 尝试休眠时间解决封IP问题（失败！！！） 但不排除网络问题
    # proxies = {
    #     'https': '222.74.73.202'   #代理IP方案
    # }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
    }
    print(f'开始下载{url["name"]}')
    try:
        while 1:
            async with aiohttp.ClientSession() as session:
                async with session.get(url['url'], headers=headers) as databases:
                    data = await databases.text()
                    # datas = data.encode('iso-8859-1').decode('gbk')
                    tree = etree.HTML(data)
                    text = '\n'.join(tree.xpath('//div[@id="content"]/div/text()'))
                    async with aiofiles.open(f'末日蟑螂/{url["name"]}.txt',mode='w',encoding='utf-8') as fp:
                        await fp.write(text)
                        print(f'{url["name"]}下载完成！！')
                        break
    except :
        print(f'再来一次{url["name"]}')




async def downlo(url_list):  # 封装任务函数
    desk = []
    for url in url_list:
        t = asyncio.create_task(get_ever(url))
        desk.append(t)
    await asyncio.wait(desk)
def main():  # 启动函数
    url = "https://hetushu.com/book/74/index.html"
    url_list = get_list(url)
    asyncio.get_event_loop().run_until_complete(downlo(url_list))

if __name__ == '__main__':  # 程序入口
    star = time.time()
    main()
    print('总耗时：', time.time() - star)
