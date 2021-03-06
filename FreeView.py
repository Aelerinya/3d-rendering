from graphics import *
import numpy as np
import math
import time

class p3 :

    focalLength = 0
    width = 0
    height = 0
    unit = 0

    focalPoint = 0
    plane = 0
    origin = 0
    vI = 0
    vJ = 0

    def setup (self) :
        f = self.focalPoint.getA1()
        p = self.plane

        k = -(p[0]*f[0] + p[1]*f[1] + p[2]*f[2] + p[3]) / (p[0]**2 + p[1]**2 + p[2]**2)

        self.origin = np.matrix([[k*p[0]+f[0]],
                                 [k*p[1]+f[1]],
                                 [k*p[2]+f[2]]])

        self.vN = np.matrix([[p[0]], [p[1]], [p[2]]])

    def __init__ (self, matrix) :
        self.matrix = matrix

    def render (self) :
        flatCoordinates = self.matrix.getA1()
        x = flatCoordinates[0]
        y = flatCoordinates[1]
        z = flatCoordinates[2]

        f = self.focalPoint.getA1()
        p = self.plane

        k = -(p[0]*f[0] + p[1]*f[1] + p[2]*f[2] + p[3]) / (p[0]*x - p[0]*f[0] + p[1]*y - p[1]*f[1] + p[2]*z - p[2]*f[2])

        projectionX = k * (x - f[0]) + f[0]
        projectionY = k * (y - f[1]) + f[1]
        projectionZ = k * (z - f[2]) + f[2]

        pI = self.vI.getA1()
        pJ = self.vJ.getA1()
        pO = self.origin.getA1()

        a = np.matrix([[projectionX - pO[0]],
                       [projectionY - pO[1]]])

        b = np.matrix([[pI[0], pJ[0]],
                       [pI[1], pJ[1]]])
        c = np.linalg.inv(b)

        coords = c * a
        flatCoords = coords.getA1()

        X = flatCoords[0]
        Y = flatCoords[1]

        return Point((X + self.width / 2)*self.unit, (Y + self.height / 2)*self.unit)

    def rotate (self, origin, rotation) :
        self.matrix = origin + rotation * (self.matrix - origin)

    def distance (self, otherPoint) :
        p1 = self.matrix.getA1()
        p2 = otherPoint.matrix.getA1()
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

    def translateScreen (self, scale, along) :
        if along == 0 :
            translation = scale * self.vN
            self.focalPoint += translation
            self.origin += translation
            self.plane[3] -= scale
        if along == 1 :
            translation = scale * self.vI
            self.focalPoint += translation
            self.origin += translation
        if along == 2 :
            translation = scale * self.vJ
            self.focalPoint += translation
            self.origin += translation

    def rotateScreen (self, angle, around) :
        if around == 0 :
            axis = self.vN
        elif around == 1 :
            axis = self.vI
        elif around == 2 :
            axis = self.vJ

        flat = axis.getA1()
        x = flat[0]
        y = flat[1]
        z = flat[2]

        c = math.cos(angle)
        nc = 1-c
        s = math.sin(angle)

        rotation = np.matrix([[x**2*nc+c, x*y*nc-z*s, x*z*nc+y*s],
                            [x*y*nc+z*s, y**2*nc+c, y*z*nc-x*s],
                            [x*z*nc-y*s, y*z*nc+x*s, z**2*nc+c]])

        self.vI = rotation * self.vI
        self.vJ = rotation * self.vJ

        if around == 1 or around == 2 :
            self.origin = self.focalPoint + rotation * (self.origin - self.focalPoint)
            self.vN = rotation * self.vN

            n = self.vN.getA1()
            o = self.origin.getA1()
            self.plane = [n[0], n[1], n[2], -(n[0]*o[0] + n[1]*o[1] + n[2]*o[2])]



def main ():
    p3.unit = unit = 10
    p3.width  = width = 192
    p3.height = height = 108

    p3.focalPoint = focalPoint = np.matrix([[32.], [24.], [-80.]])
    p3.plane = plane = [0,0,1,0]
    p3.vI = vI = np.matrix([[1.], [0.], [0.]])
    p3.vJ = vJ = np.matrix([[0.], [1.], [0.]])

    p3.setup(p3)

    win = GraphWin("Moteur 3D", width*unit, height*unit)
    quit = False

    #Put black background
    background = Rectangle(Point(0, 0), Point(width*unit, height*unit))
    background.setFill('black')
    background.draw(win)

    cubeCoord = [[[22],[14],[2]], [[42],[14],[2]], [[42],[34],[2]], [[22],[34],[2]], [[22],[14],[22]], [[42],[14],[22]], [[42],[34],[22]], [[22],[34],[22]]]
    cubeNet = [[0,1], [1,2], [2,3], [3,0], [4,5], [5,6], [6,7], [7,4], [0,4], [1,5], [2,6], [3,7]]
    cubeCenter = np.matrix([[32], [24], [12]])
    cube = []
    lines = []
    vNChanged = True

    for coord in cubeCoord :
        cube.append(p3(np.matrix(coord)))

    while quit == False :
        input = win.checkKey()

        if input == "Escape" :
            quit = True

        elif input == "a" :
            p3.translateScreen(p3, -0.4, 2)
        elif input == "e" :
            p3.translateScreen(p3, 0.4, 2)
        elif input == "q" :
            p3.translateScreen(p3, -0.4, 1)
        elif input == "d" :
            p3.translateScreen(p3, 0.4, 1)
        elif input == "z" :
            p3.translateScreen(p3, 0.4, 0)
        elif input == "s" :
            p3.translateScreen(p3, -0.4, 0)
        elif input == "u" :
            p3.rotateScreen(p3, 0.05, 0)
        elif input == "o" :
            p3.rotateScreen(p3, -0.05, 0)
        elif input == "i" :
            p3.rotateScreen(p3, -0.02, 1)
            vNChanged = True
        elif input == "k" :
            p3.rotateScreen(p3, 0.02, 1)
            vNChanged = True
        elif input == "j" :
            p3.rotateScreen(p3, -0.02, 2)
            vNChanged = True
        elif input == "l" :
            p3.rotateScreen(p3, 0.02, 2)
            vNChanged = True

        time.sleep(1.0/60)

        if input == "" or vNChanged == True :

            for point in cube :
                if vNChanged == True :
                    flat = point.vN.getA1()
                    x = flat[0]
                    y = flat[1]
                    z = flat[2]

                    c = math.cos(.05)
                    nc = 1-c
                    s = math.sin(.05)

                    cubeRotation = np.matrix([[x**2*nc+c, x*y*nc-z*s, x*z*nc+y*s],
                                        [x*y*nc+z*s, y**2*nc+c, y*z*nc-x*s],
                                        [x*z*nc-y*s, y*z*nc+x*s, z**2*nc+c]])

                point.rotate(cubeCenter, cubeRotation)

            for line in lines :
                line.undraw()

            for link in cubeNet :
                line = Line(cube[link[0]].render(), cube[link[1]].render())
                line.setFill("white")
                line.draw(win)
                lines.append(line)


main()
