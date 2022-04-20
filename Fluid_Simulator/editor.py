import sys
from unittest.util import sorted_list_difference
from fluid import Fluid
from enum import Enum
import numpy as np

class velAnim(Enum):
    STATIC = 1
    ROTATE_RIGHT = 2
    ROTATE_LEFT = 3
    MOVE_X = 4
    MOVE_Y = 5

    def __int__(self):
        return self.value

class Velocity:
    def __init__(self, pos_x: int, pos_y: int, strength_x: int, strength_y: int, animation=velAnim.STATIC, animation_value=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.strength_x = strength_x
        self.strength_y = strength_y
        self.__dir_x = self.strength_x
        self.__dir_y = self.strength_y

        if animation not in [velAnim.ROTATE_RIGHT, velAnim.ROTATE_LEFT, velAnim.MOVE_X, velAnim.MOVE_Y]: animation = velAnim.STATIC
        self.__animation = animation

        self.__rotation = 0
        self.__current_rot = 0

        self.__length = 0
        self.__current_length = 0
        self.__step = 1

        if self.__animation in [velAnim.ROTATE_RIGHT, velAnim.ROTATE_LEFT]: self.__rotation = animation_value
        elif self.__animation in [velAnim.MOVE_X, velAnim.MOVE_Y]: self.__length = animation_value

    def __str__(self):
        string = f"{self.pos_x}, {self.pos_y}, {self.strength_x}, {self.strength_y}, {int(self.__animation)}"
        if self.__animation in [velAnim.ROTATE_RIGHT, velAnim.ROTATE_LEFT]: string += f", {self.__rotation}"
        elif self.__animation in [velAnim.MOVE_X, velAnim.MOVE_Y]: string += f", {self.__length}"
        return string

    def __rotate(self):
        if self.__animation == velAnim.ROTATE_RIGHT: self.__current_rot += np.deg2rad(self.__rotation)
        elif self.__animation == velAnim.ROTATE_LEFT: self.__current_rot -= np.deg2rad(self.__rotation)

        self.__dir_x = self.strength_x * np.cos(self.__current_rot)
        self.__dir_y = self.strength_y * np.sin(self.__current_rot)

    def __return(self):
        if abs(self.__current_length) >= self.__length: self.__step *= -1
        self.__current_length += self.__step

        if self.__animation == velAnim.MOVE_X: self.pos_x += self.__current_length
        elif self.__animation == velAnim.MOVE_Y: self.pos_y += self.__current_length

    def get_dir(self):
        return [self.__dir_y, self.__dir_x]

    def step(self):
        if self.__animation in [velAnim.ROTATE_RIGHT, velAnim.ROTATE_LEFT]: self.__rotate()
        elif self.__animation in [velAnim.MOVE_X, velAnim.MOVE_Y]: self.__return()
        

class Density:
    
    def __init__(self, pos_x: int, pos_y: int, size_x: int, size_y: int, density=100):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.density = density

    def __str__(self):
        return f"{self.pos_x}, {self.pos_y}, {self.size_x}, {self.size_y}, {self.density}"       


class Solid:
    def __init__(self, pos_x: int, pos_y: int, size_x: int, size_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def __str__(self):
        return f"{self.pos_x}, {self.pos_y}, {self.size_x}, {self.size_y}"
    
    
def read_input(filename=""):
    filename="Data1"
    file = open(filename + ".txt", "r")
    
    lines = file.read().split("\n")
    den_array = []
    vel_array = []
    sol_array = []
    colormap = ""
    current = ""
    length = 0
    for line in lines:
        if "color" in line:
            colormap = line.split("=")[1]
        elif "D" in line:
            length = int(line.split("=")[1])
            current = "D"
        elif "V" in line:
            length = int(line.split("=")[1])
            current = "V"
        elif "S" in line:
            length = int(line.split("=")[1])
            current = "S"
        elif length > 0:
            length -= 1
            if current == "D": den_array.append(line)
            elif current == "V": vel_array.append(line)
            elif current == "S": sol_array.append(line)
    file.close()


   
    solids = []
    for sol in sol_array:
        info = sol.split(", ")
        pos_x = int(info[0])
        pos_y = int(info[1])
        size_x = int(info[2])
        size_y = int(info[3])
        temp_sol = Solid(pos_x, pos_y, size_x, size_y)
        solids.append(temp_sol)
        

    velocities = []
    for vel in vel_array:
        info = vel.split(", ")
        animation_value = 0

        pos_x = int(info[0])
        pos_y = int(info[1])
        strength_x = int(info[2])
        strength_y = int(info[3])
        animation = velAnim(int(info[4]))
        if animation in [velAnim.ROTATE_RIGHT, velAnim.ROTATE_LEFT, velAnim.MOVE_X, velAnim.MOVE_Y]:
            animation_value = int(info[5])

        temp_vel = Velocity(pos_x, pos_y, strength_x, strength_y, animation, animation_value)
        velocities.append(temp_vel)
    
    
    densities = []
    for den in den_array:
        info = den.split(", ")
        pos_x = int(info[0])
        pos_y = int(info[1])
        size_x = int(info[2])
        size_y = int(info[3])
        density = int(info[4])
        temp_den = Density(pos_x, pos_y, size_x, size_y, density)
        densities.append(temp_den)


    return colormap, densities, velocities, solids



def create_from_input(fluid: Fluid, filename=""):
    cmap, densities, velocities, solids = read_input(filename)
    colormap = choose_color(cmap)

    fluid.solid = solids
    maintain_step(fluid, densities, velocities)

    return colormap, densities, velocities

def choose_color(color_name=""):
    return color_name

def add_velocity(fluid: Fluid, velocity: Velocity):
    fluid.velo[velocity.pos_y, velocity.pos_x] = velocity.get_dir()
    
def add_density(fluid: Fluid, density: Density):
    fluid.density[density.pos_y:density.pos_y + density.size_y, density.pos_x:density.pos_x + density.size_x] = density.density
    
def maintain_step(fluid: Fluid, densities: list, velocities: list):
    for den in densities:
        add_density(fluid, den)
    
    for vel in velocities:
        add_velocity(fluid, vel)
        vel.step()