"""
Olga Rodríguez Acevedo
"""

from multiprocessing import Lock, Condition, Value

class Table():
    def __init__(self, num_philosophers: int, manager):
        self.mutex = Lock()
        self.num_philosophers = num_philosophers
        self.manager = manager
        self.phil = self.manager.list([False] * num_philosophers)
        self.eating = Value('i',0)
        self.current_phil = None
        self.free_fork= Condition(self.mutex)
        
    def set_current_phil(self, num):
        self.current_phil = num
    
    def side_philosophers_dont_eat(self):
        n = self.current_phil
        return (not self.phil[(n-1) % (self.num_philosophers)]) and (not self.phil[(n+1) % (self.num_philosophers)])
    
    def wants_eat(self, num):
        self.mutex.acquire()
        self.current_phil = num
        self.free_fork.wait_for(self.side_philosophers_dont_eat)
        self.phil[num] = True
        self.eating.value += 1
        self.mutex.release()
          
    def wants_think(self, num):
        self.mutex.acquire()
        self.phil[num] = False
        self.eating.value -= 1
        self.free_fork.notify()
        self.mutex.release()