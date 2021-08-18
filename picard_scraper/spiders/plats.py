import scrapy
from re import findall

SEARCH_SIZE = 300

class PlatsSpider(scrapy.Spider):
    name = "plats"
    start_urls = [
       "https://www.picard.fr/rayons/plats-cuisines/plats?sz=" + str(SEARCH_SIZE) + "&prefn1=filtre-mode-preparation&prefv1=modecuissonmicroonde%7Cmodedecongelation%7Csans-cuisson"
    ]

    def parse(self, response):
        product_page_links = response.css('#search-result-items div.pi-ProductCard a::attr(href)')
        yield from response.follow_all(product_page_links, self.parse_product)
    
    def parse_product(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        name_text = extract_with_css('h1.pi-ProductPage-title::text')
        price_text = extract_with_css('div.pi-ProductDetails-salesPrice meta::attr(content)')
        nutriscore_text = extract_with_css('div.pi-ProductTabsNutrition-nutriscoreTitle span::text')
        kcal_text = extract_with_css('#tableNutrition0 > table > tbody > tr:nth-child(1) > td:nth-child(4) > div:nth-child(2)::text')
        
        kcal_number = 0
        if kcal_text == '':
            kcal_text = extract_with_css('#tableNutrition0 > table > tbody > tr:nth-child(1) > td:nth-child(2) > div:nth-child(2)')
            if kcal_text == '':
                kcal_number = 0
            else:
                weight_text = extract_with_css('#pdpMain > div > div.pi-ProductPage-top > div.pi-ProductPage-details > div.pi-ProductDetails.js-ProductDetails > div.pi-ProductDetails-ref > div > span::text')
                kcal_number = round(extract_int(kcal_text) * (extract_int(weight_text)/100))
        else:
            kcal_number = extract_int(kcal_text)
        print(name_text)

        price_number = float(price_text)
        yield {
            'name': name_text,
            'price': price_number,
            'nutriscore': extract_nutriscore_letter(nutriscore_text),
            'kcal': kcal_number,
            'ratio kcal/price': round(kcal_number / price_number),
            'full_path': response.url,
        }

def extract_nutriscore_letter(text):
    # 'nutriscore-a' to A
    if len(text) > 0:
        return text[-1].upper()
    else:
        return '-'

def extract_int(text):
    regex_result = findall(r'\d+', text)
    return int(regex_result[0]) if regex_result else None