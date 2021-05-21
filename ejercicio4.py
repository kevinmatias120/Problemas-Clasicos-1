from rwlock import RWLock
import threading
import random
import logging
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

equipos = ["Boca", "River", "Racing", "Independiente", "San Lorenzo", "Huracán", "Gimnasia", 
"Estudiantes", "Velez", "Ferro", "Lanus", "Quilmes"]

partido =["equipo1", 0, "equipo2", 0]

marker = RWLock()

def escritor(id_thread):
    global equipos
    global partido

    while True:
        equipo1 = equipos[random.randint( 0,len(equipos)-1 )]
        equipo2 = equipos[random.randint( 0,len(equipos)-1 )]
        while equipo1 == equipo2:
            equipo2 = equipos[random.randint( 0,len(equipos)-1 )]
    
        marker.w_acquire()
        try:
            partido[0] = equipo1
            partido[1] = random.randint(0,3)
            partido[2] = equipo2
            partido[3] = random.randint(0,3)
            logging.info(f'Partido actualizado por Escritor-{id_thread}')
        finally:
            marker.w_release()
            time.sleep(random.randint(1,2))

def lector(id_thread):
    global partido
    while True:
        marker.r_acquire()
        try:
            logging.info(f'Lector-{id_thread}: el resultado fue: {partido[0]} {partido[1]} - {partido[2]} {partido[3]}')
        finally:
            marker.r_release()
            time.sleep(random.randint(1,2))
            

def main():
    hilos = []
    for i in range(1):
        writer = threading.Thread(target=escritor, args=(i,))
        logging.info(f'Arrancando escritor-{i}')
        writer.start()
        hilos.append(writer)

    for i in range(4):
        reader = threading.Thread(target=lector, args=(i,))
        logging.info(f'Arrancando lector-{i}')
        reader.start()
        hilos.append(escritor)

    for t in hilos:
        t.join()


if __name__ == "__main__":
    main()