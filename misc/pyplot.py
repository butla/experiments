import matplotlib.pyplot as plt

x = list(range(100))
x_sq = [i**2 for i in x]

plt.plot(x, x_sq)
plt.show()
