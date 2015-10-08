import random


class RandomUserAgentMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        ua = random.choice(spider.settings['USER_AGENT_LIST'])
        if ua:
            request.headers.setdefault('User-Agent', ua)
