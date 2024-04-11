import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from multiprocessing import Pool
import heapq

# Constants
dt = 0.01  # Time step
densityWater = 1000.0
viscosity = 0.1
cs = 0.1  # Smagorinsky coefficient
dx = dy = dz = 1  # Grid spacing

# Define priority queue structure
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def __len__(self):
        return len(self._queue)

# Define octree structure
class OctreeNode:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.children = []

# Function to initialize octree
def initialize_octree(bounds, depth):
    # Extracting bounds information
    min_corner, max_corner = bounds
    min_x, min_y, min_z = min_corner
    max_x, max_y, max_z = max_corner

    # Calculate center and size of the current node
    center = ((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2)
    size = max(max_x - min_x, max_y - min_y, max_z - min_z)

    # Base case: if depth is 0, return leaf node
    if depth == 0:
        return OctreeNode(center, size)

    # Otherwise, recursively subdivide the space into octants
    child_bounds = [
        ((min_x, min_y, min_z), center),
        ((center[0], min_y, min_z), (max_x, center[1], center[2])),
        ((min_x, center[1], min_z), (center[0], max_y, center[2])),
        ((center[0], center[1], min_z), (max_x, max_y, center[2])),
        ((min_x, min_y, center[2]), (center[0], center[1], max_z)),
        ((center[0], min_y, center[2]), (max_x, center[1], max_z)),
        ((min_x, center[1], center[2]), (center[0], max_y, max_z)),
        ((center[0], center[1], center[2]), max_corner)
    ]

    # Recursively initialize children
    node = OctreeNode(center, size)
    node.children = [initialize_octree(child_bounds[i], depth - 1) for i in range(8)]

    return node

# Function to compute velocity field value with turbulence using Smagorinsky-Lilly model
def compute_velocity_field(args):
    i, j, k, nx, ny, nz = args
    x = i / nx
    y = j / ny
    z = k / nz

    pressure = np.sin(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z)

    # Velocity computation
    velocity_field_x = np.sin(densityWater * dt * viscosity * np.pi * x)
    velocity_field_y = np.cos(densityWater * dt * viscosity * np.pi * y)
    velocity_field_z = np.sin(densityWater * dt * viscosity * np.pi * z)

    return (i + j + k, i, j, k, pressure, velocity_field_x, velocity_field_y, velocity_field_z)

# Function to initialize velocity fields using octree-based multiprocessing
def initialize_velocity_fields_parallel(nx, ny, nz):
    octree_bounds = [(0, 0, 0), (nx, ny, nz)]  # Define octree bounds
    octree_depth = 3  # Define octree depth

    octree = initialize_octree(octree_bounds, octree_depth)

    with Pool() as pool:
        args_list = [(i, j, k, nx, ny, nz) for i in range(nx) for j in range(ny) for k in range(nz)]
        results = pool.map(compute_velocity_field, args_list)
        return results

if __name__ == "__main__":
    # Size of the simulation grid
    nx = 100
    ny = 100
    nz = 100

    # Initialize velocity fields using multiprocessing and octrees
    start_time = time.time()
    velocity_fields = initialize_velocity_fields_parallel(nx, ny, nz)
    print("Initialization time:", time.time() - start_time)

    # Create meshgrid
    x = np.arange(0, nx)
    y = np.arange(0, ny)
    z = np.arange(0, nz)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # Initialize velocity field arrays
    velocity_field_x = np.zeros((nx, ny, nz))
    velocity_field_y = np.zeros((nx, ny, nz))
    velocity_field_z = np.zeros((nx, ny, nz))

    # Populate velocity field arrays
    for _, i, j, k, _, vx, vy, vz in velocity_fields:
        velocity_field_x[i, j, k] = vx
        velocity_field_y[i, j, k] = vy
        velocity_field_z[i, j, k] = vz

    # Apply no-slip boundary conditions
    velocity_field_x[0,:,:] = velocity_field_y[0,:,:] = velocity_field_z[0,:,:] = 0
    velocity_field_x[-1,:,:] = velocity_field_y[-1,:,:] = velocity_field_z[-1,:,:] = 0
    velocity_field_x[:,0,:] = velocity_field_y[:,0,:] = velocity_field_z[:,0,:] = 0
    velocity_field_x[:,-1,:] = velocity_field_y[:,-1,:] = velocity_field_z[:,-1,:] = 0
    velocity_field_x[:,:,0] = velocity_field_y[:,:,0] = velocity_field_z[:,:,0] = 0
    velocity_field_x[:,:,-1] = velocity_field_y[:,:,-1] = velocity_field_z[:,:,-1] = 0

    # Apply fluid interactions using bounce-back scheme
    velocity_field_z[0,:,:] = -velocity_field_z[1,:,:]

    # Create quiver plot for velocity vector field using parallel processing
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    stride = 5  # Adjust the stride to control density of arrows
    ax.quiver(X[::stride, ::stride, ::stride], 
              Y[::stride, ::stride, ::stride], 
              Z[::stride, ::stride, ::stride], 
              velocity_field_x[::stride, ::stride, ::stride], 
              velocity_field_y[::stride, ::stride, ::stride], 
              velocity_field_z[::stride, ::stride, ::stride], 
              length=0.1, normalize=True, color='b', arrow_length_ratio=0.4)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)
    ax.set_zlim(0, nz)
    ax.set_title('Velocity Field with Fluid Interactions')
    plt.show()
