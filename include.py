from typing import Optional, List
from abc import ABC, abstractmethod


class Product:

    name: str
    price: float

    def __init__(self, name_: str, price_: float):
        self.name = name_
        self.price = price_


class TooManyProductsFoundError(Exception):

    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać: (1) metodę inicjalizacyjną przyjmującą listę obiektów typu Product i ustawiającą atrybut products zgodnie z typem reprezentacji produktów na danym serwerze, (2) możliwość odwołania się do atrybutu klasowego n_max_returned_entries (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania, (3) możliwość odwołania się do metody get_entries(self, n_letters) zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries: int
    n_letters: int
    @abstractmethod
    def get_entries(self, n_letters):
        pass


class ListServer(Server):
    products: List[Product]
    n_letters_error: int

    def __init__(self, products1_: List[Product]):
        self.products = products1_

    def get_entries(self, n_letters:  int) -> List[Product]:
        products_unsorted = []
        products_sorted = []
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        literki = []
        suma = 0
        if self.n_max_returned_entries < self.n_letters:
            raise TooManyProductsFoundError
        for i in products:
            nazwa = list(i.name)
            if len(nazwa) >= n_letters:
                for znak in nazwa:
                    if znak not in numbers:
                        literki.append(znak)
                    else:
                        suma += 1
                if len(literki) == n_letters and 1 < suma < 4:
                    products_unsorted.append(i)
            literki = []
            suma = 0

        n = len(products_unsorted)
        x: int = 0
        while n > 1:
            h = 0
            for i in range(1, n):
                x = x + 1
                if products_unsorted[i - 1].price > products_unsorted[i].price:
                    products_unsorted[i - 1], products_unsorted[i] = products_unsorted[i], products_unsorted[i - 1]
                    h = 1
            n = n - 1
            if not h == 1:
                break
        return products_unsorted



class MapServer(Server):

    products1: Dict
    
    def __init__(self, product_: List[Product]):
        pom_product = {}
        for e in product_:
            pom_product[e.name] = e
        self.products1 = pom_product

    def get_entries(self, n_letters: int):
        sort1 = []
        pom = []
        sort_1 = []
        s = 0
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if self.n_max_returned_entries < self.n_letters:
            raise TooManyProductsFoundError
        for i in self.products1.keys():
            if len(i) >= n_letters:
                for k in list(i):
                    if k not in numbers:
                        pom.append(k)
                    else:
                        s += 1
                if len(pom) == n_letters and 1 < s < 4:
                    sort1.append(i)
                    sort_1.append((self.products1[i]).price)
            s = 0
            pom = []

        n = len(sort1)
        x: int = 0
        while n > 1:
            h = 0
            for i in range(1, n):
                x = x + 1
                if sort1[i - 1].price > sort1[i].price:
                    sort1[i - 1], sort1[i] = sort1[i], sort1[i - 1]
                    h = 1
            n = n - 1
            if not h == 1:
                break
        return sort1

class Client(object):

    def __init__(self, pomoc_: ListServer):
        self.pomoc = pomoc_

    def get_total_price(self, n: int) -> Optional[float]:
        pomocna_lista = self.pomoc.get_entries(n)
        suma = 0
        for elem in pomocna_lista:
            suma += elem.price
        return suma


products = [Product('P12', 1), Product('PP234', 2), Product('PP2', 1)]
server = ListServer(products)
lst = server.get_entries(2)
client = Client(server)
x = client.get_total_price(2)
print('ogolna cena : {}\n'.format(x))
for i in lst:

    print(' {i} '.format(i=i.name))

