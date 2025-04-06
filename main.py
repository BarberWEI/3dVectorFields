from vpython import  vector, scene, rate
from CustomSphere import CustomSphere
import math

scene.title = "Custom Spheres with mass-Dependent Color"
scene.width = 1200
scene.height = 1200

num_spheres = 2
circle_radius = 5
custom_spheres = []
spheres_mass = [5.972e24 * 1.0, 7.348e22 * 1.0]
spheres_pos = [vector(0, 0, 0), vector(384400000, 0, 0)]
spheres_radius = [6.371e6, 1.7374e6]
spheres_velocity = [vector(0, 0, 0), vector(0, 1.022e3, 0)]
# Create spheres arranged in a circle
for i in range(num_spheres):

    pos = spheres_pos[i]
    cs = CustomSphere(pos, spheres_radius[i], spheres_mass[i], spheres_velocity[i])
    custom_spheres.append(cs)
    print(f"Sphere {i}: mass = {cs.mass:.2f}, color = {cs.color}")


def gravitational_force_components(m1, m2, pos1, pos2):
    G = 6.67430e-11  
    
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    dz = pos2.z - pos1.z
    
    r = math.sqrt(dx**2 + dy**2 + dz**2)
    
    force_factor = G * m1 * m2 / r**3
    
    Fx = force_factor * dx
    Fy = force_factor * dy
    Fz = force_factor * dz

    return vector (Fx, Fy, Fz)

def calculate_acceleration(f, m):
    acceleration = vector(0, 0, 0)
    acceleration.x = f.x / m
    acceleration.y = f.y / m
    acceleration.z = f.z / m
    return acceleration

while True:
    dt = 600
    rate(dt)  # 60 frames per second
    for i in range(len(custom_spheres)):
        pos1 = custom_spheres[i].get_position()
        for j in range(i + 1, len(custom_spheres)):
            pos2 = custom_spheres[j].get_position()
            force = gravitational_force_components(custom_spheres[i].mass, custom_spheres[j].mass, pos1, pos2)
            acceleration1 = calculate_acceleration(force, custom_spheres[i].mass)
            acceleration2 = calculate_acceleration(force, custom_spheres[j].mass)
            custom_spheres[i].change_velocity(acceleration1.x * dt, acceleration1.y * dt, acceleration1.z * dt)
            custom_spheres[j].change_velocity(-acceleration2.x * dt, -acceleration2.y * dt, -acceleration2.z * dt)

        custom_spheres[i].update_position(dt)
        