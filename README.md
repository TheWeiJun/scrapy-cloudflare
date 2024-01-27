## scrapy-cloudflare
通过对Scrapy爬虫的twisted源码高并发改造，成功冲破5秒盾站点的屏障。

## 特点

- 高并发爬取：通过对 Scrapy 源码的改造，实现了对五秒盾站点的高并发爬取。
- 技术探险：项目中蕴含了对 Scrapy 和 twisted 源码的独特改造，是一次真正的技术冒险。

## 如何使用

1. 下载项目后，进入spider文件，添加以下命令：

```bash
custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "crawler.download_handler.CloudFlareDownloadHandler",
            "https": "crawler.download_handler.CloudFlareDownloadHandler",
        }
}
```
2. 爬虫启动后，会自动调用改造后的twisted下载器，实现对五秒盾站点的高并发爬取。

## 关注公众号
<img src="WechatIMG339.jpg" alt="Image" width="400"/>