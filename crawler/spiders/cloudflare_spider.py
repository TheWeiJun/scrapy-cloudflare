# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import scrapy


class CloudflareSpider(scrapy.Spider):
    name = 'cloudflare_spider'
    custom_settings = {
        # "HTTPERROR_ALLOWED_CODES": [403],
        # "DOWNLOADER_MIDDLEWARES": {
        #     "crawler.middlewares.DownloaderMiddleware": 200,
        # },
        "DOWNLOAD_HANDLERS": {
            "http": "crawler.download_handler.CloudFlareDownloadHandler",
            "https": "crawler.download_handler.CloudFlareDownloadHandler",
        }
    }

    def __init__(self):
        super().__init__()
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        self.url = 'https://xxxx/xxx/xxx/'
        self.proxies = {
            "http": "http://127.0.0.1:59292",
            "https": "http://127.0.0.1:59292",
        }

    def start_requests(self):
        for page in range(1, 500):
            params = {
                'page': page,
                'posts_to_load': '5',
                'sort': 'top',
            }
            full_url = self.url + '?' + urlencode(params)
            yield scrapy.Request(
                url=full_url,
                headers=self.headers,
                callback=self.parse,
                dont_filter=True,
                meta={"proxies": self.proxies}
            )

    def parse(self, response, **kwargs):
        print(response.text)
