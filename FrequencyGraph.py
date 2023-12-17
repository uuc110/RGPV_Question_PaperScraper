import matplotlib.pyplot as plt

# Data for plotting - Overall frequency of topics in each unit
units = ['Unit I', 'Unit II', 'Unit III', 'Unit IV', 'Unit V']
overall_frequency = [5, 3, 2, 3, 3]  # Overall frequency count of topics in each unit

# Plotting the bar graph
plt.figure(figsize=(10, 6))
plt.bar(units, overall_frequency, color='orange')

plt.xlabel('Units')
plt.ylabel('Overall Topic Frequency')
plt.title('Overall Frequency of Topics per Unit in OOAD Course')
plt.xticks(units)
plt.ylim(0, max(overall_frequency) + 1)  # Setting the y-axis limit
plt.grid(axis='y')

# Show the plot
plt.show()
