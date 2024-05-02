import json
import pprint
import random
from objects import Object

# Simulation class for the physics engine
class Simulation:
    def __init__(self, max_x:float, max_y:float, max_z:float, objects:list=[]):
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        self.objects = {}
        for obj in objects:
            while obj.id in self.objects:
                obj.id += 1
            self.objects[obj.id] = obj
    
    def add_object(self, obj:Object):
        while obj.id in self.objects:
            obj.id += 1
        self.objects[obj.id] = obj
    
    def remove_object(self, objId:int):
        self.objects.pop(objId)
    
    def edit_object(self, objId:int, name=None, mass=None, position=None, velocity=None, acceleration=None, vector=None, size=None, color=None, force=None, torque=None, angular_velocity=None, angular_acceleration=None, angular_vector=None, moment_of_inertia=None, center_of_mass=None, orientation=None, angular_momentum=None, angular_impulse=None, orientation_matrix=None, orientation_matrix_inverse=None):
        self.objects[objId].edit(name, mass, position, velocity, acceleration, vector, size, color, force, torque, angular_velocity, angular_acceleration, angular_vector, moment_of_inertia, center_of_mass, orientation, angular_momentum, angular_impulse, orientation_matrix, orientation_matrix_inverse)

    def update(self, time:float):
        for obj in self.objects.values():
            obj.update(time)

    def random_object(self):
        return Object(mass=random.randrange(1, 100), position=[random.random()*self.max_x, random.random()*self.max_y, random.random()*self.max_z], velocity=[random.random()*10, random.random()*10, random.random()*10], acceleration=[random.random()*10, random.random()*10, random.random()*10], vector=[random.random()*10, random.random()*10, random.random()*10], size=[random.random()*10, random.random()*10, random.random()*10], color=[random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)], force=[random.random()*10, random.random()*10, random.random()*10], torque=[random.random()*10, random.random()*10, random.random()*10], angular_velocity=[random.random()*10, random.random()*10, random.random()*10], angular_acceleration=[random.random()*10, random.random()*10, random.random()*10], angular_vector=[random.random()*10, random.random()*10, random.random()*10], moment_of_inertia=random.random()*10, center_of_mass=[random.random()*10, random.random()*10, random.random()*10], orientation=[random.random()*10, random.random()*10, random.random()*10], angular_momentum=[random.random()*10, random.random()*10, random.random()*10], angular_impulse=[random.random()*10, random.random()*10, random.random()*10], orientation_matrix=[[random.random()*10, random.random()*10, random.random()*10], [random.random()*10, random.random()*10, random.random()*10], [random.random()*10, random.random()*10, random.random()*10]], orientation_matrix_inverse=[[random.random()*10, random.random()*10, random.random()*10], [random.random()*10, random.random()*10, random.random()*10], [random.random()*10, random.random()*10, random.random()*10]])
    
    def get_info(self):
        info = {}
        print(self.objects.items())
        for obj in self.objects.values():
            info[obj.id] = obj.get_info()
        return info
    
    def display_info(self):
        print("\n", "-"*20, "\n", "Simulation Info:")
        pprint.pprint(self.get_info())
        print("-"*20, "\n")
    
    def get_objects(self):
        return self.objects.keys()
    
    def save(self, path:str):
        with open(path, "w") as file:
            json.dump(self.get_info(), file)


# Test the Simulation class
if __name__ == "__main__":
    simulation = Simulation(100, 100, 100)
    simulation.add_object(simulation.random_object())
    simulation.add_object(simulation.random_object())
    simulation.add_object(simulation.random_object())
    simulation.display_info()
    simulation.remove_object(1)
    simulation.display_info()
    simulation.edit_object(2, position=[0,0,0])
    simulation.display_info()
    simulation.update(1)
    simulation.display_info()
    print(simulation.get_objects())
    simulation.save("simulation.json")