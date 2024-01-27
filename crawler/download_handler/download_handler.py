"""Download handlers for http and https schemes"""

import logging
from time import time
from urllib.parse import urldefrag

from tls_client import Session
from twisted.internet import threads
from twisted.internet.error import TimeoutError
from scrapy.http import HtmlResponse
from scrapy.core.downloader.handlers.http11 import HTTP11DownloadHandler

logger = logging.getLogger(__name__)


class CloudFlareDownloadHandler(HTTP11DownloadHandler):

    def __init__(self, settings, crawler=None):
        super().__init__(settings, crawler)
        self.session: Session = Session(
            client_identifier="chrome_104"
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def download_request(self, request, spider):
        from twisted.internet import reactor
        timeout = request.meta.get("download_timeout") or 10
        # request details
        url = urldefrag(request.url)[0]
        start_time = time()

        # Embedding the provided code asynchronously
        d = threads.deferToThread(self._async_download, request)

        # set download latency
        d.addCallback(self._cb_latency, request, start_time)
        # check download timeout
        self._timeout_cl = reactor.callLater(timeout, d.cancel)
        d.addBoth(self._cb_timeout, url, timeout)
        return d

    def _async_download(self, request):
        timeout = int(request.meta.get("download_timeout"))
        proxies = request.meta.get("proxies") or None
        headers = request.headers.to_unicode_dict()
        if request.method == "GET":
            response = self.session.get(
                url=request.url,
                headers=headers,
                proxy=proxies,
                timeout_seconds=timeout,
            )
        else:
            response = self.session.post(
                url=request.url,
                headers=headers,
                proxy=proxies,
                timeout_seconds=timeout,
            )
        return HtmlResponse(
            url=request.url,
            status=response.status_code,
            body=response.content,
            encoding="utf-8",
            request=request,
        )

    def _cb_timeout(self, result, url, timeout):
        if self._timeout_cl.active():
            self._timeout_cl.cancel()
            return result
        raise TimeoutError(f"Getting {url} took longer than {timeout} seconds.")

    def _cb_latency(self, result, request, start_time):
        request.meta["download_latency"] = time() - start_time
        return result