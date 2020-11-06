import matplotlib.pyplot as plt
import numpy as np
import random
import keyboard

print('\nостановка построения траекторий - shift+s\n',
      'очистка экрана - shift+c')
# print('\nвведите количество фазовых траекторий\n и номер варианта системы.\n',
#       '1 - линейная система\n',
#       '2 - устойчивый узел\n',
#       '3 - устойчивый фокус\n',
#       '4 - седло\n',
#       '5 - консервативная система\n',
#       'иначе - задание по варианту\n')
m = 4
var = 7
h = 0.01
# m = int(input('введите число фазовых траекторий: '))
# var = int(input('введите номер варианта системы: '))
key_stop = 'shift+s'
key_clear = 'shift+c'
tp = np.arange(0, 15, h)
r = [[random.randint(1, 10)*0.1 for j in range(m)] for i in range(2)]

def f(r, t):
    fxd, fyd = [], []
    x, y = r[0], r[1]
    if var == 1:
        fxd = np.add(np.multiply(2, x), np.multiply(3, y))
        fyd = np.add(np.multiply(4, x), np.multiply(-2, y))
    elif var == 2:
        fxd = np.multiply(-2, x)
        fyd = np.multiply(-2, y)
    elif var == 3:
        fxd = np.add(np.multiply(1, x), np.multiply(-2, y))
        fyd = np.add(np.multiply(4, x), np.multiply(-3, y))
    elif var == 4:
        fxd = np.add(np.multiply(1, x), np.multiply(-2, np.power(x, 2)))
        fyd = np.add(np.multiply(-1, y), np.multiply(y, x))
    elif var == 5:
        fxd = y
        fyd = np.multiply(-1, x)
    else:
        fxd = np.subtract(np.subtract(y, np.power(x, 3)), np.multiply(x, np.power(y, 3)))
        fyd = np.subtract(np.multiply(x, -1), np.multiply(x, np.power(y, 2)))
    return np.array([fxd, fyd], float)

def rk4(r, t, h):
    k1 = np.multiply(h, f(r, t))
    k2 = np.multiply(h, f(np.add(r, np.multiply(0.5, k1)), np.add(t, 0.5*h)))
    k3 = np.multiply(h, f(np.add(r, np.multiply(0.5, k2)), np.add(t, 0.5*h)))
    k4 = np.multiply(h, f(np.add(r, np.multiply(1, k3)), np.add(t, h)))
    x1 = np.add(k1, np.multiply(2, k2))
    x2 = np.add(x1, np.multiply(2, k3))
    x3 = np.add(k4, x2)
    return np.multiply(x3, 1/6)

xpoints = []
ypoints = []

for t in tp:
    xpoints.append(rk4(r, 0, h)[0])
    ypoints.append(rk4(r, 0, h)[1])
    r += rk4(r, t, h)

def extract_point(xpoints, ypoints, i):
    x, y = [], []
    for j in range(0, len(xpoints)-1):
        x.append(xpoints[j][i])
        y.append(ypoints[j][i])
    return np.array([x, y], float)

## если раскомментировать этот кусочка кода
## (и закомментировать всю часть ниже этого кусочка), то отрисовка будет мгновенная

# for j in range(m):
#     point = extract_point(xpoints, ypoints, j)
#     plt.plot(point[0], point[1], 'k')
#     plt.xlabel("x[t]")
#     plt.ylabel("y[t]")
#     plt.title("Фазовые траектории")
#     plt.grid(True)
# plt.show()

plt.ion()
for k in range(0, np.shape(xpoints)[0]):
    for j in range(m):
        point = extract_point(xpoints, ypoints, j)
        plt.plot(point[0][0:k], point[1][0:k], 'k')
    plt.pause(0.00001)
    plt.draw()
    plt.gcf().canvas.flush_events()
    if keyboard.is_pressed(key_stop):
        plt.pause(20)
        break
    if keyboard.is_pressed(key_clear):
        plt.clf()
        break
    plt.xlabel("x[t]")
    plt.ylabel("y[t]")
    plt.title("Фазовые траектории")
    plt.grid(True)

plt.ioff()
plt.show()