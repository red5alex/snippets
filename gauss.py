import numpy as np
import matplotlib.pyplot as plt

# Use XKCD style
plt.xkcd()

# Generate data for the Gaussian curves
x = np.linspace(-5, 5, 1000)
mu1, sigma1 = 0, 1
mu2, sigma2 = mu1 + 0.5*sigma1, sigma1

y1 = 1/(sigma1*np.sqrt(2*np.pi))*np.exp(-(x-mu1)**2/(2*sigma1**2))
y2 = 1/(sigma2*np.sqrt(2*np.pi))*np.exp(-(x-mu2)**2/(2*sigma2**2))

# Create the figure and plot the curves
fig, ax = plt.subplots()

ax.plot(x, y1, label='Gaussian 1')
ax.plot(x, y2, label='Gaussian 2')

ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Add annotations and style
ax.annotate('Half Standard Deviation', xy=(mu2+0.5*sigma2, 0.4), xytext=(mu2+2, 0.8),
            arrowprops=dict(arrowstyle='->', lw=1),
            fontsize=12)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_title('Two Gaussian Curves Separated by 0.5 Standard Deviation')

plt.show()
