## wyspider

#### 使用步骤:

* pip install scrapy && pip install MySQL-python
* 把 wyspider.sql 导进数据库
* 更改 wyspider/settings.py 里的配置
* 运行 `scrapy crawl wooyun`

#### 常用配置介绍

选项|说明
:----|:----
START_URLS | 爬虫开始的链接
KEYWORDS | 关键字，默认为空
DEPTH_LIMIT | 爬行深度，默认为0，即无限制
CLOSESPIDER_PAGECOUNT | 爬行页面数量限制，默认为0，即无限制
LOG_FILE | 日志保存文件
LOG_LEVEL | 日志级别，可选 DEBUG/INFO/WARNING/ERROR/CRITICAL 五个级别
USER_AGENT_LIST | 爬虫UA列表，可自行修改
DOWNLOAD_DELAY | 爬行延时
DEPTH_PRIORITY | 默认为深度优先，如需广度优先去掉注释即可
