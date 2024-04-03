import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import queue

# Size of the simulation grid
nx = 20
ny = 20
nz = 20

# Constants
dt = 0.01  # Time step
densityWater = 1000.0
viscosity = 0.1

# Function to initialize a shape in the velocity field
def initializeShape_single_point(i, j, k):
    x = i / nx
    y = j / ny
    z = k / nz

    velocityFieldX = np.sin(densityWater * dt * viscosity * np.pi * x)
    velocityFieldY = np.cos(densityWater * dt * viscosity * np.pi * y)
    velocityFieldZ = np.sin(densityWater * dt * viscosity * np.pi * z)

    return velocityFieldX, velocityFieldY, velocityFieldZ

# Worker function to initialize shape in parallel
def worker(q):
    while True:
        try:
            i, j, k = q.get(block=False)
            result = initializeShape_single_point(i, j, k)
            q.task_done()
            yield result
        except queue.Empty:
            break

# Initialize velocity fields using queue system
q = queue.Queue()

# Put tasks into the queue
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            q.put((i, j, k))

# Initialize velocity fields
results = list(worker(q))

# Reshape results to match grid dimensions
velocityFieldX = np.zeros((nx, ny, nz))
velocityFieldY = np.zeros((nx, ny, nz))
velocityFieldZ = np.zeros((nx, ny, nz))

for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            index = i * ny * nz + j * nz + k
            vx, vy, vz = results[index]
            velocityFieldX[i, j, k] = vx
            velocityFieldY[i, j, k] = vy
            velocityFieldZ[i, j, k] = vz

# Create meshgrid
x = np.arange(0, nx)
y = np.arange(0, ny)
z = np.arange(0, nz)
X, Y, Z = np.meshgrid(x, y, z)

# Create quiver plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, velocityFieldX, velocityFieldY, velocityFieldZ, length=0.1, normalize=True)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Velocity Field')
plt.show()
