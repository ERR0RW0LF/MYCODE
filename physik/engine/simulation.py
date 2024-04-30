# Simulation class for the physics engine
class Simulation:
    def __init__(self, max_x:float, max_y:float, max_z:float, objects:list=[]):
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
        self.objects = []
        for object in objects:
            self.objects.append(object)
    
    def add_object(self, object):
        self.objects.append(object)
    
    def remove_object(self, object):
        self.objects.remove(object)
    
    def edit_object(self, object, name=None, mass=None, position=None, velocity=None, acceleration=None):
        object.edit(name, mass, position, velocity, acceleration)
    
    