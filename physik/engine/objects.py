# Object class
import json
from jinja2 import pass_context


class Object():
    # MARK: - Initialize
    # Initialize the object
    def __init__(self, name:str, mass:float, position, velocity, acceleration, vector, size:float, color:list=None, force:float=None, torque=None, angular_velocity=None, angular_acceleration=None, angular_vector=None, moment_of_inertia=None, center_of_mass=[0,0,0], orientation=None, angular_momentum=None, angular_impulse=None, orientation_matrix=None, orientation_matrix_inverse=None, orientation_matrix_transpose=None, orientation_matrix_transpose_inverse=None):
        self.name = name # str (name of the object) (e.g. "ball", "car", "plane", "rocket", etc.)
        self.mass = mass # kg (mass of the object) (m) (e.g. 1, 2, 3, 4, 5, etc.) is the amount of matter in an object
        self.position = position # m (position of the object) (x, y, z) is the location of the object in space
        self.velocity = velocity # m/s (velocity of the object) (v) (dx/dt, dy/dt, dz/dt) is the rate of change of position of the object
        self.acceleration = acceleration # m/s^2 (acceleration of the object) (a) (d^2x/dt^2, d^2y/dt^2, d^2z/dt^2) is the rate of change of velocity of the object
        self.vector = vector # m/s (vector of the object) (vx, vy, vz) is the direction and magnitude of the object's motion
        self.size = size # m (size of the object) (radius for a sphere) is the distance from the center of the object to the edge of the object
        self.color = color # (r, g, b) (color of the object) (e.g. (255, 0, 0) for red, (0, 255, 0) for green, (0, 0, 255) for blue, etc.) is the appearance of the object
        self.force = force # N (force acting on the object) (F=m*a) (e.g. 1, 2, 3, 4, 5, etc.) is the interaction that changes the motion of the object
        self.torque = torque # Nm (torque acting on the object) (τ) (e.g. 1, 2, 3, 4, 5, etc.) is the interaction that changes the rotation of the object
        self.angular_velocity = angular_velocity # rad/s (angular velocity of the object) (dθ/dt) is the rate of change of orientation of the object
        self.angular_acceleration = angular_acceleration # rad/s^2 (angular acceleration of the object) (d^2θ/dt^2) is the rate of change of angular velocity of the object
        self.angular_vector = angular_vector # rad/s (angular vector of the object) (ωx, ωy, ωz) is the direction and magnitude of the object's rotation
        self.moment_of_inertia = moment_of_inertia # kg*m^2 (moment of inertia of the object) (e.g. 1, 2, 3, 4, 5, etc.) is the resistance of the object to changes in its rotation
        self.center_of_mass = center_of_mass # m (center of mass of the object) (x, y, z) is the average position of the mass of the object in its own coordinate system where 0 0 0 is the origin of the objects projection and 1 1 1 is the maximum size of the object in the objects projection (e.g. 0.5 0.5 0.5 is the center of the object) and -1 -1 -1 is the minimum size of the object in the objects projection (e.g. 0 0 0 is normally the center of the object)
        self.orientation = orientation # rad (orientation of the object) (θ) is the angle of the object's rotation 
        self.angular_momentum = angular_momentum # kg*m^2/s (angular momentum of the object) (L) is the quantity of rotation of the object
        self.angular_impulse = angular_impulse # Nm*s (angular impulse of the object) (J) is the change in angular momentum of the object
        self.orientation_matrix = orientation_matrix # 3x3 matrix (orientation matrix of the object) is the matrix that transforms the object's local coordinate system to the world coordinate system
        self.orientation_matrix_inverse = orientation_matrix_inverse # 3x3 matrix (inverse orientation matrix of the object) is the matrix that transforms the world coordinate system to the object's local coordinate system
        
    
    # MARK: - Edit
    # Edit the object
    def edit(self, name=None, mass=None, position=None, velocity=None, acceleration=None, vector=None, size=None, color=None, force=None, torque=None, angular_velocity=None, angular_acceleration=None, angular_vector=None, moment_of_inertia=None, center_of_mass=None, orientation=None, angular_momentum=None, angular_impulse=None, orientation_matrix=None, orientation_matrix_inverse=None):
        if name:
            self.name = name
        if mass:
            self.mass = mass
        if position:
            self.position = position
        if velocity:
            self.velocity = velocity
        if acceleration:
            self.acceleration = acceleration
        if vector:
            self.vector = vector
        if size:
            self.size = size
        if color:
            self.color = color
        if force:
            self.force = force
        if torque:
            self.torque = torque
        if angular_velocity:
            self.angular_velocity = angular_velocity
        if angular_acceleration:
            self.angular_acceleration = angular_acceleration
        if angular_vector:
            self.angular_vector = angular_vector
        if moment_of_inertia:
            self.moment_of_inertia = moment_of_inertia
        if center_of_mass:
            self.center_of_mass = center_of_mass
        if orientation:
            self.orientation = orientation
        if angular_momentum:
            self.angular_momentum = angular_momentum
        if angular_impulse:
            self.angular_impulse = angular_impulse
        if orientation_matrix:
            self.orientation_matrix = orientation_matrix
        if orientation_matrix_inverse:
            self.orientation_matrix_inverse = orientation_matrix_inverse
    
    # MARK: - Update
    # Update the object using the necessary variables to calculate the other variables of the object
    def update(self, forces, time):
        # calculate acceleration using time and velocity
        pass
    
    
    
    
    
    # MARK: - Velocity
    # Calculate new velocity using acceleration and time
    def calculate_velocity_from_acceleration(self, acceleration:list=[0,0,0], time:float=1):
        self.velocity[0] += acceleration[0]*time
        self.velocity[1] += acceleration[1]*time
        self.velocity[2] += acceleration[2]*time
    
    
    
    
    
    # MARK: - Acceleration
    # Calculate new acceleration using force
    def calculate_acceleration_from_forces(self, forces:list=[[0,0,0]]):
        for force in forces:
            self.acceleration[0] += force[0]/self.mass
            self.acceleration[1] += force[1]/self.mass
            self.acceleration[2] += force[2]/self.mass
    
    
    
    
    # MARK: - Position
    # Calculate new position using velocity and time
    def calculate_position_from_velocity(self, velocity:list=[0,0,0], time:float=1):
        self.position[0] += velocity[0]*time
        self.position[1] += velocity[1]*time
        self.position[2] += velocity[2]*time
    
    
    
    
    
    # MARK: - Velocity from Forces
    # Calculate new velocity using forces and time
    def calculate_velocity(self, forces:list=[[0,0,0]], time:float=1):
        # calculate acceleration
        self.calculate_acceleration_from_forces(forces)
        # calculate velocity
        self.calculate_velocity_from_acceleration(self.acceleration, time)
    
    
    
    
    
    # MARK: - Cycle
    # Cycle the object using the necessary variables to calculate the other variables of the object
    def cycle(self, forces, time):
        # calculate new velocity
        self.calculate_velocity(forces, time)
        # calculate new position
        self.calculate_position_from_velocity(self.velocity, time)
        # calculate new acceleration
        self.calculate_acceleration_from_forces(forces)
    
    
    
    
    # MARK: - Save
    # Save the object to a file
    def save(self, file:str):
        # save the object to a file
        with open(file, "w") as file:
            json.dump(self.__dict__, file)



# MARK: - Test
# test the object class
def test():
    # create an object
    object = Object("ball", 1, [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 1, force=0)
    # test the object
    assert object.name == "ball"
    assert object.mass == 1
    assert object.position == [0, 0, 0]
    assert object.velocity == [0, 0, 0]
    assert object.acceleration == [0, 0, 0]
    assert object.vector == [0, 0, 0]
    assert object.size == 1
    assert object.color == None
    assert object.force == 0
    
    # force acting on the object
    forces = [[1, 0, 1], [0, -1, 0], [1, 1, 1]]
    # time
    time = 1
    # calculate new velocity
    print("object.velocity: ", object.velocity)
    print("forces: ", forces)
    print("time: ", time)
    print("--------------------")
    object.calculate_velocity(forces, time)
    print("object.velocity: ", object.velocity)
    
    # test save
    object.save("object.json")

# test the object class
test()