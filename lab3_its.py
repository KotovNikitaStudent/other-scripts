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
