# Example list of dictionaries representing the data frame
swarm_data = [
    {'ID': 1, 'x': 10, 'y': 20, 'measurement': 5},
    {'ID': 2, 'x': 15, 'y': 25, 'measurement': 8},
    {'ID': 3, 'x': 5, 'y': 15, 'measurement': 10}
]

# Find the dictionary with the maximum z value using the max() function with a custom key function
max_data = max(swarm_data, key=lambda x: x['measurement'])

# Extract relevant values
max_id = max_data['ID']
max_x = max_data['x']
max_y = max_data['y']
max_measurement = max_data['measurement']

# Print the corresponding ID, position, and measurement values
print("Maximum z value: {}".format(max_measurement))
print("Corresponding ID: {}".format(max_id))
print("Corresponding position: ({}, {})".format(max_x, max_y))