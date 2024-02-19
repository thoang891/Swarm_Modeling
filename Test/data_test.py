import pandas as pd

# Sample DataFrame
data = {
    'Time': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'behv': ['seeker', 'seeker', 'seeker', 'seeker', 'seeker', 'explorer', 'explorer', 'explorer', 'explorer', 'explorer'],
    'com_radius': [5.0, 5.0, 5.0, 5.0, 5.0, 10.0, 10.0, 10.0, 10.0, 10.0],
    'Battery': [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
    'x': [-1.3, 8.2, -0.7, -2.5, 3.4, -3.0, -0.3, 6.8, -8.8, 4.5],
    'y': [-7.2, 1.2, -9.0, 7.8, -1.6, 6.0, 6.5, 9.0, 3.1, -4.4],
    'Measurement': [-33.098, -61.066, -36.053, -221.483, -16.100, -184.100, -164.200, -218.000, -242.200, -1.400],
    'u': [None, None, None, None, None, None, None, None, None, None],
    'v': [None, None, None, None, None, None, None, None, None, None],
    'speed': [None, None, None, None, None, None, None, None, None, None],
    'best_x': [-1.3, 8.2, -0.7, -2.5, 3.4, -3.0, -0.3, 6.8, -8.8, 4.5],
    'best_y': [-7.2, 1.2, -9.0, 7.8, -1.6, 6.0, 6.5, 9.0, 3.1, -4.4],
    'best_measure': [-54.170, -68.322, -81.712, -66.836, -14.282, -44.900, -42.300, -127.200, -86.500, -39.200],
    'best_id': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
}

df = pd.DataFrame(data)

# Group by 'Time' and calculate the mean of 'best_x' for each time step
average_best_x = df.groupby('Time')['best_x'].mean().reset_index()
average_best_x.columns = ['Time', 'average_best_x']

# Display the resulting DataFrame
print(average_best_x)
