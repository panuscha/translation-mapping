import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['svg.fonttype'] = 'none'

# Create a figure and axis
fig, ax = plt.subplots()

# Add text at specified coordinates (x, y)
ax.text(0.5, 0.5,'poměr zastoupení dalších jazyků', fontsize=16, ha='center', va='center')

# Hide the axes for a clean text image
ax.axis('off')

plt.savefig('plots/with title/dummy charts/pomer_zastoupeni.svg', transparent=True)