import numpy as np
import random
# from _thread import start_new_thread

alpha1 = 5
modeling_time = 24*60

# генерация события прихода заявки
time_event = []
last_time_event = 0
for time in range(0, modeling_time - 1):
    x = random.random()
    rnd = alpha1 - alpha1 * np.sqrt(1 - x)
    last_time_event += rnd
    time_event.append(last_time_event)
time_event.sort()

# генерация времи обслуживания запроса
serv_time = []
for time in time_event:
    # x = random.random() # случайное время обслуживания
    # rnd = alpha1 - alpha1 * np.sqrt(1 - x)
    rnd = 1 # фиксированное время обслуживания
    serv_time.append(rnd)

reject_serv = 0
take_serv = 0

# генерация времени простоя в случайный момент времи
# + генерация вероятностей отказа и обслуживания
i = random.randint(1, 100)
for time in range(0, len(time_event) - 2):
    count = random.randint(1, 100)
    if i < (len(time_event)):
        time_event[i] += 10
        time_end = time_event[time] + serv_time[time]
        i += count
    else:
        time_end = time_event[time] + serv_time[time]
    if time_event[time + 1] < time_end:
        reject_serv += 1
    else:
        take_serv += 1

reject_prob = reject_serv/len(time_event)
take_prob = take_serv/len(time_event)
throughput = take_serv/modeling_time
print(f'Вероятность отказа = {reject_prob}')
print(f'Вероятность обслуживания = {take_prob}')
print(f'Пропусканя способность = {throughput}')

