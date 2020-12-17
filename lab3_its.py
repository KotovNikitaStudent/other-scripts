# import numpy as np
# import random
# # from _thread import start_new_thread
#
# alpha1 = 5
# modeling_time = 24*60
#
# # генерация события прихода заявки
# time_event = []
# last_time_event = 0
# for time in range(0, modeling_time - 1):
#     x = random.random()
#     rnd = alpha1 - alpha1 * np.sqrt(1 - x)
#     last_time_event += rnd
#     time_event.append(last_time_event)
# time_event.sort()
#
# # генерация времи обслуживания запроса
# serv_time = []
# for time in time_event:
#     # x = random.random() # случайное время обслуживания
#     # rnd = alpha1 - alpha1 * np.sqrt(1 - x)
#     rnd = 1 # фиксированное время обслуживания
#     serv_time.append(rnd)
#
# reject_serv = 0
# take_serv = 0
#
# # генерация времени простоя в случайный момент времи
# # + генерация вероятностей отказа и обслуживания
# i = random.randint(1, 100)
# for time in range(0, len(time_event) - 2):
#     count = random.randint(1, 100)
#     if i < (len(time_event)):
#         time_event[i] += 10
#         time_end = time_event[time] + serv_time[time]
#         i += count
#     else:
#         time_end = time_event[time] + serv_time[time]
#     if time_event[time + 1] < time_end:
#         reject_serv += 1
#     else:
#         take_serv += 1
#
# reject_prob = reject_serv/len(time_event)
# take_prob = take_serv/len(time_event)
# throughput = take_serv/modeling_time
# print(f'Вероятность отказа = {reject_prob}')
# print(f'Вероятность обслуживания = {take_prob}')
# print(f'Пропусканя способность = {throughput}')

import numpy as np
import random

# alpha = float(input())
# mu_1 = float(input())
# mu_2 = float(input())
# t_k = float(input())

alpha = 5
mu_1 = 1
mu_2 = 3
t_k = 24

t_c = 0
n = 0
n_serv, n_rej = 0, 0
t_pr_1, t_pr_2 = 0, 0
t_1, t_2, t_3, t_4 = 0, 0, 0, 0
t = 0

alpha_1 = 5
# tc = []
while t_c < t_k:
    x = random.random()
    r = alpha_1 - alpha_1*np.sqrt(1-x)
    t_c += (1/alpha)*np.log(r)
    n += 1
    if t_c >= t_1:
        # x = random.random()
        # r = alpha_1 - alpha_1 * np.sqrt(1 - x)
        t += (t_c - t_1)
        t_1 = t_c - (1/mu_1)*np.log(r)
        n_rej += 1
        t_pr_1 += t_c - t_1
    elif t_c >= t_2:
        # x = random.random()
        # r = alpha_1 - alpha_1 * np.sqrt(1 - x)
        t += (t_c - t_2)
        t_2 = t_c - (1/mu_2) * np.log(r)
        n_rej += 1
        t_pr_2 += t_c - t_2
    elif t_c >= t_3:
        t_3 = min(t_1, t_2)
    elif t_c >= t_4:
        t_4 = t_3
    else:
        n_serv += 1
        n_rej += 1

print('\n')
print(f'производительность системы A = {n_serv/t_k}')
print(f'вероятность обслуживания Pобс = {n_serv/n}')
print(f'вероятность отказа Pотк = {n_rej/n}')
print(f'вероятность простоя 1 канала Pпр1 = {t_pr_1/t_k}')
print(f'вероятность простоя 2 канала Pпр2 = {t_pr_2/t_k}')
