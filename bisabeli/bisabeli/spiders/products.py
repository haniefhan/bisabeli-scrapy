import scrapy

class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['bisabeli.id']
    start_urls = ['http://bisabeli.id/notebook']

    def parse(self, response):
        # yield self.get_products_in_page(response)
        products: List[Selector] = response.css("div.products-category > div.products-list div.product-item-container")
        for product in products:
            title = product.css("h4 a::text").get()
            url = product.css("h4 a").attrib.get("href")

            yield{
                "title": title,
                "url": url
            }