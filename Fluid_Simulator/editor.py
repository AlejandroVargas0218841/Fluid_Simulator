import numpy as np
class Vel:
    def __init__(self, positionx, positiony, forceX, forceY, animation="STATIC", animation_value=0):
        self.positionx = positionx
        self.positiony = positiony
        self.forceX = forceX
        self.forceY = forceY
        self.directionX = self.forceX
        self.directionY = self.forceY

        if animation not in ["ROTATE_RIGHT", "ROTATE_LEFT", "MOVE_X", "MOVE_Y"]: animation = "STATIC"
        self.animation = animation

        self.rotation = 0
        self.current_rot = 0

        self.length = 0
        self.current_length = 0
        self.current_step = 1

        if self.animation in ["ROTATE_RIGHT", "ROTATE_LEFT"]: self.rotation = animation_value
        elif self.animation in ["MOVE_X", "MOVE_Y"]: self.length = animation_value

    def anim_rotate(self):
        if self.animation == "ROTATE_RIGHT": self.current_rot += np.deg2rad(self.rotation)
        elif self.animation == "ROTATE_LEFT": self.current_rot -= np.deg2rad(self.rotation)

        self.directionX = self.forceX * np.cos(self.current_rot)
        self.directionY = self.forceY * np.sin(self.current_rot)

    def anim_return(self):
        if abs(self.current_length) >= self.length: self.current_step *= -1
        self.current_length += self.current_step

        if self.animation == "MOVE_X": self.positionx += self.current_length
        elif self.animation == "MOVE_Y": self.positiony += self.current_length

    def get_direction(self):
        return [self.directionY, self.directionX]

    def step(self):
        if self.animation in ["ROTATE_RIGHT", "ROTATE_LEFT"]: self.anim_rotate()
        elif self.animation in ["MOVE_X", "MOVE_Y"]: self.anim_return()
        

class Den:
    def __init__(self, positionx, positiony, sizeX, sizeY, den=100):
        self.positionx = positionx
        self.positiony = positiony
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.den = den  


class Sol:
    def __init__(self, positionx, positiony, sizeX, sizeY):
        self.positionx = positionx
        self.positiony = positiony
        self.sizeX = sizeX
        self.sizeY = sizeY
    
    
def read_input(filename=""):
    file = open(filename + ".txt", "r")
    
    lines = file.read().split("\n")
    den_array = []
    vel_array = []
    sol_array = []
    current = ""
    length = 0
    for line in lines:
        if "D" in line:
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
    
    sols = []
    for sol in sol_array:
        info = sol.split(", ")
        positionx = int(info[0])
        positiony = int(info[1])
        sizeX = int(info[2])
        sizeY = int(info[3])
        temp_sol = Sol(positionx, positiony, sizeX, sizeY)
        sols.append(temp_sol)
        
    vels = []
    for vel in vel_array:
        info = vel.split(", ")
        animation_value = 0

        positionx = int(info[0])
        positiony = int(info[1])
        forceX = int(info[2])
        forceY = int(info[3])
        animation = info[4]
        if animation in ["ROTATE_RIGHT", "ROTATE_LEFT", "MOVE_X", "MOVE_Y"]:
            animation_value = int(info[5])

        temp_vel = Vel(positionx, positiony, forceX, forceY, animation, animation_value)
        vels.append(temp_vel)
    
    dens = []
    for den in den_array:
        info = den.split(", ")
        positionx = int(info[0])
        positiony = int(info[1])
        sizeX = int(info[2])
        sizeY = int(info[3])
        density = int(info[4])
        temp_den = Den(positionx, positiony, sizeX, sizeY, density)
        dens.append(temp_den)
        
    return dens, vels, sols

def fill_fluid(fluid, filename=""):
    dens, vels, sols = read_input(filename)
    colors = ["inferno", "magma", "plasma"]
    print("1. Black to Yellow")
    print("2. Black to pink")
    print("3. Blue to Yellow")
    while True:
        color = int(input("Choose a color (default 1): ") or 1)
        if color in [1, 2, 3]: break
    color_map = colors[color - 1]

    fluid.solid = sols
    maintain_step(fluid, dens, vels)

    return color_map, dens, vels

def add_Vel(fluid, Vel):
    fluid.velo[Vel.positiony, Vel.positionx] = Vel.get_direction()
    
def add_Den(fluid, Den):
    fluid.density[Den.positiony:Den.positiony + Den.sizeY, Den.positionx:Den.positionx + Den.sizeX] = Den.den
    
def maintain_step(fluid, densities, velocities):
    for den in densities:
        add_Den(fluid, den)
    
    for vel in velocities:
        add_Vel(fluid, vel)
        vel.step()
