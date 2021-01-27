import scrapy
import urllib.parse as urlparse
from urllib.parse import parse_qs


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['bisabeli.id']
    start_urls = ['http://bisabeli.id/notebook']

    def parse(self, response):
        # just page one
        # return self.get_products_in_page(response)
        # find the last pagination page
        last_url = response.css("ul.pagination li a")[-1].attrib.get("href")
        url_params = urlparse.urlparse(last_url)
        last_page = parse_qs(url_params.query)['page'][0]
        last_page = int(last_page)

        base_url = response.url

        for page in range(1, last_page):
            url = base_url + "?page=" + str(page)
            yield response.follow(url, callback=self.get_products_in_page)

    def get_products_in_page(self, response):
        products = response.css("div.products-category > div.products-list div.product-item-container")
        for product in products:
            title = product.css("h4 a::text").get().strip()
            url = product.css("h4 a").attrib.get("href")

            yield {
                "title": title,
                "url": url
            }
