# Animated Gradient Decent, Alex Falkovskiy, May 2022
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import math

fig, ax = plt.subplots()

length=10
alpha = 0.8
nIterations = 10
length = nIterations

# objective function
def F(x1, x2):
    y = np.sin(x1) * np.cos(x2) - 0.04*(x1-2)**2 - 0.02*(x2-1)**2 + 0.2*x1
    return y
# derivative
def dF(x1, x2):
    dFx1 = math.cos(x1) * math.cos(x2) - 2.*0.04*(x1-2) + 0.2
    dFx2 = -math.sin(x1) * math.sin(x2) - 2.*0.02*(x2-1)
    return dFx1, dFx2

def gen_lineData(length=10, dims=2):
    lineData = np.empty((dims, length), dtype=float)
    lineData[:, 0] = np.zeros(dims)

    x1 = np.random.uniform(-2, 2.5)
    x2 = np.random.uniform(-2.5, 2.5)
    lineData[0, 0] = x1
    lineData[1, 0] = x2

    for idx in range(1, length):
        dFdx1, dFdx2 = dF(x1, x2)

        dx1 = - alpha * dFdx1
        dx2 = - alpha * dFdx2

        x1 = x1 + dx1
        x2 = x2 + dx2

        lineData[0, idx] = x1
        lineData[1, idx] = x2

    return lineData

# def init():

def animate(i, data, lines):
    line_current = math.ceil(i/length) % nlines
    current_el = i%length

    line_num = 0
    for line, dat in zip(lines, data):

        if line_num < line_current:
            line.set_xdata(dat[0, :length])
            line.set_ydata(dat[1, :length])
        if line_num == line_current:
            m1 = max(current_el, 1)
            if current_el == 0 and i > 0:
                m1 = length
            line.set_xdata(dat[0, :m1])
            line.set_ydata(dat[1, :m1])
        if line_num > line_current:
            line.set_xdata(dat[0, 0])
            line.set_ydata(dat[1, 0])

        line_num = line_num + 1

    return lines,

nlines = 20
data = [gen_lineData() for index in range(nlines)]

lines = []
x1 = np.linspace(0, 10, length)
x2 = np.linspace(0, 10, length)
for dat in data:
    line, = ax.plot(x1, x2, '--', color='darkred')
    lines.append(line)

for line, dat in zip(lines, data):
    print('dat0: ', dat[0, :10])
    print('dat1: ', dat[1, :10])

plt.text(1.3, 3.2, 'Min1', c='navy', size=12, fontweight='bold')
plt.text(-2., -0.5, 'Min2-global', c='navy', size=12, fontweight='bold')
plt.text(1.2, -3.2, 'Min3', c='navy', size=12, fontweight='bold')

x = np.arange(-5.0, 5.0, 0.1)
y = np.arange(-5.0, 5.0, 0.1)

X, Y = np.meshgrid(x, y)
Z = F(X, Y)

mycmap1 = plt.get_cmap('gist_earth')
ax.set_aspect('equal')
ax.set_title('Gradient Descent on several local minimums')
cf1 = ax.contourf(X,Y,Z, cmap='RdGy', alpha=0.7)

CS = ax.contour(x, y, Z, levels=np.arange(-5, 5, 0.2))
ax.clabel(CS, inline=True, colors=('k'), fontsize=9)

ax.set_xlim([-3.5,4.5])
ax.set_ylim([-5,5])

ax.set_xlim([-4, 4])
ax.set_ylim([-4,4])

fig.colorbar(cf1, ax=ax)

plt.grid()

ani = animation.FuncAnimation(
    fig, animate,  interval=30, fargs=(data, lines), blit=False, save_count=300)


ani.save('grad_dec_anim.gif', writer='imagemagick', fps=15)

plt.show()