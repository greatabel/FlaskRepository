import os
import scipy as sp

sp.random.seed(3)

data = sp.genfromtxt("../data/i1processed_steel_price.csv", delimiter=",")
print(data[:3])
print(data.shape)

x = data[:,0]
y = data[:,1]
print('x=', x[:3])
print('y=', y[:3])

print('sp.sum(sp.isnan(y))=',sp.sum(sp.isnan(y)) )
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]
print(x[:3])
print(y[:3])

import matplotlib.pyplot as plt

plt.scatter(x,y, s=26)
plt.title("price over the last n year")
plt.xlabel("Time")
plt.ylabel("price/time")
plt.xticks([w*12 for w in range(26)],
    ['%i' % w for w in range(26)])
plt.autoscale(tight=True)
plt.grid(True, linestyle='-', color='0.75')
plt.show()
plt.save('i3.png')