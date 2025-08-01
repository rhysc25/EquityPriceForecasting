from DataProcess import timeArray, vwArray
import matplotlib.pyplot as plt

plt.figure(1)
plt.clf()
plt.xlabel('time (s)')
plt.grid()
plt.plot(timeArray, vwArray, label='Volume Weighted Average Price')
plt.legend()
plt.show()
