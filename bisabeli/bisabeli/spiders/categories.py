import scrapy


class CategoriesSpider(scrapy.Spider):
    name = 'categories'
    allowed_domains = ['bisabeli.id']
    start_urls = ['http://bisabeli.id/']

    def parse(self, response):
        categories: List[Selector] = response.css("ul.megamenu > li")
        for category in categories:
            yield self.get_categories(category)

    @classmethod
    def get_categories(self, category):
        return {
            'category': category.css('a > span > strong::text').get().strip(),
            'url': category.css('a').attrib.get('href'),
            'subcategories': self.get_subcategories(category),
        }

    @classmethod
    def get_subcategories(self, category):
        ret = []
        subcategories: List[Selector] = category.css("div.sub-menu div.menu > ul > li")
        for subcategory in subcategories:
            ret.append({
                'subcategory': subcategory.css('a::text').get().strip(),
                'url': subcategory.css('a').attrib.get('href'),
                'subsubcategories': self.get_subsubcategories(subcategory)
            })
        return ret

    @classmethod
    def get_subsubcategories(self, subcategory):
        ret = []
        subsubcategories: List[Selector] = subcategory.css("ul > li")
        for subsubcategory in subsubcategories:
            ret.append({
                'subsubcategory': subsubcategory.css('a::text').get().strip(),
                'url': subsubcategory.css('a').attrib.get('href'),
            })
        return ret
