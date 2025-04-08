from vpython import sphere, vector, textures
import random
from math import cos, sin, pi

class CustomSphere:
    def __init__(self, pos, radius=0.5, mass=None, velocity=vector(0, 0, 0), sphere_color=vector(255, 255, 255), sphere_texture=None, axis = None):
        self.velocity = velocity
        self.pos = pos
        self.radius = radius
        self.mass = mass if mass is not None else random.uniform(1, 10)
        self.axis = axis
        self.sphere_obj = sphere(pos=self.pos, radius=self.radius, color=sphere_color, texture=sphere_texture)
    
    def update_position(self, dt = 1):
        self.pos.x = self.pos.x + self.velocity.x * dt
        self.pos.y = self.pos.y + self.velocity.y * dt
        self.pos.z = self.pos.z + self.velocity.z * dt
        self.sphere_obj.pos = self.pos
        
    def rotate(self, angle, dt = 1):
        if not self.axis is None:
            self.sphere_obj.rotate(angle=angle * dt, axis=self.axis, origin=self.sphere_obj.pos)

    def get_position(self):
        
        return self.pos
    
    def get_velocity(self):
        
        return self.velocity
    
    def change_velocity(self, x, y, z, dt):
        self.velocity.x = self.velocity.x + x * dt
        self.velocity.y = self.velocity.y + y * dt
        self.velocity.z = self.velocity.z + z * dt