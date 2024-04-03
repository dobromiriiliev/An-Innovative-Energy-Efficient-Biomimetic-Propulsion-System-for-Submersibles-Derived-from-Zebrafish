import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from queue import PriorityQueue
import time

# Constants
dt = 0.01  # Time step
densityWater = 1000.0
viscosity = 0.1

# Function to initialize a shape in the velocity field
def initialize_shape_single_point(i, j, k, nx, ny, nz):
    x = i / nx
    y = j / ny
    z = k / nz

    velocity_field_x = np.sin(densityWater * dt * viscosity * np.pi * x)
    velocity_field_y = np.cos(densityWater * dt * viscosity * np.pi * y)
    velocity_field_z = np.sin(densityWater * dt * viscosity * np.pi * z)

    return velocity_field_x, velocity_field_y, velocity_field_z

# Function to initialize velocity fields in parallel
def initialize_velocity_fields():
    results = PriorityQueue()
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                result = initialize_shape_single_point(i, j, k, nx, ny, nz)
                priority = np.random.random()  # Assign random priority
                results.put((priority, result))
    return results

# Size of the simulation grid
nx = 10
ny = 10
nz = 10

# Initialize velocity fields
start_time = time.time()
results = initialize_velocity_fields()
print("Initialization time:", time.time() - start_time)

# Create meshgrid
x = np.arange(0, nx)
y = np.arange(0, ny)
z = np.arange(0, nz)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Create arrays to store velocity field data
velocity_field_x = np.zeros((nx, ny, nz))
velocity_field_y = np.zeros((nx, ny, nz))
velocity_field_z = np.zeros((nx, ny, nz))

# Extract data from priority queue and assign to velocity field arrays
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            _, (vx, vy, vz) = results.get()
            velocity_field_x[i, j, k] = vx
            velocity_field_y[i, j, k] = vy
            velocity_field_z[i, j, k] = vz

# Create quiver plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, velocity_field_x, velocity_field_y, velocity_field_z, length=0.1, normalize=True)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(0, nx)
ax.set_ylim(0, ny)
ax.set_zlim(0, nz)
ax.set_title('Velocity Field')
plt.show()
