from typing import Optional, List, Dict
from abc import ABC, abstractmethod


class Product:

    name: str
    price: float

    def __init__(self, name_: str, price_: float):
        self.name = name_
        self.price = price_


class TooManyProductsFoundError:

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
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        literki = []
        suma = 0
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
    products_: List[Product]
    products_dict: Dict

    def _init__(self, products_dict, products: List[Product]):
        for i in products_:
            products_dict[i.name] = i

    def wypisz(self, products_dict):
        for k, v in products_dict.items():
            print("{k} : {v}\n".format(k=k, v=v))

    def get_entries(self, n_letters):
        returned = []
        for i, j in products_dict.items():
            if returned.len() < n_letters:
                returned.apppend([i, j])
        return returned


class Client(object):
    n: int
    pomoc:  ListServer

    def __init__(self, pomoc_: ListServer):
        self.pomoc = pomoc_

    def get_total_price(self, n: int) -> Optional[float]:
        pomocna_lista = pomoc.get_entries(self.pomoc, n)
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
