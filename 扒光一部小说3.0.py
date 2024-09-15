import requests
import asyncio
import aiohttp
import time
import aiofiles
from lxml import etree
def get_list(url,headers):
    url_list = []
    resbans = requests.get(url=url,headers=headers).text
    re = resbans.encode('iso-8859-1').decode('gbk')  #无需解码
    tree = etree.HTML(re)
    url_n = tree.xpath('//div[@id="list"]/dl/dd/a/@href')
    names = tree.xpath('//div[@id="list"]/dl/dd/a/text()')
    for urls,name in zip(url_n,names):
        dic = {
            'name':name,
            'url':urls
        }
        url_list.append(dic)
    return url_list


async def get_even(url,headers):
    print(f'开始下载{url["name"]}!!!')
    try:
        # count = 0
        while 1:
            # count = count + 1
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url['url'],headers=headers) as resbans:
                    data = await resbans.text()
                    # datas = data.encode('iso-8859-1').decode('gbk') #无需解码
                    tree = etree.HTML(data)
                    url_text = '\n'.join(tree.xpath('//div[@class="bookcontent clearfix"]/text()'))
                    async with aiofiles.open(f'三体全集/{url["name"]}.txt',mode='w',encoding='utf-8') as fp:
                        await fp.write(url_text)
                        print(f'下载完成{url["name"]}')
                        break
    except:
        print(f'重试一次{url["name"]}!!!')


async def dnwlod(url_list,headers):
    desk = []
    for url in url_list:
        t = asyncio.create_task(get_even(url,headers))
        desk.append(t)
    await asyncio.wait(desk)


def main(url,headers):
    url_list = get_list(url,headers)
    # asyncio.run(dnwlod(url_list))        # closed报错
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dnwlod(url_list,headers))


if __name__ == '__main__':
    url = 'https://www.qianyege.com/37/37428/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
    }
    star = time.time()
    main(url,headers)
    print(time.time()-star,'秒   爬取结束!!!')









