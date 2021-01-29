import scrapy


class ProductDetailSpider(scrapy.Spider):
    name = 'productdetail'
    allowed_domains = ['bisabeli.id']
    start_urls = [
        "https://bisabeli.id/msi-gt75-8sg-i9-8950hk-64gb-1tb-hdd-512gb-ssd-nvidia-8gb-win10-173in-["
        "9s7-17a611-055]-bbli-1800 ",
        "https://bisabeli.id/index.php?route=product/product&product_id=7874"
    ]

    def parse(self, response):
        title = response.css('div#content div.title-product h1::text').get().strip()
        price_str = response.css('div#content div.price span.price-new span::text').get().strip()
        price = ''.join([i for i in price_str if i.isdigit()])
        brand = response.css('div#content div.product-box-desc div.brand a span::text').get().strip()
        model = response.css('div#content div.product-box-desc div.model::text').get().strip()
        description = response.css('div.producttab div#tab-description div#collapse-description').get().strip()

        yield {
            'title': title,
            'price': price,
            'brand': brand,
            'model': model,
            'shipping_support': self.shipping_support(response),
            'specification': self.specification(response),
            'description': description,
        }

    @staticmethod
    def shipping_support(response):
        shipping = []

        for ship in response.css('div#content div.shipping-image img'):
            shipping.append(ship.attrib.get('data-original-title'))

        return shipping

    @staticmethod
    def specification(response):
        specs = []

        spec_list = response.css('div.producttab div#tab-description ul.product-property-list li.property-item')

        for spec in spec_list:
            prop_title = spec.css('span.propery-title::text').get().strip()
            prop_value = spec.css('span.propery-des::text').get().strip()
            specs.append({
                prop_title: prop_value
            })
        return specs
