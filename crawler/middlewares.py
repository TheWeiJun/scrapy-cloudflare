from scrapy.http import HtmlResponse
from tls_client import Session


class DownloaderMiddleware(object):

    def __init__(self):
        self.session: Session = Session(
            client_identifier="chrome_104"
        )

    def process_request(self, request, spider):
        proxies = request.meta.get("proxies") or None
        headers = request.headers.to_unicode_dict()
        if request.method == "GET":
            response = self.session.get(
                url=request.url,
                headers=headers,
                proxy=proxies,
                timeout_seconds=60,
            )
        else:
            response = self.session.post(
                url=request.url,
                headers=headers,
                proxy=proxies,
                timeout_seconds=60,
            )
        return HtmlResponse(
            url=request.url,
            status=response.status_code,
            body=response.content,
            encoding="utf-8",
            request=request,
        )
