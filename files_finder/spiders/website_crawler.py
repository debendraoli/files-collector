from scrapy import Request
from scrapy.linkextractors import IGNORED_EXTENSIONS, LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.spiders import CrawlSpider, Rule
from twisted.internet.error import DNSLookupError, TCPTimedOutError, TimeoutError
from ..filters import get_extensions
from ..items import OpaxeItem
import mysql.connector as mysql


class WebsiteCrawler(CrawlSpider):
    name = 'website_crawler'
    links = set()
    conn = None

    link_extractor = LinkExtractor(
        deny=('.*/(?i)contact|about|newsletter|privacy|login|register|tel:',),
        deny_extensions=IGNORED_EXTENSIONS)

    rules = (Rule(
        link_extractor=link_extractor,
        cb_kwargs=None, follow=True,
        process_links='process_links', callback='parse_start_url', process_request='process_request'),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.IGNORED_EXTENSIONS = IGNORED_EXTENSIONS.copy()

        #  remove registred extensions from ignored extensions list
        for ext in self.settings.get('FILE_EXTENSIONS'):
            self.IGNORED_EXTENSIONS.remove(ext)

        #  connect to mysql if there is none so we have only one connection
        if not self.conn:
            self.conn = mysql.connect(**self.settings.get('DB_CRED'))
        cursor = self.conn.cursor()
        cursor.execute("SELECT url from files_link;")
        self.links.update({url[0] for url in cursor.fetchall()})

    def start_requests(self):
        """This function is called once"""
        for company_id, url in self.start_urls:
            yield Request(url=url, errback=self.err_back, callback=self.parse, meta={'company_id': company_id})

    def parse_start_url(self, response):

        #  extract links from the page
        extract_links = self.link_extractor.extract_links(response)

        #  pass the extracted links to the filter function for filtering downloadable files
        map_links = set(get_extensions(self.settings['FILE_EXTENSIONS'], extract_links)).difference(self.links)

        #  save the filtered links to the memory for future use
        self.links.update(map_links)

        # initialize item
        item = OpaxeItem()

        #  get company id from the meta dict that was passed from the start_request method.
        item['company_id'] = response.meta.get('company_id')
        item['url'] = response.url
        item['links'] = map_links
        item['body'] = response.body.strip()
        return item

    def process_request(self, request, response):
        # add company id to new request's metadata.
        request.meta['company_id'] = response.meta.get('company_id')

        # and also the errback
        request.errback = self.err_back
        return request

    def process_links(self, links):
        """Filters new links with already discovered links"""
        return filter(lambda link: link.url not in self.links, links)

    def close(self, reason):
        self.conn.close()

    def err_back(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f'HttpError on {response.url}')

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error(f'DNSLookupError on {request.url}')

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(f'TimeoutError on {request.url}')
