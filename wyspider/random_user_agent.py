from scrapy.utils.project import get_project_settings
import random
from scrapy import log

SETTINGS = get_project_settings()


class RandomUserAgentMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        ua = random.choice(SETTINGS['USER_AGENT_LIST'])
        if ua:
            request.headers.setdefault('User-Agent', ua)
            log.msg('[+] UA %s' % request.headers)
