import numpy as np
import matplotlib.pyplot as plt

# Фукнция вычисления вектора y
def linear_regression(m):
	matrix = np.zeros((n, m))
	for i in range(m):
		matrix[: ,i] = x**i
	w = np.linalg.inv(matrix.T @ matrix) @ matrix.T @ t
	y = matrix @ w.T 
	return y	

# Функция рисования решения задачи регрессии
def draw_regression(m):
	y = linear_regression(m)
	fig, ax = plt.subplots()
	ax.plot(x, z)
	title = 'M = {}'
	ax.set_title(title.format(m))
	ax.set_xlabel('x')
	ax.set_ylabel('z(x), t(x)')
	ax.scatter(x, t, 1, color='red')
	ax.plot(x, y, color='green')

# Функция построения графика зависимости ошибки от m 
def error_depend_regression():
	e = []
	m = np.arange(1, 101)
	for i in m:
		e.append(np.sum(((linear_regression(i) - t)**2))/2)
	fig, ax = plt.subplots()
	ax.plot(m, e, color='red')
	ax.set_title('График зависимости ошибки E(w) от степени полинома m')
	ax.set_xlabel('m')
	ax.set_ylabel('E(w)')


def complete_task():
	global n, x, z, error, t
	draw_regression(1)
	draw_regression(8)
	draw_regression(100)
	error_depend_regression()
	plt.show()


n = 1000
x = np.linspace(0, 1, n)
z = 20 * np.sin(2 * np.pi * 3 * x) + 100 * np.exp(x)
error = 10 * np.random.randn(n)
t = z + error
complete_task()
