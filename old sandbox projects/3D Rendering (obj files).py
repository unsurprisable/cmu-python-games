# January 2024

import re
import math
import time
import random

app.setMaxShapeCount(2147483647)

class Input:
    
    keyDownList = []
    keyUpList = []
    keyHeldList = []
    
    mouseDownList = [False, False, False]
    mouseUpList = [False, False, False]
    mouseHeldList = [False, False, False]

    @staticmethod
    def GetKeyDown(key):
        if (key in Input.keyDownList):
            return True
        return False

    @staticmethod
    def GetKeyUp(key):
        if (key in Input.keyUpList):
            return True
        return False

    @staticmethod
    def GetKey(key):
        if (key in Input.keyHeldList):
            return True
        return False


    @staticmethod
    def GetMouseDown(button):
        if (Input.mouseDownList[button]):
            return True
        return False

    @staticmethod
    def GetMouseUp(button):
        if (Input.mouseUpList[button]):
            return True
        return False

    @staticmethod
    def GetMouse(button):
        if (Input.mouseHeldList[button]):
            return True
        return False


        
    @staticmethod
    def Update():
        Input.keyDownList.clear()
        Input.keyUpList.clear()
        Input.keyHeldList.clear()
        Input.mouseDownList = [False, False, False]
        Input.mouseUpList = [False, False, False]
     
        
class Time:
    lastFrame = time.time()
    timeScale = 1
    deltaTime = 0.0
    realDeltaTime = 0.0
    
    @staticmethod
    def Update():
        Time.deltaTime = (time.time() - Time.lastFrame) * Time.timeScale
        Time.realDeltaTime = (time.time() - Time.lastFrame)
        Time.lastFrame = time.time()
        
        
def Remap(value, oldMin, oldMax, newMin, newMax):
    if (oldMin == oldMax):
        return newMin
        
    if (oldMin > oldMax):
        tempMax = oldMin
        oldMin = oldMax
        oldMax = tempMax
    if (newMin > newMax):
        tempMax = newMin
        newMin = newMax
        newMax = tempMax
        
    return (((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin

########## ENGINE STUFF ##########




app.obj = ""

app.background = gradient(rgb(210, 210, 210), rgb(240, 240, 240), start='top-left')

class Vertex:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return f"Vertex({self.x}, {self.y}, {self.z})"
        
    def __repr__(self):
        return f"Vertex({self.x}, {self.y}, {self.z})"
        
    def __sub__(self, other):
        return Vertex(self.x - other.x, self.y - other.y, self.z - other.z)
        
    def _eq__(self, other):
        if (not isinstance(other, Vertex)):
            raise TypeError(f"Cannot compare Vertex to {type(other)}")
        return (self.x == other.x and self.y == other.y and self.z == other.z)

class Face:
    def __init__(self, rawVerticesTuple):
        self.vertices = [*rawVerticesTuple]
        self.depth = sum(vertex.z for vertex in self.vertices) / len(self.vertices)
        self.verticesTuple = ()
        for vertex in self.vertices:
            self.verticesTuple += (vertex.x, vertex.y)
        self.normal = self.calculateNormal()
    
    def calculateNormal(self):
        v1 = self.vertices[1] - self.vertices[0]
        v2 = self.vertices[2] - self.vertices[0]
        normal = Vertex(
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
            )
        length = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)
        if (length != 0):
            normal.x /= length
            normal.y /= length
            normal.z /= length
        return normal
        
        
    def calculateLighting(self):
        lightVector = app.light
        
        intensity = self.normal.x * lightVector.x + self.normal.y * lightVector.y + self.normal.z * lightVector.z
        intensity = max(0, min(intensity, 1))
        
        
        faceCenter = Vertex(
            sum(vertex.x for vertex in self.vertices) / len(self.vertices),
            sum(vertex.y for vertex in self.vertices) / len(self.vertices),
            sum(vertex.z for vertex in self.vertices) / len(self.vertices)
            )
        distanceToLight = math.sqrt(
            (faceCenter.x - (lightVector.x * app.baseScale + app.transformX))**2 +
            (faceCenter.y - (lightVector.y * app.baseScale + app.transformY))**2 +
            (faceCenter.z - (lightVector.z * app.baseScale + app.transformZ))**2
            )
            
        attenuationFactor = 1 / (1 + (distanceToLight**3.5) / 10**8.9)
        # attenuationFactor = 1000
        intensity *= attenuationFactor
        
        color = int(intensity * 220)
        # color = Remap(self.depth, app.frontMost * app.scale + app.transformZ, app.backMost * app.scale + app.transformZ, 0, 255 + (-20))
        color = max(0, min(color, 255))
        self.mesh.fill = rgb(color, color, color)
        self.mesh.border = rgb(color, color, color)
        
        
    def draw(self):
        self.mesh = Polygon(*self.verticesTuple)
        # print(f"formed a face with coordinates {self.verticesTuple}")
        
    # def __repr__(self):
    #     return f"""Triangle(
    #         [{int(self.vertices[0].x)}, {int(self.vertices[0].y)}, {int(self.vertices[0].z)}], 
    #         [{int(self.vertices[1].x)}, {int(self.vertices[1].y)}, {int(self.vertices[1].z)}], 
    #         [{int(self.vertices[2].x)}, {int(self.vertices[2].y)}, {int(self.vertices[2].z)}], 
    #     )"""
        
    
    def Destroy(self):
        if (isinstance(self.mesh, Polygon)):
            self.mesh.visible = False
        del self


### or use console w/ the function right here (bypasses 90,000 char limit)
def R(fileText):
    app.obj = fileText
    InitialRender()
    
    
    
app.scaleFactor = 0.8 # to what percent of the screen the auto-scale targets (0-1: 0.5 = half of the screen, 1 = all of the screen)
app.light = Vertex(0.25, 0.2, -0.75)

app.scale = 0
app.transformX = 0
app.transformY = 0
app.transformZ = 75
    
app.leftMost = None
app.rightMost = None
app.topMost = None
app.bottomMost = None

app.frontMost = None
app.backMost = None
    
app.renderingFinished = False


def InitializeVertices():
    app.rendLabel = Label("Rendering...", 200, 200, size=36, bold=True)
    
    sleep(0.01)
    
    vertexSearch = re.findall(r'v\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)', app.obj)
    faceSearch = re.findall(r'f\s[0-9\s]+', app.obj)
    
    rawVertices = ['{} {} {}'.format(match[0], match[2], match[4]) for match in vertexSearch]
    rawFaces = [match.replace('f ', '').split() for match in faceSearch]
    
    # print(rawVertices)
    # print(rawFaces)
    
    app.faceIndexList = []
    for rawFace in rawFaces:
        app.faceIndexList.append([int(index) for index in rawFace])
    
    app.vertices = []
    for rawVertex in rawVertices:
        components = rawVertex.split(' ')
        app.vertices.append(Vertex(
            float(components[0]),
            -float(components[1]),
            float(components[2])
        ))
        
    for vertex in app.vertices:
        if (app.leftMost == None):
            app.leftMost = vertex.x
            app.rightMost = vertex.x
            app.topMost = vertex.y
            app.bottomMost = vertex.y
            app.frontMost = vertex.z
            app.backMost = vertex.z
        else:
            if (vertex.x < app.leftMost):
                app.leftMost = vertex.x
            elif (vertex.x > app.rightMost):
                app.rightMost = vertex.x
            if (vertex.y < app.topMost):
                app.topMost = vertex.y
            elif (vertex.y > app.bottomMost):
                app.bottomMost = vertex.y
            if (vertex.z > app.frontMost):
                app.frontMost = vertex.z
            elif (vertex.z < app.backMost):
                app.backMost = vertex.z
                
    print(f"FRONT Z: {app.frontMost}")
    print(f"BACK Z: {app.backMost}")
    
    # center the model
    app.transformX = 200 - (app.rightMost + app.leftMost) / 2
    app.transformY = 200 - (app.bottomMost + app.topMost) / 2
    
    # scale the model
    horzScale = 400 / (app.rightMost - app.leftMost)
    vertScale = 400 / (app.bottomMost - app.topMost)
    
    print(f"horzScale = {horzScale}")
    print(f"vertScale = {vertScale}")
    print(f"min = {min(horzScale, vertScale) * app.scaleFactor}")
    app.scale = min(horzScale, vertScale) * app.scaleFactor
    app.baseScale = app.scale
    app.minScale = app.scale * 0.2
    app.maxScale = app.scale * 4
    
    
def DrawFaces():
    app.faces = []
    for faceIndex in app.faceIndexList:
        faceVertices = ()
        for index in faceIndex:
            vertex = app.vertices[index-1]
            faceVertices += (Vertex(
                vertex.x * app.scale + app.transformX,
                vertex.y * app.scale + app.transformY,
                vertex.z * app.scale + app.transformZ,
                ),)
        app.faces.append(Face(faceVertices))
        
    app.sortedFaces = sorted(app.faces, key=lambda face:face.depth)
    for face in app.sortedFaces:
        face.draw()
        face.calculateLighting()
        
    app.renderingFinished = True
    app.paused = False
    app.rendLabel.visible = False
    app.zoomNotice.visible = False
    print("Render complete!")
    
    
def InitialRender():
    InitializeVertices()
    Label("+/- to zoom", 5, 8, size=12, align='left', bold=True)
    Label("A/D to move the light X", 5, 24, size=12, align='left', bold=True)
    Label("W/S to move the light Y", 5, 40, size=12, align='left', bold=True)
    Label("Q/E to move the light Z", 5, 56, size=12, align='left', bold=True)
    Label("R to reset light", 5, 72, size=12, align='left', bold=True)
    DrawFaces()
    
    
def Rerender():
    for face in app.faces:
        face.Destroy()
    DrawFaces()
    
def UpdateLighting():
    for face in app.faces:
        face.calculateLighting()
    
    
app.zoomNotice = Label("Re-rendering...", 200, 360, size=24, bold=True, visible=False)
    
def ZoomIn():
    newScale = max(app.minScale, min(app.scale + app.baseScale * 0.2, app.maxScale))
    ApplyZoom(newScale)
def ZoomOut():
    newScale = max(app.minScale, min(app.scale - app.baseScale * 0.2, app.maxScale))
    ApplyZoom(newScale)
        
def ApplyZoom(newScale):
    if (app.scale != newScale):
        app.scale = newScale
    app.zoomTimer = app.zoomBuffer
    
    
# def Rotate(xAxis, yAxis, zAxis):
    
    
    
    
if (app.obj == ""):
    consoleCheck = app.getTextInput("To use this program, you will need to have a downloaded 3D model as a '.obj' file (examples: https://people.sc.fsu.edu/~jburkardt/data/obj/obj.html). Then you will need to open that file in any text editor of your choosing and copy and paste all of that text into this program. (Dont paste anything yet, this is just a tutorial box.) Hit 'Enter' or press 'OK' to continue.")
    if (consoleCheck != "c" and consoleCheck != "cmd" and consoleCheck != "con" and consoleCheck != "console" and consoleCheck != "command"):
        app.obj = app.getTextInput("CMU's text input feature seems to be limited to about 90,000 characters per input. Check how many characters you have in your file. If it's over 90,000, you are going to have to copy and paste smaller chunks at a time. Proceed to paste the first part of your file (under 90,000 characters!). Hit 'Enter' or press 'OK' once you have done so.").lower()
        while True:
            input = app.getTextInput("Input recieved! If you have finished entering the contents of your model, simply type 'done'. Otherwise, proceed to paste the next part of your file. (Start exactly where you left off, and remember to keep it under 90,000 characters.) Hit 'Enter' or press 'OK' to continue.").lower()
            if (input == "done" or input == "d" or input == "do" or input == "don" or input == "dn"):
                break
            app.obj += input
        app.getTextInput("Perfect! After exiting this prompt, your model should show up in the program window. If it does not, you might have to restart and make sure you entered your file text correctly. Also make sure to check the keybinds in the top-left once you are in. Hit 'Enter' or press 'OK' to continue.")
        InitialRender()
    
    
app.zoomBuffer = 0.75
app.zoomTimer = None
    
app.stepsPerSecond = 60
def onStep():
    if (not app.renderingFinished):
        return
    inputDir = Vertex(0, 0, 0)
    if (Input.GetKey('w')):
        inputDir.y -= 1
    if (Input.GetKey('a')):
        inputDir.x -= 1
    if (Input.GetKey('s')):
        inputDir.y += 1
    if (Input.GetKey('d')):
        inputDir.x += 1
    if (Input.GetKey('q')):
        inputDir.z += 1
    if (Input.GetKey('e')):
        inputDir.z -= 1
        
    if (Input.GetKeyDown('r')):
        app.light = Vertex(0.25, 0.2, -0.75)
        
    if (Input.GetKeyDown('=')):
        ZoomIn()
    if (Input.GetKeyDown('-')):
        ZoomOut()
        
    if (Input.GetKeyDown('u')):
        # rotate around X  UP
        pass
    if (Input.GetKeyDown('i')):
        # rotate around X DOWN
        pass
    if (Input.GetKeyDown('h')):
        # rotate around Y LEFT
        pass
    if (Input.GetKeyDown('j')):
        # rotate around Y RIGHT
        pass
    if (Input.GetKeyDown('b')):
        # rotate around Z LEFT
        pass
    if (Input.GetKeyDown('n')):
        # rotate around Z RIGHT
        pass
    
        
    app.light.x += inputDir.x * Time.deltaTime / 2*(app.baseScale / app.scale)
    app.light.y -= inputDir.y * Time.deltaTime / 2*(app.baseScale / app.scale)
    app.light.z += inputDir.z * Time.deltaTime / 2*(app.baseScale / app.scale)
    
    if (inputDir != Vertex(0,0,0)):
        UpdateLighting()
        
    if (app.zoomTimer != None):
        app.zoomTimer -= Time.deltaTime
        if (app.zoomTimer <= 0):
            app.zoomTimer = None
            app.zoomNotice.visible = True
            app.zoomNotice.toFront()
            sleep(0.01)
            Rerender()
            
    
    
        
    Input.Update()
    Time.Update()





def onKeyPress(key):
    Input.keyDownList.append(key)
    
def onKeyRelease(key):
    Input.keyUpList.append(key)
    
def onKeyHold(keys):
    for key in keys:
        Input.keyHeldList.append(key)
    
def onMousePress(x, y, button):
    if (button == 0):
        Input.mouseDownList[0] = True
        Input.mouseHeldList[0] = True
        
    elif (button == 1):
        Input.mouseDownList[2] = True
        Input.mouseHeldList[2] = True
        
    elif (button == 2):
        Input.mouseDownList[1] = True
        Input.mouseHeldList[1] = True
    
def onMouseRelease(x, y, button):
    if (button == 0):
        Input.mouseUpList[0] = True
        Input.mouseHeldList[0] = False
        
    elif (button == 1):
        Input.mouseUpList[2] = True
        Input.mouseHeldList[2] = False
        
    elif (button == 2):
        Input.mouseUpList[1] = True
        Input.mouseHeldList[1] = False






Label("The lighting is a little buggy right now...", 5, 390, size=14, align='left', opacity=25)




    
        

