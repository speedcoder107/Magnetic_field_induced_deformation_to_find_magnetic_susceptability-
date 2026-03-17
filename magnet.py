import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Halved x and y values
x_val = np.array([0.5, 0.6, 1, 8.9])
y_val = np.array([1, 0.95,  0.85, 0.35])

x_halved = np.array([0.25, 0.3, 0.5, 4.45])
y_halved = np.array([0.5, 0.475, 0.375, 0.0175])

# Define the function to fit
def func(x, k):
    return k / (x ** 2)

# Generate more x values for plotting
x_plot = np.linspace(min(x_halved), max(x_halved), 100)

# Perform curve fitting
popt, pcov = curve_fit(func, x_halved, y_halved)

# Extract the optimal value of k
k = popt[0]

print("Optimal value of k:", k)

# Plot scatter plot and the fitted curve
plt.scatter(x_halved, y_halved, color='blue', label='Halved data points')
plt.plot(x_plot, func(x_plot, k), color='red', label='Fitted curve')
plt.xlabel('Halved x values')
plt.ylabel('Halved y values')
plt.title('Fitting y = k / x^2')
plt.legend()
plt.grid(True)
plt.show()

y = 0.03737087483710961*2/3.5
y = 2*y
print(y)