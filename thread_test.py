#!/usr/bin/python3

import threading


class mythread(threading.Thread):
	def __init__(self,threadingID):
		threading.Thread.__init__(self)
		self.threadingID = threadingID
	def run(self):
		while True:
			print('This is %s' %self.threadingID)


thread1 = mythread(1);
thread2 = mythread(2);

thread1.start()
thread2.start()

