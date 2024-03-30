import numpy as np
import math

def map_value(current_min: float, current_max: float,
              new_min: float, new_max: float, value: float)->float:
    """Remap value from one range to another"""
    current_range = current_max - current_min
    new_range = new_max - new_min

    ratio = (value-current_min)/current_range
    return (new_min + new_range) * ratio

def save_canvas():
    with open("canvas.txt", "w") as f:
        f.write(f"{len(ptcache)}\n")
        for cache in ptcache:
            f.write(f"{len(cache)}\n")
            for coord in cache:
                f.write(f"{coord[0]} {coord[1]}\n")
    print("Canvas is saved!")

def load_canvas():
    with open("./canvas.txt", "r") as file:
        global points
        global ptcache
        cache_num = int(file.readline())

        ptcache = []
        for cache in range(cache_num):
            points = []
            ptcache.append(points)
            point_num = int(file.readline())
            for p in range(point_num):
                px, py = [float(value) for value in next(file).split()]
                points.append((px,py))

def plot_graph():
    for px in np.arange(0, 4, 0.005):
        py = math.exp(-px) * math.cos(2*math.pi * px)
        px = map_value(0,4,ortho_width[0],ortho_width[1],px)
        py = map_value(-1,1,ortho_height[0],ortho_height[1],py)
        points.append((px,py))
    ptcache.append(points)

def x_rotation(vector, theta):
    new_vector = np.array([[1,0,0], [0, np.cos(theta), -np.sin(theta)],
                           [0, np.sin(theta), np.cos(theta)]])
    return np.dot(new_vector, vector)

def y_rotation(vector, theta):
    new_vector = np.array([[np.cos(theta), 0, np.sin(theta)], [0,1,0],
                           [-np.sin(theta), 0, np.cos(theta)]])
    return np.dot(new_vector, vector)

def z_rotation(vector, theta):
    new_vector = np.array([[np.cos(theta), -np.sin(theta), 0],
                           [np.sin(theta), np.cos(theta), 0], [0,0,1]])
    return np.dot(new_vector, vector)
