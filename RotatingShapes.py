import pygame
from pygame.locals import *
import math

WIDTH = 1280
HEIGHT = 720
RESOLUTION = (1280,720)
angle = 0
window = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()




def Cube():
    return  [
                [[-1],[-1],[-1]], #P0 
                [[1],[-1],[-1]],  #P1
                [[1],[1],[-1]],  #P2
                [[-1],[1],[-1]],   #P3
                [[-1],[-1],[1]],  #P4   # Geogebra link https://www.geogebra.org/3d/kmyj3azc 
                [[1],[-1],[1]],   #P5
                [[1],[1],[1]],   #P6
                [[-1],[1],[1]]     #P7
            ]

def Pyramid():
    return  [  
                [[0],[0],[2]],    #P0
                [[1],[1],[0]],    #P1
                [[1],[-1],[0]],   #P2       # Geogebra link https://www.geogebra.org/3d/ca5fsvqn
                [[-1],[-1],[0]],   #P3
                [[-1],[1],[0]]   #P4
            ]



def projection_matrix():
    return          [
                        [1,0,0],
                        [0,1,0],
                        [0,0,0]
                    ]


def rX_matrix():
    return              [
                        [1,0,0],
                        [0,math.cos(angle), -math.sin(angle)],
                        [0,math.sin(angle), math.cos(angle)]
                        ]

def rY_matrix():
    return              [
                        [math.cos(angle),0,math.sin(angle)],
                        [0,1,0],
                        [-math.sin(angle),0,math.cos(angle)]    
                        ]

def rZ_matrix():
    return              [
                        [math.cos(angle),-math.sin(angle),0],
                        [math.sin(angle), math.cos(angle),0],
                        [0,0,1]
                        ]
    


def connectPoints(i, j, points):
    pygame.draw.line(window, (255,255,255), (points[i][0], points[i][1]), (points[j][0], points[j][1]))


def matrix_multiplication(a,b):
    
    a_columns = len(a[0])
    a_rows = len(a)
    
    b_columns = len(b[0])
    b_rows = len(b)

    if a_columns == b_rows:
        result_matrix = []
        for i in range(a_rows):
            result_matrix.append([])  
            for k in range(b_columns):
                result = 0    
                for j in range(a_columns):
                    result+= a[i][j] * b[j][k]
                result_matrix[i].append(result)
        return result_matrix
    else:
        print("No se pueden multiplicar :(")


scale = 100
#Main Loop
while True:
    clock.tick(60)
    window.fill((0,0,0))
    angle += 0.01
    
    #Projection Matrix
    p_matrix = projection_matrix()

    #Rotation Matrixes
    rotationX_matrix = rX_matrix()
    rotationY_matrix = rY_matrix()
    rotationZ_matrix = rZ_matrix()
    
    #3D Shape
    #shape_points = Cube()  #Cube
    shape_points = Pyramid() #Pyramid
    

    points = [0 for _ in range(len(shape_points))]
    i = 0

    for point in shape_points:
        rotate_x = matrix_multiplication(rotationX_matrix, point)    #It doesn't matter in what order, but you've to multiply all
        rotate_y = matrix_multiplication(rotationY_matrix, rotate_x)
        rotate_z = matrix_multiplication(rotationZ_matrix, rotate_y)
        
        point2D = matrix_multiplication(p_matrix, rotate_z)

        x = (point2D[0][0] * scale) + WIDTH/2
        y = (point2D[1][0] * scale) + HEIGHT/2

        points[i] = (x,y)
        i += 1

        pygame.draw.circle(window, (50, 205, 50), (x, y), 5)

    # Connecting points with lines (CUBE)
    """
    for i in range(4):
        connectPoints(i, (i+1)%4, points)
        connectPoints(i+4, ((i+1)%4)+4, points)
        connectPoints(i, i+4, points)
    """
    # Connecting points with lines (Pyramid)
    for i in range(4):
        connectPoints(i+1,0, points)
        connectPoints(i+1,(i+2)%5, points)

        if(i == 3):
            connectPoints(4,1,points)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()