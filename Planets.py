import math
import numpy as np
from PyQt5.QtGui import *
import random as rand

class Planet():
    def __init__(self, name, mass, dist, phi, theta, position, vel, acel):
        self.name = name
        self.mass = mass
        self.dist = dist
        self.vel = vel
        self.phi = phi
        self.theta = theta
        self.acel = acel
        self.force = np.zeros(3)
        self.position = position
        self.trace = []

        self.position_Graph = np.zeros(3)
        self.color = QColor(255,255,255,255)
        self.previosPosition = np.zeros(3)

    def grafPosition(self, length):
        for i in range(len(self.position_Graph)):
            self.previosPosition[i] = self.position_Graph[i]
            self.position_Graph[i] = length*self.position[i]/(5*10**12)
    
    def randColor(self):
        self.color = QColor(rand.randint(0,255), rand.randint(0,255), rand.randint(0,255) , 255)

def RandomSolar(length):
    solar = []
    for i in range(500):
        position = [rand.randint(-10**13, 10**13), rand.randint(-10**13, 10**13), rand.randint(-10**13, 10**13)]
        mass = rand.randint(10**20, 10**37)
        k = Planet("", mass, 0, 0, 0, position, np.zeros(3), np.zeros(3))
        k.randColor()
        k.grafPosition(length)
        solar.append(k)
    return solar

def SolarSystem(length):
    planets = np.array(['Slunce', 'Merkur', 'Venuše', 'Země', 'Mars', 'Jupite', 'Saturn', 'Uran', 'Neptun'])
    mass = np.array([1.989*10**30, 3.287*10**23, 4.867*10**24, 5.972*10**24, 6.39*10**23, 1.898*10**27, 5.683*10**26, 8.681*10**25, 1.024*10**26])
    dist = np.array([0, 57.91*10**9, 108.2*10**9, 149.6*10**9, 227.9*10**9, 778.5*10**9, 1.434*10**12, 2.871*10**12, 4.495*10**12])
    vel = np.array([0, 170503/3.6, 130074/3.6, 107218/3.6, 86677/3.6, 47002/3.6, 34701/3.6,24477/3.6, 19566/3.6])
    theta = np.array([90, 90, 90, 90, 90, 90, 90, 90, 90])
    phi = np.array([0, 245, 295, 198, 166, 97, 75, 212, 130])
    solar = []
    for i in range(len(planets)):
        hanicka = PositionKartez(dist[i], theta[i], phi[i])
        vector = OnesVector(np.array([0.0,0.0,0.0]), hanicka)
        velocity = np.array([vel[i]*vector[1], -vel[i]*vector[0], vel[i]*vector[2]])
        k = Planet(planets[i], mass[i], dist[i], phi[i], theta[i], hanicka, velocity, np.zeros(3))
        k.randColor()
        k.grafPosition(length)
        solar.append(k)
    return solar

def SolarSystemLook(system, length):
    for i in system:
        i.grafPosition(length)

def GravitationForce(m1, m2, r):
    G = 6.67384*10**-11
    return G*(m1*m2)/r**2

def Velocity(v, a, t):
    return v + a*t

def Move(s, a, v, t):
    return s + v*t + 0.5*a*t**2

def Acceleration(a, F, m):
    return a + F/m

def PositionKartez(r, theta, phi):
    x= r*math.sin(math.radians(theta))*math.cos(math.radians(phi))
    y= r*math.sin(math.radians(theta))*math.sin(math.radians(phi))
    z= r*math.cos(math.radians(theta))
    return np.array([x, y, z])

def Distance(b1, b2):
    return math.sqrt((b2[0]-b1[0])**2+(b2[1]-b1[1])**2+(b2[2]-b1[2])**2)

def OnesVector(b1, b2):
    d=Distance(b1,b2)
    return np.array([(b2[0]-b1[0])/d, (b2[1]-b1[1])/d, (b2[2]-b1[2])/d])

def CountForces(system):
    for i in range(math.ceil(len(system)/2)):
        s = system[i]
        for k in system:
            if s==k:
                continue
            force = GravitationForce(s.mass, k.mass, Distance(s.position, k.position))
            vector = OnesVector(s.position, k.position)
            s.force = np.add(vector*force, s.force)
            k.force = np.add(-vector*force, k.force)

def CountNewPosition(system, time, length):
    for s in system:
        s.trace.append(s.position)
        for i in range(3):
            s.position[i] = Move(s.position[i], s.acel[i], s.vel[i], time)
            s.acel[i] = Acceleration(s.acel[i], s.force[i], s.mass)
            s.vel[i] = Velocity(s.vel[i], s.acel[i], time)
        s.grafPosition(length)
   