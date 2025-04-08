import numpy
from vpython import scene, mag, vector
scene.visible = False
import math

class Environment:
    def __init__(self):
        self.to = 0
    
    def sphere_collision(s1, s2):
        distance = mag(s1.pos - s2.pos)

        # Check for collision (if distance is less than the sum of the radii)
        if distance < (s1.radius + s2.radius):
            return True
        return False



    # returns true if object1 is in orbit of object2
    def is_in_orbit(obj1, obj2, G=6.67430e-11):
        r_vec = obj1.get_position() - obj2.get_position()
        r = mag(r_vec)
        v_rel = obj1.get_velocity() - obj2.get_velocity()
        energy = 0.5 * mag(v_rel)**2 - G * obj2.mass / r
        return energy < 0
        
    
    def one_step(self, custom_objects):
        dt = 60
        for i in range(len(custom_objects)):
            pos1 = custom_objects[i].get_position()
            for j in range(i + 1, len(custom_objects)):
                pos2 = custom_objects[j].get_position()
                force = self.gravitational_force_components(custom_objects[i].mass, custom_objects[j].mass, pos1, pos2)
                acceleration1 = self.calculate_acceleration(force, custom_objects[i].mass)
                acceleration2 = self.calculate_acceleration(force, custom_objects[j].mass)
                custom_objects[i].change_velocity(acceleration1.x, acceleration1.y, acceleration1.z, dt)
                custom_objects[j].change_velocity(-acceleration2.x, -acceleration2.y, -acceleration2.z, dt)
            custom_objects[i].rotate(0.05, dt)
            custom_objects[i].update_position(dt)

    def gravitational_force_components(self, m1, m2, pos1, pos2):
        G = 6.67430e-11
        dx = pos2.x - pos1.x
        dy = pos2.y - pos1.y
        dz = pos2.z - pos1.z
        r = math.sqrt(dx**2 + dy**2 + dz**2)
        force_factor = G * m1 * m2 / r**3
        return vector(force_factor * dx, force_factor * dy, force_factor * dz)

    def calculate_acceleration(self, f, m):
        return vector(f.x/m, f.y/m, f.z/m)