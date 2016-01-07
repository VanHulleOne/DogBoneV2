# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:13:34 2015

@author: lvanhulle
"""
import numpy
import math
from parameters import constants as c
import Line as l
class Point(object):
    
    COMPARE_PRECISION = 10000
    
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.normalVector = numpy.array([x, y, z, 1])
        
    @property
    def x(self):
        return self.__x/float(self.COMPARE_PRECISION)
        
    @x.setter
    def x(self, value):
        self.__x = int(round(value*self.COMPARE_PRECISION))
        
    @property
    def y(self):
        return self.__y/float(self.COMPARE_PRECISION)
        
    @y.setter
    def y(self, value):
        self.__y = int(round(value*self.COMPARE_PRECISION))
    
    @property
    def z(self):
        return self.__z/float(self.COMPARE_PRECISION)
        
    @z.setter
    def z(self, value):
        self.__z = int(round(value*self.COMPARE_PRECISION))
    
    def __iter__(self):
        return(i for i in (self.x, self.y, self.z))
    
    def get2DPoint(self):
        return [self.x, self.y]

    def translateMatrix(self, shiftX, shiftY, shiftZ=0):
        transMatrix = numpy.identity(4)
        transMatrix[c.X][3] = shiftX
        transMatrix[c.Y][3] = shiftY
        transMatrix[c.Z][3] = shiftZ
        return transMatrix
        
    def rotateMatrix(self, angle):
        rotateMatrix = numpy.identity(4)
        rotateMatrix[c.X][0] = math.cos(angle)
        rotateMatrix[c.Y][0] = math.sin(angle)
        rotateMatrix[c.X][1] = -rotateMatrix[c.Y][0]
        rotateMatrix[c.Y][1] = rotateMatrix[c.X][0]
        return rotateMatrix
        
    def mirrorMatrix(self, axis):
        transMatrix = numpy.identity(4)
        if(axis == c.X):
            transMatrix[c.Y][1] *= -1
        else:
            transMatrix[c.X][0] *= -1
        return transMatrix
    
    def mirror(self, axis):
        if type(axis) is l.Line:
            mList = []
            mList.append(self.translateMatrix(-axis.start.x, -axis.start.y)) #toOrigin
            angle = math.tan((axis.end.y-axis.start.y)/(axis.end.x-axis.start.x)) #angle
            mList.append(self.rotateMatrix(angle)) #rotate to X-axis
            mList.append(self.mirrorMatrix(c.X)) #mirror about X axis
            mList.append(self.rotateMatrix(-angle)) #rotate back
            mList.append(self.translateMatrix(axis.start.x, axis.start.y)) #translate back
            transMatrix = numpy.identity(4)
            for matrix in mList:
                transMatrix = numpy.dot(matrix, transMatrix)
            return self.transform(transMatrix)
        else:
            return self.transform(self.mirrorMatrix(axis))
    
    def rotate(self, angle, point=None):
        if point is None:
            point = Point(0,0)
            
        toOrigin = self.translateMatrix(-point.x, -point.y)        
        rotateMatrix = self.rotateMatrix(angle)        
        transBack = self.translateMatrix(point.x, point.y)        
        transMatrix = numpy.dot(transBack, numpy.dot(rotateMatrix, toOrigin))
        return self.transform(transMatrix)
    
    def translate(self, shiftX, shiftY, shiftZ=0):
        return self.transform(self.translateMatrix(shiftX, shiftY, shiftZ))
        
    def transform(self, transMatrix):
        nv = numpy.dot(transMatrix, self.normalVector)
        return Point(nv[c.X], nv[c.Y], nv[c.Z])
        
    def __getitem__(self, index):
        return self.normalVector[index]
    
    def __sub__(self, other):
        return numpy.linalg.norm(self.normalVector - other.normalVector)
        
    def __neg__(self):
        return Point(-self.x, -self.y)
    
    def squareDistance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)

    def __key(self):
        return (self.__z, self.__x, self.__y)
    
    def __lt__(self, other):
        return self.__key() < other.__key()
        
    def __gt__(self, other):
        return self.__key() > other.__key()

    def __eq__(self, other):
        return self.__key() == other.__key()
        
    def __ne__(self, other):
        return self.__key() != other.__key()
        
    def __hash__(self):
        return hash(self.__key())
    
    def CSVstr(self):
        return '{:.3f},{:.3f}'.format(self.x, self.y)
    
    def __str__(self):
        return 'X{:.3f} Y{:.3f} Z{:.3f}'.format(self.x, self.y, self.z)
    
    def getNormalVector(self):
        nv = [n for n in self.normalVector]
        return nv
        
    