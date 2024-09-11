import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from scrapy.http import HtmlResponse
import time

class NJSnapSpider(scrapy.Spider):
    name = 'njsnap'
    start_urls = ['https://www.nj.gov/humanservices/njsnap/']

    def __init__(self):
        # Set up Selenium with headless Firefox
        firefox_options = Options()
        firefox_options.headless = True  # Run Firefox in headless mode

        # Set up the service for GeckoDriver
        service = Service('/usr/local/bin/geckodriver')  # Path to your geckodriver

        self.driver = webdriver.Firefox(service=service, options=firefox_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3)  # Wait for JavaScript to load the content

        # Get the HTML rendered by Selenium
        selenium_html = self.driver.page_source
        response = HtmlResponse(url=response.url, body=selenium_html, encoding='utf-8')

        # Extract the main content of the page
        page_content = response.xpath('//body').get()

        # Save or process the content
        page_url = response.url
        yield {
            'url': page_url,
            'content': page_content
        }

        # Follow all internal links
        for href in response.css('a::attr(href)').extract():
            url = response.urljoin(href)
            if 'https://www.nj.gov/humanservices/njsnap/' in url:  # Stay within the njsnap site
                yield scrapy.Request(url, callback=self.parse)

    def close(self, reason):
        self.driver.quit()

# Run the spider and save the output to a JSON file
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "output.json": {"format": "json"},  # Save output in JSON format
            # Or, if you want CSV: "output.csv": {"format": "csv"},
        },
    })
    process.crawl(NJSnapSpider)
    process.start()
