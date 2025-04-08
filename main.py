from vpython import vector, scene, rate, button, slider, textures, color
import random, math
from CustomSphere import CustomSphere

scene.title = "rocket launch and universe"
scene.width = 1200
scene.height = 1200

sphere_counter = 0
follow_mode = False
follow_index = 0
add_mode_active = False
num_objects = 2
custom_objects = []
objects_colors = [color.cyan, color.white]
objects_textures = [textures.earth, textures.wood]
objects_mass = [5.972e24, 7.348e22]
objects_pos = [vector(0, 0, 0), vector(384400000, 0, 0)]
objects_radius = [6.371e6, 1.7374e6]
objects_velocity = [vector(0, 0, 0), vector(0, 1.022e3, 0)]
objects_rotate = [vector(0, 1, 0), None]

for i in range(num_objects):
    cs = CustomSphere(objects_pos[i], objects_radius[i], objects_mass[i], objects_velocity[i], objects_colors[i], objects_textures[i])
    custom_objects.append(cs)

def gravitational_force_components(m1, m2, pos1, pos2):
    G = 6.67430e-11
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    dz = pos2.z - pos1.z
    r = math.sqrt(dx**2 + dy**2 + dz**2)
    force_factor = G * m1 * m2 / r**3
    return vector(force_factor * dx, force_factor * dy, force_factor * dz)

def calculate_acceleration(f, m):
    return vector(f.x/m, f.y/m, f.z/m)

def center_camera(evt=None):
    global follow_mode, follow_index, sphere_counter
    if not follow_mode:
        follow_mode = True
        follow_index = sphere_counter
    else:
        sphere_counter = (sphere_counter + 1) % len(custom_objects)
        follow_index = sphere_counter

def add_sphere(evt):
    new_pos = evt.pos
    new_mass = mass_slider.value
    new_radius = radius_slider.value  
    new_velocity = vector(0, 0, 0)
    new_cs = CustomSphere(new_pos, new_radius, new_mass, new_velocity)
    custom_objects.append(new_cs)

def toggle_add_mode():
    global add_mode_active
    if not add_mode_active:
        scene.bind("click", add_sphere)
        add_mode_active = True
    else:
        scene.unbind("click", add_sphere)
        add_mode_active = False

mass_slider = slider(min=1e20, max=1e25, value=1e24, length=300, bind=None, right=15)
radius_slider = slider(min=1e6, max=8e6, value=1e6, length=300, bind=None, right=15)
button(text="Toggle Add Mode", bind=lambda: toggle_add_mode())
button(text="Center Camera", bind=center_camera)

while True:
    dt = 60
    rate(dt)
    for i in range(len(custom_objects)):
        pos1 = custom_objects[i].get_position()
        for j in range(i + 1, len(custom_objects)):
            pos2 = custom_objects[j].get_position()
            force = gravitational_force_components(custom_objects[i].mass, custom_objects[j].mass, pos1, pos2)
            acceleration1 = calculate_acceleration(force, custom_objects[i].mass)
            acceleration2 = calculate_acceleration(force, custom_objects[j].mass)
            custom_objects[i].change_velocity(acceleration1.x, acceleration1.y, acceleration1.z, dt)
            custom_objects[j].change_velocity(-acceleration2.x, -acceleration2.y, -acceleration2.z, dt)
        custom_objects[i].rotate(0.05, dt)
        custom_objects[i].update_position(dt)
    if follow_mode:
        scene.center = custom_objects[follow_index].get_position()
