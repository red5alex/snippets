import numpy as np
import matplotlib.pyplot as plt

# Generate data for the Gaussian curve
x = np.linspace(-5, 5, 1000)
mu, sigma = 0, 1

y = 1/(sigma*np.sqrt(2*np.pi))*np.exp(-(x-mu)**2/(2*sigma**2))

# Create the figure and plot the curve
fig, ax = plt.subplots()

ax.plot(x, y, label='Gaussian')

ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Add a vertical line at 1 standard deviation to the right of the mean
x_max = x[np.argmax(y)]
x_sd = mu + sigma

if x_sd > x_max:
    y_sd = 1/(sigma*np.sqrt(2*np.pi))*np.exp(-(x_sd-mu)**2/(2*sigma**2))
else:
    y_sd = np.max(y)

ax.vlines(x=x_sd, ymin=0, ymax=y_sd, linestyle='--', color='gray')
ax.fill_between(x[x>=x_sd], y[x>=x_sd], color='lightblue', alpha=0.5)

ax.set_title('One Gaussian Curve with a Vertical Line at 1 Standard Deviation to the Right of the Mean')

plt.show()
