"""
Author: debendra
All rights reserved
"""

from urllib.parse import urlparse
from twisted.internet import reactor
from .runner import runner


def init(event, _):
    #  get records sent by SQS event
    records = event.get('Records')

    # map messages as, [('company_id', 'website')]
    messages = ((body['messageAttributes']['CompanyId']['stringValue'], body.get('body')) for body in records)

    print(f'Got {len(records)} links to crawl.')

    for message in messages:
        # map params for the crawler
        params = {'allowed_domains': [urlparse(url[1]).netloc for url in message], "start_urls": message}
        runner.crawl('website_crawler', **params)

    d = runner.join()

    #  pass deferred to stop reactor in case of exception or crawler finishes crawling.
    d.addBoth(lambda _: reactor.stop())

    # run reactor and start crawling, a blocking call
    reactor.run()

    return {
        'status': 200
    }
