from vpython import sphere, vector, color, scene, rate
import random
from math import cos, sin, pi

class CustomSphere:
    def __init__(self, pos, radius=0.5, mass=None, velocity=vector(0, 0, 0)):
        self.dt = 60
        self.velocity = velocity
        self.pos = pos
        self.radius = radius
        self.mass = mass if mass is not None else random.uniform(1, 10)
        
        self.color = vector(255, 255, 255)
        
        self.sphere_obj = sphere(pos=self.pos, radius=self.radius, color=self.color)
    
    def update_position(self, dt = 1):
        self.pos.x = self.pos.x + self.velocity.x * dt
        self.pos.y = self.pos.y + self.velocity.y * dt
        self.pos.z = self.pos.z + self.velocity.z * dt
        self.sphere_obj.pos = self.pos
        
    def get_position(self):
        
        return self.pos
    
    def get_velocity(self):
        
        return self.velocity
    
    def change_velocity(self, x, y, z):
        self.velocity.x = self.velocity.x + x 
        self.velocity.y = self.velocity.y + y 
        self.velocity.z = self.velocity.z + z 