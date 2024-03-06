import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots()

# Add text at specified coordinates (x, y)
ax.text(0.5, 0.5,'podíl překladů do dalších jazyků', fontsize=16, ha='center', va='center')

# Hide the axes for a clean text image
ax.axis('off')

plt.savefig('plots/with title/dummy charts/podil_prekladu.svg', transparent=True)