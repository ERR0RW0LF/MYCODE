from objects import Object
from simulation import Simulation

# MARK: - Collisions
class Collision:
    def __init__(self) -> None:
        pass
    
    
    # MARK: - Distance
    # Calculate the distance between two objects
    def calculate_distance(self, obj1: Object, obj2: Object) -> float:
        return ((obj1.position[0]-obj2.position[0])**2 + (obj1.position[1]-obj2.position[1])**2 + (obj1.position[2]-obj2.position[2])**2)**0.5 + obj1.size + obj2.size
    
    
    # MARK: - Check for collision
    # check if two objects collide
    def check_colliding(self, obj1: Object, obj2: Object) -> bool:
        d = self.calculate_distance(obj1, obj2)
        if d <= 0:
            return True
    
    # MARK: - Collision
    # Calculate the collision between two objects
    
    # MARK: - Elastic Collision
    # Calculate the elastic collision between two objects
    def calculate_elastic_collision(self, obj1: Object, obj2: Object) -> list:
        # calculate the normal vector
        normal = [obj1.position[0]-obj2.position[0], obj1.position[1]-obj2.position[1], obj1.position[2]-obj2.position[2]]
        # calculate the unit normal vector
        unit_normal = [normal[0]/((normal[0]**2+normal[1]**2+normal[2]**2)**0.5), normal[1]/((normal[0]**2+normal[1]**2+normal[2]**2)**0.5), normal[2]/((normal[0]**2+normal[1]**2+normal[2]**2)**0.5)]
        # calculate the unit tangent vector
        unit_tangent = [unit_normal[1], -unit_normal[0], 0]
        # calculate the initial velocity in the normal direction
        v1n = obj1.velocity[0]*unit_normal[0] + obj1.velocity[1]*unit_normal[1] + obj1.velocity[2]*unit_normal[2]
        v2n = obj2.velocity[0]*unit_normal[0] + obj2.velocity[1]*unit_normal[1] + obj2.velocity[2]*unit_normal[2]
        # calculate the initial velocity in the tangent direction
        v1t = obj1.velocity[0]*unit_tangent[0] + obj1.velocity[1]*unit_tangent[1] + obj1.velocity[2]*unit_tangent[2]
        v2t = obj2.velocity[0]*unit_tangent[0] + obj2.velocity[1]*unit_tangent[1] + obj2.velocity[2]*unit_tangent[2]
        # calculate the final velocity in the normal direction
        v1n_f = (v1n*(obj1.mass-obj2.mass)+2*obj2.mass*v2n)/(obj1.mass+obj2.mass)
        v2n_f = (v2n*(obj2.mass-obj1.mass)+2*obj1.mass*v1n)/(obj1.mass+obj2.mass)
        # calculate the final velocity in the tangent direction
        v1t_f = v1t
        v2t_f = v2t
        # calculate the final velocity
        v1        

    