from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings


runner = CrawlerRunner(get_project_settings())
