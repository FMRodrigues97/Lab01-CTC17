import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import art3d


def f(x, y):
    f = 4 * np.exp(-x ** 2 - y ** 2 + 2 * (x + y - 1))
    f = f + np.exp(-(x + 3) ** 2 - (y - 3) ** 2)
    f = f + np.exp(-(x - 3) ** 2 - (y + 3) ** 2)
    f = f + np.exp(-(x - 3) ** 2 - (y - 3) ** 2)
    f = f + np.exp(-(x + 3) ** 2 - (y + 3) ** 2)

    return f


class plotar_superficie:
    def __init__(self, funcao):
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = funcao(X, Y)
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.plot_surface(X, Y, Z, color='k')

    def adicionar_ponto(self, point, color):
        p = Circle((point.x, point.y), 0.2, ec=color, fc="none")
        self.ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=point.z, zdir="z")

    def mostrar(self):
        plt.show()


class ponto:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def simmulated_annealing(espaco, funcao, T):
    ini_x = np.random.choice(espaco)
    ini_y = np.random.choice(espaco)

    x = ini_x * 1
    y = ini_y * 1
    z = funcao(x, y)

    for i in range(10000):
        prox_x = np.random.uniform(-5, 5)
        prox_y = np.random.uniform(-5, 5)
        prox_z = funcao(prox_x, prox_y)
        if prox_x > 5 or prox_x < -5 or prox_y > 5 or prox_y < -5 or np.log(np.random.rand()) * T > (prox_z - z):
            prox_x = x
            prox_y = y
            prox_z = z
        x = prox_x
        y = prox_y
        z = prox_z
        T = 0.99 * T  # reduzindo temperatura em 1% a cada iteração
        p = ponto(x, y, z)
        grafico_f.adicionar_ponto(p, color='b')

    return x, y, z


# chamando as funções
grafico_f = plotar_superficie(f)
espaco_x = np.linspace(-5, 5, 50)
espaco_y = np.linspace(-5, 5, 50)
x_aux, y_aux, z_aux = simmulated_annealing(espaco_x, f, T=100)

# printando último ponto
q = ponto(x_aux, y_aux, z_aux)
grafico_f.adicionar_ponto(q, color='r')

grafico_f.mostrar()
