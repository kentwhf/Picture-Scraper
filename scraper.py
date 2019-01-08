import multiprocessing as mp
import time
import requests
from bs4 import BeautifulSoup
import re
import os
import asyncio
import aiohttp
from urllib.request import urljoin, urlopen

label = 0
base_url = 'https://bbs.hupu.com/vote'  # A base url
unseen = {base_url}
seen = set()


def update_base_url(num):
    """
    Add urls of different pages by given index
    """
    for i in range(num):
        unseen.add(base_url + '-' + str(num))


async def crawl(url, session):
    """
    Crawl the text with the url
    """
    r = await session.get(url)
    html = await r.text()
    return html


def parse(html):
    """
    Parse the text with the url
    """
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {'class': "truetit"})
    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    return page_urls


def get_downloaded(s: str):
    """
    return a list that only contains jpg. url
    """
    list_ = s.split('/')
    for i in range(len(list_)):
        if 'jpg' in list_[i]:
            for j in range(len(list_[i])):
                if list_[i][j:j + 3] == 'jpg':
                    list_[i] = list_[i][:j + 3]
                    return '/'.join(list_[:i + 1])


def download(imgs: BeautifulSoup, tag: str, page_url):
    """
    Download the jpg. pictures with page_url
    """
    global label
    for img in imgs:
        label += 1
        url = img[tag]
        downloaded = get_downloaded(url)
        if downloaded:
            print(page_url)
        print(downloaded)
        r = requests.get(downloaded, stream=True)
        with open('/Users/whf/PythonProjects/img/%s' % label + '.jpg', 'wb') as f:
            for chunk in r.iter_content(chunk_size=9999):
                f.write(chunk)
            print('Saved %s' % label + '.jpg')


async def execute(page_url, session):
    """
    Download exceution
    """
    r = await session.get(page_url)
    html = await r.text()
    soup = BeautifulSoup(html, 'lxml')
    img_ul = soup.find_all('div', {'class': 'quote-content'})
    os.makedirs('/Users/whf/PythonProjects/img/', exist_ok=True)
    for ul in img_ul:
        imgs_1 = ul.find_all(src=re.compile('.jpg'))
        imgs_2 = ul.find_all(attrs={'data-original': re.compile('.jpg')})
        # print(page_url)
        download(imgs_1, 'src', page_url)
        download(imgs_2, 'data-original', page_url)


async def main(loop):
    pool = mp.Pool(4)  # slightly affected
    async with aiohttp.ClientSession() as session:
        while len(unseen) != 0:

            print(unseen)

            print('\nAsync Crawling...')
            tasks = [loop.create_task(crawl(url, session)) for url in unseen]
            finished, unfinished = await asyncio.wait(tasks)
            htmls = [f.result() for f in finished]

            print('\nDistributed Parsing...')
            parse_jobs = [pool.apply_async(parse, args=(html,)) for html in htmls]
            results = [j.get() for j in parse_jobs]

            print('\nAnalysing...')
            for page_urls in results:
                page_urls -= seen
                for page_url in page_urls:
                    await loop.create_task(execute(page_url, session))
                seen.update(page_urls)
            unseen.clear()


if __name__ == '__main__':
    num_of_pages = '0'
    while not (1 <= int(num_of_pages) <= 100):
        num_of_pages = input("Select the number of pages being scraped : ")
    if num_of_pages == '1':
        num_of_pages = '0'
    update_base_url(int(num_of_pages))

    t1 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
    print("Async total time:", time.time() - t1)
