import numpy as np
import random

alpha = 5
mu_1 = 1
mu_2 = 3
t_k = 24
alpha_1 = 1

t_c = 0
n = 0
n_serv, n_rej = 0, 0
t_pr_1, t_pr_2 = 0, 0
t_1, t_2, t_3, t_4 = 0, 0, 0, 0
t = 0

while t_c < t_k:
    # r = alpha_1 - alpha_1*np.sqrt(1-random.random())
    r = random.random()
    t_c = t_c - np.log(r)/alpha
    n += 1
    if t_c >= t_1:
        # r = alpha_1 - alpha_1 * np.sqrt(1 - random.random())
        r = random.random()
        t = t + (t_c - t_1)
        t_1 = t_c - np.log(r)/mu_1
        n_serv += 1
        t_pr_1 = abs(t_pr_1 + t_c - t_1)
    else:
        if t_c >= t_2:
            # r = alpha_1 - alpha_1 * np.sqrt(1 - random.random())
            r = random.random()
            t = t + (t_c - t_2)
            t_2 = t_c - np.log(r)/mu_2
            n_rej += 1
            t_pr_2 = abs(t_pr_2 + t_c - t_2)
        else:
            if t_c >= t_3:
                t_3 = min(t_1, t_2)
            else:
                if t_c >= t_4:
                    t_4 = t_3
                else:
                    n_serv += 1
                    n_rej += 1

print(f'\nпроизводительность системы A = {n_serv/t_k}')
print(f'вероятность обслуживания Pобс = {n_serv/n}')
print(f'вероятность отказа Pотк = {n_rej/n}')
print(f'вероятность простоя 1 канала Pпр1 = {t_pr_1/t_k}')
print(f'вероятность простоя 2 канала Pпр2 = {t_pr_2/t_k}')