import time
import threading
from Queue import Queue
from Data import Data
from Command import Command
from LinuxSensor import LinuxSensor
import random

def readSensor(data):
	while 1:
		condition.acquire()
		frequency = sensor.getFrequency()
		if (sensor.getSense() == False) & (frequency == 0):
			condition.wait()
		else:
			condition.wait(frequency)
			data.put(sensor.getData())
		condition.release()
		
def readData (data):
	while 1:
		print data.get(True).getData() 
		data.task_done()

def receiveCommand (command):
	while 1:
		comando = command.get(True)
		condition.acquire()
		if comando.getCommand() == 'SENSE':
			sensor.setSense(True)
		else:
			sensor.setSense(False)

		sensor.setFrequency(comando.getValue())
		if (sensor.getFrequency() > 0) | (sensor.getSense() == True):
			condition.notify()
		condition.release()
		command.task_done()
		time.sleep(0)
		
def setCommand (command):
	global i, frequency
	while 1:	
		commandValue = round(random.uniform(1,2))
		oldFrequency = frequency
		if commandValue == 1:
			frequency = random.uniform(5,10)
			command.put(Command(13,'SETFR', frequency))
			print 'SETFR ', frequency
		else:
			command.put(Command(13,'SENSE', oldFrequency))
			print 'SENSE'
		time.sleep(random.uniform(1,20))

try:
	if __name__=="__main__":
	
		sensor = LinuxSensor(0,[3])
		i=0
		command = Queue(10)
		data = Queue(10)
		condition = threading.Condition()		
		frequency = 0

		dataThread = threading.Thread(target=readSensor, args = (data,)) 
		commandThread = threading.Thread(target=receiveCommand, args = (command,))
		escribircomando = threading.Thread(target=setCommand, args = (command,))
		leerDato = threading.Thread(target=readData, args = (data,))

		dataThread.start()
		commandThread.start()
		escribircomando.start()
		leerDato.start()

		while 1: pass
except KeyboardInterrupt:
	print 'limpio pines'
