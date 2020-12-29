#import numpy as np
import random as rnd
import math
#import matplotlib.pyplot as plt

kappa = 1
time_model = 10
len_queue = 2
time_event_last = 0
num_channel = 1

time_serv_sum = 0
time_pr = 0
time_in_queue = 0
pos_queue = 0

time_event = []
time_serv = []
time_last_end = []
ones_end = []
ones_event = []

class TEvent:
	def __init__(self, _id, _label, _thread_id, _time_started):
		self.id = _id
		self.label = _label
		self.thread_id = _thread_id
		self.time_started = _time_started

class TAvarege:
	def __init__(self):
		self.sum = 0
		self.count = 0
	def append(self, value):
		self.sum += value
		self.count += 1
	def get(self):
		if self.count == 0:
			return 0
		return self.sum/self.count

class Statistics:
	def __init__(self, num_channel):
		self.n_rej = 0
		self.n_serv = 0
		self.time_eq = []
		for i in range(num_channel):
			self.time_eq.append(0)
		self.avr_n_len = TAvarege()
		self.time_running = 0
		self.avr_time_task = TAvarege()
		self.avr_eq_in_system = TAvarege()
		self.avr_len_task = 0
		self.avr_time_in_serv = TAvarege()
		self.avr_time_eq_in_system = TAvarege()

	def print(self):
		print(' 1) Вероятность обслуживания = ' + str(self.n_serv/(self.n_serv + self.n_rej)))
		print(' 2) Вероятность отказа = ' + str(self.n_rej/(self.n_serv + self.n_rej)))
		print(' 3) Пропускная способность = ' + str(self.n_serv/time_model))
		print(' 4) Среднее количество занятых каналов = ' + str(self.avr_len_task / time_model))
		print(' 5) Вероятность простоя всей системы = ' + str((time_model-self.time_running)/time_model))
		print(' 6) Среднее количество заявок в очереди = ' + str(self.avr_n_len.get()))
		print(' 7) Среднее время ожидания заявки в очереди = ' + str(self.avr_time_task.get()))
		print(' 8) Среднее время обслуживания заявки = ' + str(self.avr_time_in_serv.get()))
		print(' 9) Среднее время нахождения заявки в системе = ' + str(self.avr_time_task.get() + self.avr_time_in_serv.get()))
		print(' 10) Среднее количество заявок в системе = ' + str(time_model/(self.n_serv + self.n_rej)))

class TThread:
	def __init__(self, _label_thread, _power):
		self.label_thread = _label_thread
		self.power = _power

def push_event(id,label,thread_id, time_started):
	global time_event
	if id == 1:
		print("Task planned: id = " + str(label) + " at " + str(time_started))
	t = TEvent(id,label,thread_id, time_started)
	for i in range(0,len(time_event)):
		if time_event[i].label > label:
			v = time_event[:i]
			v.append(t)
			time_event = v + time_event[i:]
			return
	time_event.append(t)

time_stamps = [0,0,0,0,1000000]
time_pos = 0
def gen_rnd(kappa):
	global time_stamps, time_pos
	result = time_stamps[time_pos]
	time_pos += 1
	return result
	#return kappa*(1 - math.sqrt(1 - rnd.random()))

current_time = 0
push_event(1, gen_rnd(kappa), -1, 0)
q = []
thread = []
thread_power = [1,1,1,1,1,1,1]
for i in range(num_channel):
	thread.append(TThread(-1, thread_power[i]))

def countRunningThreads():
	global thread
	counter = 0
	for i in thread:
		if i.label_thread >= 0:
			counter += 1
	return counter

stat = Statistics(num_channel)
while current_time < time_model:
	current = time_event.pop(0)
	if current.id == 1:
		push_event(1, current_time + gen_rnd(kappa), -1, current_time)
		if len(q) < len_queue:
			q.append(current)
			stat.n_serv += 1
			# print('task queued')
		else:
			stat.n_rej += 1
			# print('task NOT queued')
	if current.id == 2:
		thread[current.thread_id].label_thread = -1
	for t in thread:
		if t.label_thread == -1:
			if len(q) > 0:
				t.label_thread = current.label
				stat.avr_time_in_serv.append(t.power)
				print("Task started at " + str(current_time) + " planned = " + str(current.time_started))
				stat.avr_time_task.append(current_time - current.time_started)
				push_event(2, current.label + t.power, i, current_time)
				q.pop(0)
				print('task threaded ' + str(t.label_thread) + " threads = " + str(countRunningThreads()))
				break
	if time_event[0].label > time_model:
		break
	len_time = time_event[0].label - current_time
	runningThreads = countRunningThreads()
	for i in range(0, len(thread)):
		if thread[i].label_thread > 0:
			stat.time_eq[i] += len_time
	if runningThreads != 0:
		stat.time_running += len_time
	stat.avr_len_task += runningThreads * len_time
	current_time = time_event[0].label

stat.print()
# plt.scatter(time_event, ones_event)
# plt.scatter(time_last_end, ones_end)
# plt.xlim([0, 2])
# plt.grid(True)
# plt.show()

