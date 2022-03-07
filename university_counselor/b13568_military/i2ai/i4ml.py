import os
import scipy as sp
from termcolor import colored,cprint
import matplotlib.pyplot as plt

# http://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html

sp.random.seed(3)

def error(f, x,y):
    return sp.sum( (f(x) - y)**2 )

data = sp.genfromtxt("../data/i1processed_steel_price.csv", delimiter=",")
print(data[:3])
print(data.shape)

x = data[:,0]
y = data[:,1]

x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]

plt.scatter(x,y, s=26)
plt.title("traffic over the last n year")
plt.xlabel("Time")
plt.ylabel("price/time")
plt.xticks([w*12 for w in range(26)],
    ['%i' % w for w in range(26)])
plt.autoscale(tight=True)
plt.grid(True, linestyle='-', color='0.75')
# plt.show()



# create and plot models
fp1, res1, rank1, sv1, rcond1 = sp.polyfit(x, y, 1, full=True)
print('#'*10,fp1, res1, rank1, sv1, rcond1,'#'*10)
print("Model parameters of fp1: %s" % fp1)
print("Error of the model of fp1:", res1)
f1 = sp.poly1d(fp1)
print(colored('error=','red'),error(f1, x, y))

fx = sp.linspace(0,x[-1], 1000) 
# generate X-values for plotting
plt.plot(fx, f1(fx), linewidth=4)
plt.legend(["d=%i" % f1.order], loc="upper left")
plt.show()