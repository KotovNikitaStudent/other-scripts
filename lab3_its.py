import numpy as np
import random as rnd

kappa = 1
time_model = 24

time_event_last = 0
time_serv_sum = 0
n_rej = 0
n_serv = 0

time_event = []
time_serv = []
time_last_end = []

def gen_rnd(kappa):
    return kappa*(1 - np.sqrt(1 - rnd.random()))

while time_event_last < time_model:
    time_event_last += gen_rnd(kappa)
    time_event.append(time_event_last)

for i in time_event:
    serv = gen_rnd(kappa)
    time_serv_sum += serv
    time_serv.append(gen_rnd(kappa))

for i in range(0, len(time_event) - 2):
    time_end = time_event[i] + time_serv[i]
    time_last_end.append(time_end)
    if time_event[i + 1] < time_end:
        n_serv += 1
    else:
        n_rej += 1

print(f' 1) Вероятность обслуживания = {round(n_serv/len(time_event), 3)}')
print(f' 2) Вероятность отказа = {round(n_rej/len(time_event), 3)}')
print(f' 3) Пропускная способность = {round(n_serv/time_model, 3)}')
# print(f' 4) Среднее количество занятых каналов = {}')
# print(f' 5) Вероятность простоя всей системы = {}')
# print(f' 6) Среднее количество заявок в очереди = {}')
# print(f' 7) Среднее время ожидания заявки в очереди = {}')
print(f' 8) Среднее время обслуживания заявки = {round(time_serv_sum/len(time_event), 3)}')
# print(f' 9) Среднее время нахождения заявки в системе = {}')
# print(f' 10) Среднее количество заявок в системе = {}')

