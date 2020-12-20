import numpy as np
import random as rnd
import matplotlib.pyplot as plt

kappa = 1
time_model = 24
len_queue = 4
num_channel = 1

time_event_last = 0
time_serv_sum = 0
time_pr = 0
time_in_queue = 0
pos_queue = 0
n_rej = 0
n_serv = 0
n_queue = 0

time_event = []
time_serv = []
time_last_end = []
ones_end = []
ones_event = []

def gen_rnd(kappa):
    return kappa*(1 - np.sqrt(1 - rnd.random()))

while time_event_last < time_model:
    time_event_last += gen_rnd(kappa)
    time_event.append(time_event_last)
    ones_event.append(1)

for i in time_event:
    serv = gen_rnd(kappa)
    time_serv_sum += serv
    time_serv.append(gen_rnd(kappa))

for i in range(0, len(time_event) - 2):
    time_end = time_event[i] + time_serv[i]
    time_pr += time_serv[i]
    time_last_end.append(time_end)
    ones_end.append(1)
    if time_event[i + 1] < time_end:
        n_serv += 1
    else:
        if pos_queue < len_queue:
            n_queue += 1
            pos_queue += 1
            time_in_queue += abs(time_end - time_event[i + 1])
            if time_event[i + 1] < time_end:
                pos_queue -= 1
                n_serv += 1
            else:
                n_rej += 1

print(f' 0) Вероятность нахождения в очереди = {round(n_queue/len(time_event)*100, 3)} [%]')
print(f' 1) Вероятность обслуживания = {round(n_serv/len(time_event)*100, 3)} [%]')
print(f' 2) Вероятность отказа = {round(n_rej/len(time_event)*100, 3)} [%]')
print(f' 3) Пропускная способность = {round(n_serv/time_model, 3)} [шт/час]')
print(f' 4) Среднее количество занятых каналов = {round(num_channel*time_serv_sum/time_model, 3)}')
print(f' 5) Вероятность простоя всей системы = {round(100*(abs(time_model - time_pr))/time_model, 3)} [%]')
# print(f' 6) Среднее количество заявок в очереди = {}')
print(f' 7) Среднее время ожидания заявки в очереди = {round(time_in_queue/n_queue, 3)} [час]')
print(f' 8) Среднее время обслуживания заявки = {round(time_serv_sum/len(time_event), 3)} [час]')
print(f' 9) Среднее время нахождения заявки в системе = {round(time_in_queue/n_queue + time_serv_sum/len(time_event), 3)} [час]')
# print(f' 10) Среднее количество заявок в системе = {}')

# plt.scatter(time_event, ones_event)
# plt.scatter(time_last_end, ones_end)
# plt.xlim([0, 2])
# plt.grid(True)
# plt.show()

