import numpy as np
import pygame
from math import *

class Rotation:
    def __init__(self, angle, axis) -> None:
        self.angle = angle
        self.axis = axis

def identity_matrix():
    return np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [0,0,0,1]], np.float32)

def translate_matrix(x, y, z):
    return np.array([[1,0,0,x],
                     [0,1,0,y],
                     [0,0,1,z],
                     [0,0,0,1]], np.float32)

def scale_matrix(x, y, z):
    return np.array([[x,0,0,0],
                     [0,y,0,0],
                     [0,0,z,0],
                     [0,0,0,1]], np.float32)

def uniform_scale_matrix(s):
    return np.array([[s,0,0,0],
                     [0,s,0,0],
                     [0,0,s,0],
                     [0,0,0,1]], np.float32)

def rotate_x_matrix(angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[1,0,0,0],
                     [0,c,-s,0],
                     [0,s,c,0],
                     [0,0,0,1]], np.float32)

def rotate_y_matrix(angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[c,0,s,0],
                     [0,1,0,0],
                     [-s,0,c,0],
                     [0,0,0,1]], np.float32)

def rotate_z_matrix(angle):
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[c,-s,0,0],
                     [s,c,0,0],
                     [0,0,1,0],
                     [0,0,0,1]], np.float32)

def rotate_axis(angle, axis):
    axis = axis.normalize()

    c = cos(radians(angle))
    s = sin(radians(angle))

    x00 = c+(1-c)*pow(axis.x,2)
    y00 = (1-c)*axis.x*axis.y-s*axis.z
    z00 = (1-c)*axis.x*axis.z+s*axis.y

    x01 = (1-c)*axis.y*axis.x+axis.z*s
    y01 = c+pow(axis.y,2)*(1-c)
    z01 = axis.y*axis.z*(1-c)-axis.x*s

    x02 = axis.x*axis.z*(1-c)-axis.y*s
    y02 = axis.z*axis.y*(1-c)+axis.x*s
    z02 = c+pow(axis.z,2)*(1-c)

    return np.array([[x00,y00,z00,0],
                     [x01,y01,z01,0],
                     [x02,y02,z02,0],
                     [0,0,0,1]], np.float32)

def translate(matrix, x, y, z):
    translation = translate_matrix(x, y ,z)
    return matrix @ translation

def scale(matrix, s):
    uniform_scale = uniform_scale_matrix(s)
    return matrix @ uniform_scale

def scale_non_uniform(matrix, x, y, z):
    scale = scale_matrix(x, y, z)
    return matrix @ scale

def rotate(matrix, angle, axis, local=True):
    rot = identity_matrix()
    if axis == "X":
        rot = rotate_x_matrix(angle)
    elif axis == "Y":
        rot = rotate_y_matrix(angle)
    elif axis == "Z":
        rot = rotate_z_matrix(angle)
    if local:
        return matrix @ rot
    else:
        return rot @ matrix

def rotate_complex(matrix, angle, axis, local=True):
    rotator = rotate_axis(angle, axis)
    if local:
        return matrix @ rotator
    else:
        return rotator @ matrix
