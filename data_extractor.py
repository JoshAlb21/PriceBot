from bs4 import BeautifulSoup

import tools

class DataExtractor:
    def __init__(self, elements_to_watch:dict) -> None:
        self.elements_to_watch = elements_to_watch

    def print_raw_data(self, soup:BeautifulSoup) -> None:
        print(soup.body.get_text().strip())
    
    def extract_from_soup(self, soup:BeautifulSoup) -> list:
        container_master = 'div'
        element_master = 'a-row a-size-base a-color-secondary'

        element_stock_per_product = 'a-link-normal s-underline-text s-underline-link-text s-link-style'
        container_stock_per_product = 'a'

        element_price_per_product = 'a-color-base'
        container_price_per_product = 'span'

        all_nums_of_product = []
        all_prices = []
        results = []
        if soup is not None:
            if soup.findAll(container_master, attrs={'class': element_master}):
                for d in soup.findAll(container_master, attrs={'class': element_master}):
                    num_of_product = d.find(container_stock_per_product, attrs={'class': element_stock_per_product}).text.strip()
                    all_nums_of_product.append(num_of_product)
                    price = d.find(container_price_per_product, attrs={'class':element_price_per_product}).text.strip()
                    price = tools.convert_back_to_euro(price)
                    all_prices.append(price)
                    results.extend([num_of_product, price])
                    print("Available: ",results)
            else:
                print("no_soup_data")

        return results


    