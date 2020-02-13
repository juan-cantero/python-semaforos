import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


semaforo = threading.Semaphore()

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    logging.info('Reponiendo los platos...')
    platosDisponibles = 3
    semaforo.release()

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    semaforo.acquire()
    if(platosDisponibles == 0):
      Cocinero.run(Cocinero)
      if(platosDisponibles == 3):
        self.run()
    else:    
      platosDisponibles -= 1
      logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
      semaforo.release()

platosDisponibles = 3

for i in range(7):
  Comensal(i).start()

