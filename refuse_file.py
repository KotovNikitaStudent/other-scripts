import numpy as np
import random as rnd
import matplotlib.pyplot as plt

kappa = 1
time_model = 1
len_queue = 1
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
        self.time_free = 0
        self.avr_time_task = TAvarege()
        self.avr_task_in_sistem = TAvarege()
        self.avr_len_task = TAvarege()
        self.avr_time_in_serv = TAvarege()
        self.avr_time_eq_in_system = TAvarege()

    def print(self):
        print(f' 1) Вероятность обслуживания = {self.n_serv/(self.n_serv + self.n_rej)}')
        print(f' 2) Вероятность отказа = {self.n_rej/(self.n_serv + self.n_rej)}')
        print(f' 3) Пропускная способность = {self.n_serv/time_model}')
        # print(f' 4) Среднее количество занятых каналов = {}')
        print(f' 5) Вероятность простоя всей системы = {self.time_free/time_model}')
        print(f' 6) Среднее количество заявок в очереди = {self.avr_n_len.get()}')
        # print(f' 7) Среднее время ожидания заявки в очереди = {}')
        # print(f' 8) Среднее время обслуживания заявки = {}')
        # print(f' 9) Среднее время нахождения заявки в системе = {}')
        # print(f' 10) Среднее количество заявок в системе = {}')

class TThread:
    def __init__(self, _label_thread, _power):
        self.label_thread = _label_thread
        self.power = _power

def push_event(id,label,thread_id, time_started):
	global time_event
	t = TEvent(id,label,thread_id, time_started)
	for i in range(0,len(time_event)):
		if time_event[i].label > label:
			v = time_event[:i]
			v.append(t)
			time_event = v + time_event[i:]
			return
	time_event.append(t)

test_arr = [1]
pos = 0
def gen_rnd(kappa):
    # return kappa*(1 - np.sqrt(1 - rnd.random()))
    global pos, test_arr
    if pos < len(test_arr):
        i = test_arr[pos]
        pos += 1
        return i
    else:
        return 1000

current_time = 0
push_event(1, gen_rnd(kappa), -1, 0)
q = []
thread = []
for i in range(num_channel):
    thread.append(TThread(-1, int(input(f'input thread power {i+1}: '))))

stat = Statistics(num_channel)
while current_time < time_model:
    current = time_event.pop(0)
    if current.id == 1:
        push_event(1, current_time + gen_rnd(kappa), -1, current_time)
        if len(q) < len_queue:
            q.append(current)
            stat.n_serv += 1
            print('task queued')
        else:
            stat.n_rej += 1
            print('task NOT queued')
    if current.id == 2:
        thread[current.thread_id].label_thread = -1
        print('thread end')
        stat.avr_time_task.append(current_time - current.time_started)
    for i in range(0, len(thread)):
        if thread[i].label_thread == -1:
            if len(q) > 0:
                thread[i].label_thread = current.label
                stat.avr_time_in_serv.append(current_time - current.time_started)
                push_event(2, current.label + thread[i].power, i, current_time)
                q.pop(0)
                print('task threaded')
                break
    len_time = time_event[0].label - current_time
    thread_free = 0
    for i in range(0, len(thread)):
        if thread[i].label_thread > 0:
            stat.time_eq[i] += len_time
        else:
            thread_free += 1
    if thread_free == num_channel:
        stat.time_free += len_time
    current_time = time_event[0].label

stat.print()

# plt.scatter(time_event, ones_event)
# plt.scatter(time_last_end, ones_end)
# plt.xlim([0, 2])
# plt.grid(True)
# plt.show()