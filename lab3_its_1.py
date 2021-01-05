import random as rnd
import math
import matplotlib.pyplot as plt
from os import system

# kappa = 1
gamma = float(input('\nВведите произодительность источника: '))
# time_model = 10
time_model = float(input('Введите время моделирования: '))
# len_queue = 2
len_queue = int(input('Введите длину очереди: '))
time_event_last = 0
# num_channel = 1
num_channel = int(input('Введите количество каналов: '))

kappa = 10
epsilon = 2/math.log(1 + (gamma ** 2 / kappa ** 2))
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
		self.avr_time_eq_in_system = 0

	def print(self):
		print('\n 1) Вероятность обслуживания = ' + str(round((self.n_serv/(self.n_serv + self.n_rej))*100, 2)) + ' [%]')
		print(' 2) Вероятность отказа = ' + str(round((self.n_rej/(self.n_serv + self.n_rej))*100, 2)) + ' [%]')
		print(' 3) Пропускная способность = ' + str(round(self.n_serv/time_model, 2)) + ' [шт/ед.вр]')
		print(' 4) Среднее количество занятых каналов = ' + str(round(self.avr_len_task / time_model, 2)) + ' [шт]')
		print(' 5) Вероятность простоя всей системы = ' + str(round(((time_model-self.time_running)/time_model)*100, 2)) + ' [%]')
		print(' 6) Среднее количество заявок в очереди = ' + str(round(n_avr_q/(self.n_serv), 2)) + ' [шт]')
		print(' 7) Среднее время ожидания заявки в очереди = ' + str(round(self.avr_time_task.get(), 2)) + ' [ед.вр]')
		print(' 8) Среднее время обслуживания заявки = ' + str(round(self.avr_time_in_serv.get(), 2)) + ' [ед.вр]')
		print(' 9) Среднее время нахождения заявки в системе = ' + str(round(self.avr_time_task.get() + self.avr_time_in_serv.get(), 2)) + ' [ед.вр]')
		print(' 10) Среднее количество заявок в системе = ' + str(round(self.avr_time_eq_in_system/time_model, 2)) + ' [шт]')

class TThread:
	def __init__(self, _label_thread, _power):
		self.label_thread = _label_thread
		self.power = _power

def push_event(id,label,thread_id, time_started):
	global time_event
	# if id == 1:
	# 	print("Task planned: id = " + str(label) + " at " + str(time_started))
	t = TEvent(id,label,thread_id, time_started)
	for i in range(0,len(time_event)):
		if time_event[i].label > label:
			v = time_event[:i]
			v.append(t)
			time_event = v + time_event[i:]
			return
	time_event.append(t)

# time_stamps = [0,0,0,0,1000000]
# time_pos = 0
def gen_rnd(kappa):
	# global time_stamps, time_pos
	# result = time_stamps[time_pos]
	# time_pos += 1
	# return result
	# return kappa*(1 - math.sqrt(1 - rnd.random()))
    return kappa*math.sqrt(math.exp(2*rnd.random()/epsilon) - 1)

current_time = 0
push_event(1, gen_rnd(gamma), -1, 0)
q = []
thread = []
# thread_power = [1,1,1,1,1,1,1]
for i in range(num_channel):
	# thread.append(TThread(-1, thread_power[i]))
    thread.append(TThread(-1,float(input(f'Введите интенсивность обслуживания канала {i+1} : '))))

def countRunningThreads():
	global thread
	counter = 0
	for i in thread:
		if i.label_thread >= 0:
			counter += 1
	return counter

n_avr_q = 0
time_event_plt = []
ones_time_event_plt = []
serv_qt_plt = []
rej_qt_plt = []
thread_label_plt = []

time_event_plt.append(current_time)
stat = Statistics(num_channel)
while current_time < time_model:
	current = time_event.pop(0)
	if current.id == 1:
		push_event(1, current_time + gen_rnd(gamma), -1, current_time)
		time_event_plt.append(current_time + gen_rnd(gamma))
		# ones_time_event_plt.append(1)
		if len(q) < len_queue:
			q.append(current)
			serv_qt_plt.append(current_time)
			stat.n_serv += 1
			# print('task queued')
		else:
			stat.n_rej += 1
			rej_qt_plt.append(current_time)
			# print('task NOT queued')
	if current.id == 2:
		thread[current.thread_id].label_thread = -1
		n_avr_q += 1
	for i in range(0, len(thread)):
	# for t in thread:
		if thread[i].label_thread == -1:
			if len(q) > 0:
				thread[i].label_thread = current.label
				stat.avr_time_in_serv.append(thread[i].power)
				# print("Task started at " + str(current_time) + " planned = " + str(current.time_started))
				stat.avr_time_task.append(current_time - current.time_started)
				push_event(2, current.label + thread[i].power, i, current_time)
				# thread_label_plt.append(current.label + thread[i].power)
				thread_label_plt.append(current.label)
				q.pop(0)
				# print('task threaded ' + str(thread[i].label_thread) + " threads = " + str(countRunningThreads()))
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
	stat.avr_time_eq_in_system += len_time*(len_queue+runningThreads)

stat.print()

ras_kappa = [1, 2, 3, 4, 5]
ras_num_channel = [1, 2, 3, 4, 5]
ras_power_channel = [1, 2, 3, 4, 5]
ras_len_queue = [1, 2, 3, 4, 5]
ras_time_model = [5, 10, 15, 20, 24]

kappa_0 = [7.95,30.77,63.16,100.0,100.0]
kappa_1 = [92.05,69.23,36.84,0,0]
kappa_2 = [1.2,1.2,1.2,1.1,0.8]
kappa_3 = [0.99,0.99,0.99,0.98,0.86]
kappa_4 = [0.51,0.61,0.84,2.15,13.96]
kappa_5 = [0.75,0.75,0.75,0.82,0.88]
kappa_6 = [0.91,0.94,0.98,1.0,1.27]
kappa_7 = [1.0,1.0,1.0,1.0,1.0]
kappa_8 = [1.91,1.94,1.98,2.0,2.27]
kappa_9 = [2.98,2.98,2.97,2.96,2.96]

lambda_0 = [8.0,4.73,3.9,3.27,2.72]
lambda_1 = [92.0,95.27,96.1,96.73,97.28]
lambda_2 = [1.2,0.7,0.6,0.5,0.4]
lambda_3 = [0.99,1.0,1.0,1.0,1.0]
lambda_4 = [0.58,0.45,0.23,0.0,0.29]
lambda_5 = [0.75,0.57,0.5,0.4,0.25]
lambda_6 = [0.91,1.6,2.27,2.68,2.54]
lambda_7 = [1.0,2.0,3.0,4.0,5.0]
lambda_8 = [1.91,3.6,5.27,6.68,7.54]
lambda_9 = [2.98,2.99,2.99,3.0,2.99]

length_queue_0 = [7.38,7.84,8.72,9.52,9.74]
length_queue_1 = [92.62,92.16,91.28,90.48,90.26]
length_queue_2 = [1.1,1.2,1.3,1.4,1.5]
length_queue_3 = [0.99,0.99,0.99,0.99,1.0]
length_queue_4 = [0.66,0.77,0.62,0.56,0.25]
length_queue_5 = [0.82,0.75,0.69,0.64,0.6]
length_queue_6 = [0.91,0.91,0.91,0.91,0.91]
length_queue_7 = [1.0,1.0,1.0,1.0,1.0]
length_queue_8 = [1.91,1.91,1.91,1.91,1.91]
length_queue_9 = [1.99,2.98,3.98,4.97,5.99]

time_model_0 = [9.33,8.0,7.8,7.26,7.05]
time_model_1 = [90.67,92.0,92.2,92.74,92.95]
time_model_2 = [1.4,1.2,1.13,1.1,1.08]
time_model_3 = [0.99,1.0,1.0,1.0,1.0]
time_model_4 = [1.14,0.09,0.33,0.09,0.08]
time_model_5 = [0.57,0.75,0.82,0.86,0.88]
time_model_6 = [0.82,0.91,0.94,0.95,0.96]
time_model_7 = [1.0,1.0,1.0,1.0,1.0]
time_model_8 = [1.82,1.91,1.94,1.95,1.96]
time_model_9 = [2.97,3.0,2.99,3.0,3.0]

num_channels_0 = [8.11,11.33,13.82,16.44,16.88]
num_channels_1 = [91.89,88.67,86.18,83.56,83.12]
num_channels_2 = [1.2,1.7,2.1,2.4,2.6]
num_channels_3 = [0.99,2.0,2.96,3.94,4.91]
num_channels_4 = [0.67,0.0,0.71,0.33,0.43]
num_channels_5 = [0.75,0.76,0.76,0.75,0.73]
num_channels_6 = [0.91,1.14,1.38,1.56,1.64]
num_channels_7 = [1.0,1.33,1.68,2.0,2.25]
num_channels_8 = [1.91,2.48,3.06,3.56,3.89]
num_channels_9 = [2.98,4.0,4.94,5.94,6.9]

fig, ax = plt.subplots(ncols=5, figsize=(20, 4))
ax = ax.ravel()
ax[0] = plt.subplot(1, 5, 1)
ax[0].set_xlabel('Интенсивность источника [усл.ед]')
ax[0].set_ylabel('Значение измеряемого параметра [%],[шт/ед.вр],[шт],[ед.вр]')
ax[0].grid(True)
ax[1] = plt.subplot(1, 5, 2)
# ax[1].set_title('Интенсивности обслуживания')
ax[1].set_xlabel('Интенсивность обслуживания [усл.ед]')
ax[1].set_ylabel('Значение измеряемого параметра [%],[шт/ед.вр],[шт],[ед.вр]')
ax[1].grid(True)
ax[2] = plt.subplot(1, 5, 3)
# ax[2].set_title('Длины очереди')
ax[2].set_xlabel('Длина очереди [шт]')
ax[2].set_ylabel('Значение измеряемого параметра [%],[шт/ед.вр],[шт],[ед.вр]')
ax[2].grid(True)
ax[3] = plt.subplot(1, 5, 4)
# ax[3].set_title('Времени моделирования')
ax[3].set_xlabel('Время моделирования [ед.вр]')
ax[3].set_ylabel('Значение измеряемого параметра [%],[шт/ед.вр],[шт],[ед.вр]')
ax[3].grid(True)
ax[4] = plt.subplot(1, 5, 5)
# ax[4].set_title('Количество каналов')
ax[4].set_xlabel('Количество каналов [шт]')
ax[4].set_ylabel('Значение измеряемого параметра [%],[шт/ед.вр],[шт],[ед.вр]')
ax[4].grid(True)

ax[0].plot(ras_kappa, kappa_0, ras_kappa, kappa_1,ras_kappa, kappa_2, ras_kappa, kappa_3, ras_kappa, kappa_4, ras_kappa, kappa_5, ras_kappa, kappa_6, ras_kappa, kappa_7, ras_kappa, kappa_8, ras_kappa, kappa_9)
ax[1].plot(ras_power_channel, lambda_0, ras_power_channel, lambda_1, ras_power_channel, lambda_2, ras_power_channel, lambda_3, ras_power_channel, lambda_4, ras_power_channel, lambda_5, ras_power_channel, lambda_6, ras_power_channel, lambda_7, ras_power_channel, lambda_8, ras_power_channel, lambda_9)
ax[2].plot(ras_len_queue, length_queue_0, ras_len_queue, length_queue_1, ras_len_queue, length_queue_2, ras_len_queue, length_queue_3, ras_len_queue, length_queue_4, ras_len_queue, length_queue_5, ras_len_queue, length_queue_6, ras_len_queue, length_queue_7, ras_len_queue, length_queue_8, ras_len_queue, length_queue_9)
ax[3].plot(ras_time_model, time_model_0, ras_time_model, time_model_1, ras_time_model, time_model_2, ras_time_model, time_model_3, ras_time_model, time_model_4, ras_time_model, time_model_5, ras_time_model, time_model_6, ras_time_model, time_model_7, ras_time_model, time_model_8, ras_time_model, time_model_9)
ax[4].plot(ras_num_channel, num_channels_0, ras_num_channel, num_channels_1, ras_num_channel, num_channels_2, ras_num_channel, num_channels_3, ras_num_channel, num_channels_4, ras_num_channel, num_channels_5, ras_num_channel, num_channels_6, ras_num_channel, num_channels_7, ras_num_channel, num_channels_8, ras_num_channel, num_channels_9)
ax[0].legend(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), loc='center right', ncol=2)
ax[1].legend(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), loc='center right', ncol=2)
ax[2].legend(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), loc='center right', ncol=2)
ax[3].legend(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), loc='center right', ncol=2)
ax[4].legend(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'), loc='center right', ncol=2)

plt.figure(2)
for i in range(len(time_event_plt)):
	ones_time_event_plt.append(1)
val_serv = []
for i in range(len(serv_qt_plt)):
	val_serv.append(2)
val_rej = []
for i in range(len(rej_qt_plt)):
	val_rej.append(3)
val_thread = []
for i in range(len(thread_label_plt)):
	val_thread.append(4)
plt.scatter(time_event_plt, ones_time_event_plt, label='Заявки')
plt.vlines(time_event_plt, 1, 4, colors='k', linestyle=':', linewidth=1)
plt.scatter(serv_qt_plt, val_serv, label='Обслужено')
plt.scatter(rej_qt_plt, val_rej, label='Отказано')
plt.scatter(thread_label_plt, val_thread, label='В канале')
location = ['center right']
i = 0
plt.legend(fontsize=10, loc=location[i])
plt.title('Временные диграммы работы СМО')
plt.xlabel('Время, [ед.вр]')
plt.ylabel('События во времени')
plt.grid(True)
plt.show()
system('pause')
