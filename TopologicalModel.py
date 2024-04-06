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

# Function to apply no-slip boundary conditions
def apply_boundary_conditions(velocity_field_x, velocity_field_y, velocity_field_z):
    # No-slip boundary conditions
    velocity_field_x[0,:,:] = velocity_field_y[0,:,:] = velocity_field_z[0,:,:] = 0  # Boundary at x=0
    velocity_field_x[-1,:,:] = velocity_field_y[-1,:,:] = velocity_field_z[-1,:,:] = 0  # Boundary at x=nx-1
    velocity_field_x[:,0,:] = velocity_field_y[:,0,:] = velocity_field_z[:,0,:] = 0  # Boundary at y=0
    velocity_field_x[:,-1,:] = velocity_field_y[:,-1,:] = velocity_field_z[:,-1,:] = 0  # Boundary at y=ny-1
    velocity_field_x[:,:,0] = velocity_field_y[:,:,0] = velocity_field_z[:,:,0] = 0  # Boundary at z=0
    velocity_field_x[:,:,-1] = velocity_field_y[:,:,-1] = velocity_field_z[:,:,-1] = 0  # Boundary at z=nz-1
    return velocity_field_x, velocity_field_y, velocity_field_z

# Function to solve pressure using Gauss-Seidel method
def solve_pressure(pressure_field, velocity_field_x, velocity_field_y, velocity_field_z):
    # Pressure solver using Gauss-Seidel method
    rhs = densityWater / dt * (np.gradient(velocity_field_x, axis=0) + np.gradient(velocity_field_y, axis=1) + np.gradient(velocity_field_z, axis=2))
    for _ in range(10):  # Example iterations for convergence
        for i in range(1, pressure_field.shape[0] - 1):
            for j in range(1, pressure_field.shape[1] - 1):
                for k in range(1, pressure_field.shape[2] - 1):
                    pressure_field[i, j, k] = (pressure_field[i+1, j, k] + pressure_field[i-1, j, k] +
                                               pressure_field[i, j+1, k] + pressure_field[i, j-1, k] +
                                               pressure_field[i, j, k+1] + pressure_field[i, j, k-1] -
                                               rhs[i, j, k]) / 6  # Gauss-Seidel update
    return pressure_field

# Function to apply fluid interactions using bounce-back scheme
def apply_fluid_interactions(velocity_field_x, velocity_field_y, velocity_field_z):
    # Bounce-back scheme for fluid-solid interactions
    # Assuming solid surface at z=0
    velocity_field_z[0,:,:] = -velocity_field_z[1,:,:]  # Flipping the velocity component normal to the solid surface
    return velocity_field_x, velocity_field_y, velocity_field_z

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
    pressure_field = np.zeros((nx, ny, nz))

    # Apply boundary conditions
    velocity_field_x, velocity_field_y, velocity_field_z = apply_boundary_conditions(velocity_field_x, velocity_field_y, velocity_field_z)

    # Main time loop
    while velocity_fields:
        _, i, j, k, pressure, vx, vy, vz = heapq.heappop(velocity_fields)

        # Update velocity fields
        velocity_field_x[i, j, k] = vx
        velocity_field_y[i, j, k] = vy
        velocity_field_z[i, j, k] = vz

        # Apply fluid interactions
        velocity_field_x, velocity_field_y, velocity_field_z = apply_fluid_interactions(velocity_field_x, velocity_field_y, velocity_field_z)

    # Solve pressure using Gauss-Seidel method
    pressure_field = solve_pressure(pressure_field, velocity_field_x, velocity_field_y, velocity_field_z)

    # Create quiver plot for velocity vector field
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
