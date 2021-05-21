import threading
import random
import logging
import time
from typing import List

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class listaFinita(list):

    def __init__(self, max_elementos):
            self.max_elementos = max_elementos
            super().__init__()
    
    def pop(self, index):
        assert len(self) != 0, "lista vacia"
        return super().pop(index)

    def append(self, item):
        assert len(self) < self.max_elementos,"lista llena"
        super().append(item)

    def insert(self, index, item):
        assert index < self.max_elementos, "indice invalido"
        super().insert(index, item)

    def full(self):
        if len(self) == self.max_elementos:
            return True
        else:
            return False



class Productor(threading.Thread):
    def __init__(self, lista1 = listaFinita, lista2 = List):
        super().__init__()
        self.lista = lista1
        self.paises = lista2
        self.lockProductor = threading.Lock()

    def run(self):
        while True:
            self.lockProductor.acquire()
            try:
                while self.lista.full():
                    pass
                self.lista.append(self.paises[random.randint( 0,len(self.paises)-1 )])
                logging.info(f'produjo el item: {self.lista[-1]}')
                time.sleep(random.randint(1,5))
            finally:
                self.lockProductor.release()

           


class Consumidor(threading.Thread):
    def __init__(self, lista):
        super().__init__()
        self.lista = lista
        self.lockConsumidor = threading.Lock()


    def run(self):
        while True:
            self.lockConsumidor.acquire()
            try:
                while len(self.lista) == 0:
                    pass
                tupla = self.lista.pop(0)
                pais = tupla[0]
                capital = tupla[1]
                logging.info(f' la capital de {pais} es {capital}')
                time.sleep(random.randint(1,5))
            finally:
                self.lockConsumidor.release()

            

def main():
    hilos = []
    lista = listaFinita(4)
    listaPaises = [("España", "Madrid"), ("Francia", "París"), ("Italia", "Roma"), ("Inglaterra", "Londres"),
                   ("Alemania", "Berlín"), ("Rusia", "Moscú"), ("Turquía", "Istambul"), ("China", "Pekín"),
                   ("Japón", "Tokio"), ("Emiratos Árabes", "Dubai"), ("Argentina", "Buenos Aires"),
                   ("Brasil", "Brasilia"), ("Colombia", "Bogotá"),
                   ("Uruguay", "Montevideo"), ]

    for i in range(4):
        productor = Productor(lista, listaPaises)
        consumidor = Consumidor(lista)
        hilos.append(productor)
        hilos.append(consumidor)

        logging.info(f'Arrancando productor {productor.name}')
        productor.start()

        logging.info(f'Arrancando consumidor {consumidor.name}')
        consumidor.start()

    for h in hilos:
        h.join()


if __name__ == '__main__':
    main()