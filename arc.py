# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 17:08:13 2015

@author: lvanhulle
"""

from LineGroup import LineGroup as LG
import math
import Point as p
import Line as l

class Arc(LG):
    
    CW = -1
    CCW = 1
    
    def __init__(self, start, end, direction, center, numPoints):
        LG.__init__(self, None)        
        self.start = start
        self.end = end
        self.direction = direction
        self.center = center
        self.numPoints = numPoints
        
        if(self.numPoints == None): self.numPoints = 20
        
        self.arcToLines()
        
    def arcToLines(self):
        """Converts an arc to a set of line segments"""
        radius = self.start.distance(self.center)
        startAngle = math.atan2(self.start.y- self.center.y,
                            self.start.x - self.center.x)
        startAngle = startAngle if startAngle >= 0 else 2*math.pi+startAngle
        endAngle = math.atan2(self.end.y- self.center.y,
                            self.end.x- self.center.y)
        endAngle = endAngle if endAngle >= 0 else 2*math.pi+endAngle
    
        includedAngle = self.calcIncludedAngle(startAngle, endAngle)
        currentAngle = startAngle
        startPoint = p.Point(self.start.x, self.start.y)
        for i in range(self.numPoints-2):
            currentAngle += includedAngle/(self.numPoints-1)
            x = self.center.x+radius*math.cos(currentAngle)
            y = self.center.y+radius*math.sin(currentAngle)
            endPoint = p.Point(x, y)
            self.addLine(l.Line(startPoint, endPoint))
            startPoint = endPoint
        endPoint = p.Point(self.end.x, self.end.y)
        self.addLine(l.Line(startPoint, endPoint))
        
    def calcIncludedAngle(self, start, end):
        """
        Given an input of two angles, calculated in unit circle fashion, and the
        direction around the circle you want to travel, this method will return
        the total included angle.
        """    
        t = end - start
        if(self.direction == self.CW and t > 0):
            return t - 2*math.pi
        elif(self.direction == self.CCW and t < 0):
            return 2*math.pi+t
        elif(t == 0):
            return 2*math.pi
        else:
            return t
            
            