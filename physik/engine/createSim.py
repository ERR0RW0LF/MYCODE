import sys
import os
import numpy as np
import json
import matplotlib.pyplot as plt
import pickle

#MARK: - Simulation class
class Simulation():
    # MARK: - Simulation properties
    def __init__(self):
        self.objects = {} # dictionary of objects with their properties (mass, position, velocity, constraints, etc.) in the simulation
        self.generalForces = [] # forces that apply to all objects
        self.constraints = [] # constraints that apply to all objects
        self.dt = 0.01 # timestep length
        self.t = 0 # current timestep
        self.t_max = 100 # maximum timesteps the simulation will run
        self.dimensions = 0 # number of dimensions the simulation is in (2D or 3D) maybe 1D or 4D in the future
        self.size = 0 # size of the simulation space in each dimension (e.g. 3D: 10m x 10m x 10m, size = 10, dimensions = 3, 2D: 10m x 10m, size = 10, dimensions = 2)
        self.simSpace = None # the simulation space as a np.array (e.g. 3D: 10m x 10m x 10m, size = 10, dimensions = 3, 2D: 10m x 10m, size = 10, dimensions = 2)
        self.gravCon = 6.67430e-11 # gravitational constant in m^3 kg^-1 s^-2
    
    # MARK: - Simulation properties setters
    def setDimensions(self, dimensions):
        self.dimensions = int(dimensions)
    
    def setSize(self, size):
        self.size = int(size)
    
    def setTMax(self, t_max):
        # set the maximum timesteps the simulation will run
        self.t_max = int(t_max)
    
    def setDt(self, dt):
        # set the timestep length for the simulation
        self.dt = float(dt)
    
    # MARK: - Object creation
    def createObject(self, name, mass:float, position:list, velocity:list):        
        # create an object with a random id and the given properties
        while True:
            id = np.random.randint(0, 100000)
            if id not in self.objects:
                break
        
        if len(position) != self.dimensions:
            print('The position of the object does not match the number of dimensions of the simulation')
            return None
        if len(velocity) != self.dimensions:
            print('The velocity of the object does not match the number of dimensions of the simulation')
            return None
        
        
        self.objects[id] = {
            'name': name, # name of the object (e.g. ball, box, etc.) only for display purposes and search purposes
            'objectType': 'particle', # the type of object (e.g. particle, rigid body, etc.) is for search purposes only
            'mass': mass, # mass of the object in kg (kilograms) is needed for the simulation to calculate the forces acting on the object and the acceleration of the object
            'position': position, # position of the object in the simulation space (e.g. 3D: [x, y, z], 2D: [x, y]) is needed for the simulation to calculate the forces acting on the object and the acceleration of the object
            'velocity': velocity, # velocity of the object in the simulation space (e.g. 3D: [vx, vy, vz], 2D: [vx, vy]) is needed for the simulation to calculate the forces acting on the object and the acceleration of the object
            'forces': [], # forces are saved in a list with their properties (id of the interacting object, direction that the force is applied in, the force itself in N)
            'constraints': [], # constraints are saved in a list with their properties (id of the interacting object, type of constraint, additional properties of the constraint)
            'properties': {} # additional properties that can be added to the object (e.g. color, shape, etc.)
        }
        
        return id
    
    # MARK: - Force and constraint creation
    def createGeneralForce(self, force):
        # create a general force that applies to all objects in the simulation
        self.generalForces.append(force)
    
    def createConstraint(self, constraint):
        # create a constraint that applies to all objects in the simulation
        self.constraints.append(constraint)
    
    # MARK: - Simulation space creation
    def createSimSpace(self):
        # create the simulation space as a np.array
        # the simulation space is a grid with the size of the simulation space in each dimension of the simulation
        # the simulation space is used to calculate the forces acting on the objects in the simulation
        self.simSpace = np.zeros(tuple([self.size]*self.dimensions))
        
        # add the objects to the simulation space at their positions 
        for id, obj in self.objects.items():
            position = obj['position']
            self.simSpace[tuple([int(i) for i in position])] = id
    
    # MARK: - Force and acceleration calculation
    # MARK: - Force calculation
    def calculateForce(self, id1, id2):
        # calculate the force acting on object 1 by object 2
        # the force is calculated based on the properties of the objects and the constraints in the simulation
        # the force is saved in the object 1 and object 2 in the simulation
        
        obj1 = self.objects[id1]
        obj2 = self.objects[id2]
        
        # calculate the direction of the force
        obj1_position = np.array(obj1['position'])
        obj2_position = np.array(obj2['position'])
        direction = obj2_position - obj1_position
        
        # calculate the magnitude of the force
        force = self.gravCon * obj1['mass'] * obj2['mass'] / np.linalg.norm(direction)**2

        # save the force in the object 1 and object 2
        obj1['forces'].append((id2, direction, float(force)))
        #obj2['forces'].append((id1, -direction, force))
    
    def calculateForces(self):
        # calculate the forces acting on the objects in the simulation
        # the forces are calculated based on the properties of the objects and the constraints in the simulation
        # the forces are saved in the objects in the simulation
        
        # calculate the forces between all objects in the simulation
        for id1, obj1 in self.objects.items():
            for id2, obj2 in self.objects.items():
                if id1 != id2:
                    self.calculateForce(id1, id2)
        
    
    # MARK: - Acceleration calculation
    def calculateAcceleration(self, id):
        # calculate the acceleration of the object based on the forces acting on the object
        # the acceleration is calculated based on the properties of the object and the forces acting on the object
        # the acceleration is saved in the object in the simulation
        
        obj = self.objects[id]
        
        # calculate the net force acting on the object
        net_force = np.zeros(self.dimensions)
        for force in obj['forces']:
            net_force += force[2] * force[1] / np.linalg.norm(force[1])
        
        # calculate the acceleration of the object
        acceleration = net_force / obj['mass']
        
        return acceleration
    
    # MARK: - Position update
    def updatePosition(self, id):
        # update the position of the object based on the velocity and acceleration of the object
        # the position is updated based on the properties of the object and the forces acting on the object
        # the position is saved in the object in the simulation
        
        obj = self.objects[id]
        
        # calculate the acceleration of the object
        acceleration = self.calculateAcceleration(id)
        
        # update the velocity of the object
        obj['velocity'] += acceleration * self.dt
        
        # update the position of the object
        obj['position'] += obj['velocity'] * self.dt
    
    # MARK: - Space update
    def updateSpace(self):
        # update the simulation space with the new positions of the objects
        # the simulation space is a grid with the size of the simulation space in each dimension of the simulation
        # the simulation space is used to calculate the forces acting on the objects in the simulation
        
        # clear the simulation space
        self.simSpace = np.zeros(tuple([self.size]*self.dimensions))
        
        # add the objects to the simulation space at their new positions
        for id, obj in self.objects.items():
            position = obj['position']
            print('Position:', position)
            print([int(i) for i in position])
            self.simSpace[tuple([int(i) for i in position])] = id
    
    # MARK: - Simulation cycle
    def timestep(self):
        # run one timestep of the simulation
        # the simulation calculates the forces acting on the objects, updates the positions of the objects, and updates the simulation space
        
        # calculate the forces acting on the objects
        self.calculateForces()
        
        # update the positions of the objects
        for id in self.objects:
            self.updatePosition(id)
        
        # update the simulation space
        self.updateSpace()
        #self.display()
        
        # increment the timestep
        self.t += 1
    
    # MARK: - Simulation run
    def run(self):
        # run the simulation for the specified number of timesteps
        while self.t < self.t_max:
            self.timestep()
            print('Timestep:', self.t)
            print('Space:','\n', self.simSpace)
    
    # MARK: - Save and load simulation
    # MARK: - Save simulation
    def createSaveData(self):
        # create a dictionary with the properties of the simulation to save to a json file
        data = {
            'objects': self.objects,
            'generalForces': self.generalForces,
            'constraints': self.constraints,
            'dt': self.dt,
            't': self.t,
            't_max': self.t_max,
            'dimensions': self.dimensions,
            'size': self.size
        }
        
        return data
    
    def save(self, path):
        # save the simulation to a json file
        
        with open(path, 'w') as f:
            pickle.dump(self.createSaveData(), f)
    
    # MARK: - Load simulation
    def load(self, path):
        # load the simulation from a json file
        
        with open(path, 'r') as f:
            data = pickle.load(f)
        
        
        self.dimensions = data['dimensions']
        self.size = data['size']
        self.dt = data['dt']
        self.t = data['t']
        self.t_max = data['t_max']
        self.objects = data['objects']
        self.generalForces = data['generalForces']
        self.constraints = data['constraints']
        
        self.createSimSpace()
    
    # MARK: - Display simulation
    def display(self):
        # display the simulation space with the objects in the simulation
        
        # create a grid to display the simulation space
        grid = np.zeros(tuple([self.size]*self.dimensions))
        
        # add the objects to the grid at their positions
        for id, obj in self.objects.items():
            position = obj['position']
            grid[[int(i) for i in position]] = 1
        
        # display the grid
        plt.imshow(grid)
        plt.show()
    

# MARK: - Main function
def main():
    # create a simulation
    sim = Simulation()
    
    # set the dimensions of the simulation
    sim.setDimensions(2)
    
    # set the size of the simulation space
    sim.setSize(10)
    
    # create objects in the simulation
    sim.createObject('object1', 1, [5, 5], [0, 0])
    sim.createObject('object2', 1, [3, 3], [0, 0])
    
    # create a general force in the simulation
    sim.createGeneralForce('gravity')
    
    # create a constraint in the simulation
    sim.createConstraint('collision')
    
    # create the simulation space
    sim.createSimSpace()
    
    # run the simulation
    sim.run()
    
    # save the simulation
    sim.save('simulation.sim')
    
    # load the simulation
    sim.load('simulation.sim')
    
    # run the simulation
    sim.run()

# MARK: - Run main function
if __name__ == '__main__':
    main()