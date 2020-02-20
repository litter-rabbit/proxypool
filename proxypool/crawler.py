
from proxypool.utils import get_page
import re
from pyquery import PyQuery as pq

class ProxyMetaclass(type):

    def __new__(cls,name,bases,attrs):
        count=0
        attrs['__CrawlFunc__']=[]
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1

        attrs['__CrawlFuncCount__']=count
        return type.__new__(cls,name,bases,attrs)






class Crawler(object,metaclass=ProxyMetaclass):


    def __init__(self):

        pass

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies


    def crawl_daili66(self,page_count=6):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        headers={
            'Cookie': 'Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1582115074; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1582118367',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
        }

        for url in urls:
            html = get_page(url,options=headers)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])


    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address+':'+ port
                yield result.replace(' ', '')

    def crawl_kuaidaili(self):
        # 只能爬取到第一页

        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            headers={
                'Cookie': 'channelid=0; sid=1582120905958238; _ga=GA1.2.572557590.1582121272; _gid=GA1.2.79681358.1582121272; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1582121272; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1582121391'
            }
            html = get_page(start_url,options=headers)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')



    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host':'www.xicidaili.com',
                'Referer':'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests':'1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')

    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')



    # def crawl_zdaye(self):
    #
    #     url='https://www.zdaye.com/FreeIPList.html'
    #     headers={
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'acw_tc=781bad0a15821228612455780e445f7a73355e967e76647dd78323b6b4669a; __51cke__=; Hm_lvt_80f407a85cf0bc32ab5f9cc91c15f88b=1582122861; acw_sc__v2=5e4d4775abbaedc46b24e374f5a7f32552fa80eb; acw_sc__v3=5e4d47751799a7ada3a403d662d7005e27ff6ed2; ASPSESSIONIDCGACBQBQ=NEKHFDKCNEAHMKIPCINOKKPJ; __tins__16949115=%7B%22sid%22%3A%201582122860862%2C%20%22vd%22%3A%2012%2C%20%22expires%22%3A%201582124773547%7D; __51laig__=12; Hm_lpvt_80f407a85cf0bc32ab5f9cc91c15f88b=1582122974',
    #         'Host': 'www.zdaye.com',
    #         'Referer': 'https://www.zdaye.com/',
    #         'Sec-Fetch-Dest': 'document',
    #         'Sec-Fetch-Mode': 'navigate',
    #         'Sec-Fetch-Site': 'same-origin',
    #         'Sec-Fetch-User': '?1',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    #     }
    #
    #     proxies={
    #         'http':'http://171.35.162.92:9999'
    #     }
    #
    #     html=get_page(url,options=headers,proxies=proxies,verify=False)
    #     print(html)










    def test_daili66(self):
        for item in self.crawl_daili66(1):
            print(item)

    def test_daili3366(self):
        for item in self.crawl_ip3366():
            print(item)

    def test_kuaidaili(self):
        for item in self.crawl_kuaidaili():
            print(item)

    def test_xizidaili(self):
        for item in self.crawl_xicidaili():
            print(item)

    def test_iphai(self):
        for item in self.crawl_iphai():
            print(item)

    def test_zdaye(self):
        for item in self.crawl_zdaye():
            print(item)







if __name__ == '__main__':

    crawl=Crawler()
    crawl.test_zdaye()










