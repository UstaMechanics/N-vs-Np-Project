import math
import matplotlib.pyplot as plt

# Function to calculate Euclidean distance
def euclidean_distance(x, y):
    return math.sqrt(x**2 + y**2)

# Function to calculate the distance between two points
def distance_between_points(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Function to calculate the external tangent intersection points of two circles
def external_tangent_intersections(center1, r1, center2, r2):
    d = distance_between_points(center1, center2)
    
    # Check if the circles intersect externally
    if d > r1 + r2 or d < abs(r1 - r2):
        return []  # No intersection or one circle is within the other
    
    # Calculate the external tangent intersection points
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h = math.sqrt(r1**2 - a**2)
    midpoint = (center1[0] + a * (center2[0] - center1[0]) / d,
                center1[1] + a * (center2[1] - center1[1]) / d)
    
    intersection1 = (midpoint[0] + h * (center2[1] - center1[1]) / d,
                     midpoint[1] - h * (center2[0] - center1[0]) / d)
    intersection2 = (midpoint[0] - h * (center2[1] - center1[1]) / d,
                     midpoint[1] + h * (center2[0] - center1[0]) / d)
    
    return [intersection1, intersection2]

# Function to check if a point is inside a circle
def is_point_inside_circle(point, center, radius):
    return distance_between_points(point, center) < radius

# Ask the user how many points they want to input
num_points = int(input("How many points do you want to enter? "))

# Collect points from the user
points = []
for i in range(num_points):
    x = float(input(f"Enter the x-coordinate of point {i+1}: "))
    y = float(input(f"Enter the y-coordinate of point {i+1}: "))
    points.append((x, y))

# Find the farthest and nearest points from the origin
max_distance_point = max(points, key=lambda point: euclidean_distance(point[0], point[1]))
min_distance_point = min([point for point in points if point != (0, 0)], key=lambda point: euclidean_distance(point[0], point[1]))

# Calculate the distances for the farthest and nearest points
max_distance = euclidean_distance(max_distance_point[0], max_distance_point[1])
min_distance = euclidean_distance(min_distance_point[0], min_distance_point[1])

# Print the results
print(f"Farthest point: {max_distance_point}, Distance: {max_distance}")
print(f"Nearest point: {min_distance_point}, Distance: {min_distance}")

# Plot points and circles
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')

# Draw circles with max_distance radius around each point
for point in points:
    ax.plot(point[0], point[1], 'bo')  # Blue points
    circle = plt.Circle((point[0], point[1]), max_distance, color='g', fill=False, linestyle='--')  # Green dashed circles
    ax.add_artist(circle)

# Plot the origin
ax.plot(0, 0, 'ro')  # Red point

# Calculate valid intersection points
valid_intersections = []
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        p1 = points[i]
        p2 = points[j]
        r1 = max_distance
        r2 = max_distance
        
        # Calculate external tangent intersection points
        intersections = external_tangent_intersections(p1, r1, p2, r2)
        for intersection in intersections:
            # Check if the intersection point is outside all circles
            if all(not is_point_inside_circle(intersection, point, max_distance) for point in points):
                valid_intersections.append(intersection)

# Plot valid intersection points
for intersection in valid_intersections:
    ax.plot(intersection[0], intersection[1], 'ko')  # Black points for intersections
    intersection_circle = plt.Circle(intersection, min_distance, color='r', fill=False, linestyle=':')  # Red dotted circles
    ax.add_artist(intersection_circle)

# Set the graph limits
ax.set_xlim(min(point[0] - max_distance for point in points) - 1, 
            max(point[0] + max_distance for point in points) + 1)
ax.set_ylim(min(point[1] - max_distance for point in points) - 1, 
            max(point[1] + max_distance for point in points) + 1)

# Show the graph
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Points, Circles, and Valid External Tangent Intersections')
plt.grid(True)
plt.show()
