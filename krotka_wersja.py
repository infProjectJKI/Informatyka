from typing import Optional, List, Dict
from abc import ABC, abstractmethod


class Product:

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class TooManyProductsFoundError(Exception):
    pass


class Server(ABC):
    n_max_returned_entries = 3
    n_letters: int

    @abstractmethod
    def get_entries(self, n_letters):
        pass


class ListServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products

    def get_entries(self, n_letters: int) -> List[Product]:
        products_unsorted = []
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        literki = []
        suma = 0
        for i in self.products:
            nazwa = list(i.name)
            if len(nazwa) >= n_letters:
                for znak in nazwa:
                    if znak not in numbers:
                        literki.append(znak)
                    else:
                        suma += 1
                if len(literki) == n_letters and 1 < suma < 4:
                    products_unsorted.append(i)
                    if self.n_max_returned_entries < len(products_unsorted):
                        raise TooManyProductsFoundError()
            literki = []
            suma = 0
        if len(products_unsorted) == 0:
            products_unsorted = []
            return products_unsorted
        products_sorted = sorted(products_unsorted, key=lambda products: products.price)
        return products_sorted


class MapServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = dict()
        for product in products:
            self.products[product.name] = product

    def get_entries(self, n_letters: int):
        sort1 = []
        pom = []
        s = 0
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in self.products.keys():
            if len(i) >= n_letters:
                for k in list(i):
                    if k not in numbers:
                        pom.append(k)
                    else:
                        s += 1
                if len(pom) == n_letters and 1 < s < 4:
                    sort1.append(self.products[i])
                    if self.n_max_returned_entries < len(sort1):
                        raise TooManyProductsFoundError()
            s = 0
            pom = []
        if len(sort1) == 0:
            sort1 = []
            return sort1
        sort1 = sorted(sort1, key=lambda products: products.price)
        return sort1


class Client(object):

    def __init__(self, server: Server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        total_sum = 0
        try:
            server_pom = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        if len(server_pom) == 0:
            return None
        else:
            for elem in server_pom:
                total_sum += elem.price
            return total_sum


products = [Product('P12', 1), Product('PP230', 2), Product('PP209', 1), Product('PP2', 1), Product('PP709', 1)]
server = MapServer(products)
for i, j in server.products.items():
    print('{i} : {j}'.format(i=i, j=j))
lst = server.get_entries(2)
client = Client(server)
x = client.get_total_price(2)
print('ogolna cena : {}\n'.format(x))
for i in lst:
    print(' {i} '.format(i=i.name))

products1 = [Product('P12', 1), Product('PP234', 2), Product('PP29', 3)]
server1 = ListServer(products1)
for i in server1.products:
    print('{i} '.format(i=i))
lst = server1.get_entries(2)
client1 = Client(server1)
x1 = client1.get_total_price(2)
print('ogolna cena : {}\n'.format(x1))
for i in lst:
    print(' {i} '.format(i=i.name))
