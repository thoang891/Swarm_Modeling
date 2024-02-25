import numpy as np

# Function to calculate the polar angle of a point with respect to the center of the circle
def polar_angle(x, y):
    return np.arctan2(y, x)

# Function to calculate the distance between two points
def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Function to estimate the arc length of a bunch of dots aligned in a circle
def estimate_arc_length(dots):
    # Calculate the center of the circle
    center_x = np.mean([dot[0] for dot in dots])
    center_y = np.mean([dot[1] for dot in dots])
    
    # Sort the dots based on their polar angle with respect to the center of the circle
    sorted_dots = sorted(dots, key=lambda dot: polar_angle(dot[0] - center_x, dot[1] - center_y))
    
    # Calculate the distances between adjacent dots
    arc_lengths = []
    for i in range(len(sorted_dots) - 1):
        x1, y1 = sorted_dots[i]
        x2, y2 = sorted_dots[i + 1]
        arc_lengths.append(distance(x1, y1, x2, y2))
    
    # Sum up the distances to estimate the total arc length
    total_arc_length = sum(arc_lengths)
    return total_arc_length

# Example usage:
# dots = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Example dots forming a circle
dots = [(0, 0), (0, 1), (0, 2), (2, 2)]
arc_length = estimate_arc_length(dots)
print("Estimated arc length:", arc_length)
