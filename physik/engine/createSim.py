import sys
import os
import numpy as np
import json

#MARK: - Simulation class
class Simulation():
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
    
    def setDimensions(self, dimensions):
        self.dimensions = dimensions
    
    def setSize(self, size):
        self.size = size
    
    def setTMax(self, t_max):
        # set the maximum timesteps the simulation will run
        self.t_max = t_max
    
    def setDt(self, dt):
        # set the timestep length for the simulation
        self.dt = dt
    
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
    
    def createGeneralForce(self, force):
        # create a general force that applies to all objects in the simulation
        self.generalForces.append(force)
    
    def createConstraint(self, constraint):
        # create a constraint that applies to all objects in the simulation
        self.constraints.append(constraint)
    
    def createSimSpace(self):
        # create the simulation space as a np.array
        # the simulation space is a grid with the size of the simulation space in each dimension of the simulation
        # the simulation space is used to calculate the forces acting on the objects in the simulation
        self.simSpace = np.zeros(tuple([self.size]*self.dimensions))
        
        # add the objects to the simulation space at their positions 
        for id, obj in self.objects.items():
            position = obj['position']
            self.simSpace[tuple(position)] = id
    
    def calculateForces(self):
        # calculate the forces acting on the objects in the simulation
        # the forces are calculated based on the properties of the objects and the constraints in the simulation
        # the forces are saved in the objects in the simulation
        
        # reset the forces of the objects
        for id, obj in self.objects.items():
            obj['forces'] = []
        
        # calculate the forces acting on a pair of objects
        
    def calculateForce(self, obj1, obj2):
        # calculate the force acting on object 1 by object 2
        # the force is calculated based on the properties of the objects and the constraints in the simulation
        # the force is saved in the object 1 and object 2 in the simulation
        
        obj1 = self.objects[obj1]
        obj2 = self.objects[obj2]
        
        # calculate the direction of the force
        obj1_position = np.array(obj1['position'])
        obj2_position = np.array(obj2['position'])
        direction = obj2_position - obj1_position
        
        # calculate the magnitude of the force
        force = self.gravCon * obj1['mass'] * obj2['mass'] / np.linalg.norm(direction)**2
        
        # save the force in the object 1 and object 2
        obj1['forces'].append((obj2['id'], direction, force))
        obj2['forces'].append((obj1['id'], -direction, force))
        
        
