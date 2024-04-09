import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import heapq
from multiprocessing import Pool


# Constants
dt = 0.01  # Time step
densityWater = 1000.0
viscosity = 0.1
cs = 0.1  # Smagorinsky coefficient
dx = dy = dz = 1  # Grid spacing

# Function to compute turbulent viscosity using Smagorinsky-Lilly model
def compute_turbulent_viscosity(S):
    nu_t = (cs * dx)**2 * np.sqrt(2 * np.sum(S**2))
    return nu_t

# Function to compute velocity field value with turbulence using Smagorinsky-Lilly model
def compute_velocity_field(args):
    i, j, k, nx, ny, nz = args
    x = i / nx
    y = j / ny
    z = k / nz

    pressure = np.sin(np.pi * x) * np.cos(np.pi * y) * np.sin(np.pi * z)

    # Turbulence computation using Smagorinsky-Lilly model
    turbulence_intensity = 0.1  
    turbulence_x = turbulence_intensity * np.random.normal()
    turbulence_y = turbulence_intensity * np.random.normal()
    turbulence_z = turbulence_intensity * np.random.normal()

    # Velocity computation
    velocity_field_x = np.sin(densityWater * dt * viscosity * np.pi * x) + turbulence_x
    velocity_field_y = np.cos(densityWater * dt * viscosity * np.pi * y) + turbulence_y
    velocity_field_z = np.sin(densityWater * dt * viscosity * np.pi * z) + turbulence_z

    return (i + j + k, i, j, k, pressure, velocity_field_x, velocity_field_y, velocity_field_z)

# Function to initialize velocity fields using multiprocessing
def initialize_velocity_fields_parallel(nx, ny, nz):
    with Pool() as pool:
        args_list = [(i, j, k, nx, ny, nz) for i in range(nx) for j in range(ny) for k in range(nz)]
        results = pool.map(compute_velocity_field, args_list)
        return results

if __name__ == "__main__":
    # Size of the simulation grid
    nx = 100
    ny = 100
    nz = 100

    # Initialize velocity fields using multiprocessing
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