import scrapy


class SolutionItem(scrapy.Item):
    letter: scrapy.Field()
    count: scrapy.Field()
