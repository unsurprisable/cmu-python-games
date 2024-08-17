# April 2024

from time import time
import math



class Time:
    lastTime = -1
    scaledTime = -1
    deltaTime = 0
    scaledTimeCoefficient = 30
    def Update():
        if (Time.lastTime != -1):
            Time.deltaTime = time() - Time.lastTime
        Time.scaledTime = Time.deltaTime * Time.scaledTimeCoefficient
        Time.lastTime = time()
        
class Input:
    heldKeys = set()
    def Reset():
        Input.heldKeys.clear()
    def Update(keys):
        Input.heldKeys = keys
    def GetKey(key) -> bool:
        return key in Input.heldKeys
        
        
class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    # im using assertions because im too lazy to write out the type errors
    def __add__(self, other):
        assert type(other) is Vec, "non-vector"
        return Vec(self.x + other.x, self.y + other.y)
    def __iadd__(self, other):
        assert type(other) is Vec, "non-vector"
        self.x += other.x
        self.y += other.y
        return self
    def __sub__(self, other):
        assert type(other) is Vec, "non-vector"
        return Vec(self.x - other.x, self.y - other.y)
    def __isub__(self, other):
        assert type(other) is Vec, "non-vector"
        self.x -= other.x
        self.y -= other.y
        return self
    def __mul__(self, other):
        if (type(other) is type(Vec)):
            raise TypeError(f"Operand *: not compatible with Vec and '{type(other)}'")
        return Vec(self.x * other, self.y * other)
    def __imul__(self, other):
        assert type(other) is int or type(other) is float, "non-number"
        self.x *= other
        self.y *= other
        return self
    def __truediv__(self, other):
        assert type(other) is int or type(other) is float, "non-number"
        return Vec(self.x / other, self.y / other)
    def __itruediv__(self, other):
        assert type(other) is int or type(other) is float, "non-number"
        self.x /= other
        self.y /= other
        return self
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    def tuple(self):
        return (self.x, self.y)
    def normalized(self):
        magnitude = self.magnitude()
        return Vec(self.x/magnitude, self.y/magnitude)
    
    def up():
        return Vec(0, 1)
    def down():
        return Vec(0, -1)
    def right():
        return Vec(1, 0)
    def left():
        return Vec(-1, 0)
    def zero():
        return Vec(0, 0)
    
    @staticmethod
    def Dist(origin, other):
        return math.dist(origin.tuple(), other.tuple())
    @staticmethod
    def AngleTo(origin, other):
        difference = other - origin
        return difference.normalized()
    @staticmethod
    def VecTo(origin, other):
        return Vec.AngleTo(origin, other) * Vec.Dist(origin, other)
    @staticmethod
    def dot(vec1, vec2):
        return (vec1.x * vec2.x) + (vec1.y * vec2.y)
        

def GetNearestCirclePoint(origin: Vec, angleVec: Vec, distance, iterable):
    end: Vec = Vec(origin.x + angleVec.x * distance, origin.y + angleVec.y * distance)
    ray = Line(origin.x, origin.y, end.x, end.y, fill='lime', lineWidth=0.01, opacity=0)
    nearestPoint = None
    nearestDist = distance**2 + 1
    for shape in iterable:
        if (shape.hitsShape(ray)):
            shapeC: Vec = Vec(shape.centerX, shape.centerY)
            # Line(origin.x, origin.y, end.x, end.y, fill='lime', opacity=50, lineWidth=3,)
            # Line(origin.x, origin.y, shapeC.x, shapeC.y, fill='red', opacity=50, lineWidth=3)
            # Line(end.x, end.y, shapeC.x, shapeC.y, fill='blue', opacity=50, lineWidth=3)
            newOrigin: Vec = origin - shapeC
            b = Vec.dot(newOrigin, angleVec)
            c = Vec.dot(newOrigin, newOrigin) - shape.radius**2
            magnitude = -b - math.sqrt(b**2 - c)
            point: Vec = angleVec * magnitude + origin
            # Circle(point.x, point.y, 4, fill='yellow')
            # print(f"{point = }")
            # print(point - Vec.VecTo(origin, shapeC))
            dist = Vec.Dist(origin, point)
            if (dist < nearestDist):
                nearestPoint = point
                nearestDist = dist
    ray.visible = False
    return nearestPoint




class Player:
    class GrappleGun:
        def __init__(self, originShape):
            self.isActive = False
            self.rope = Line(0,0,0,0, fill=rgb(25, 25, 25), lineWidth=4, visible=False)
            self.grapple = Circle(0,0, 2, fill=rgb(25,25,25), visible=False)
            self.visual = Group(self.rope, self.grapple)
            
            self.originShape = originShape
            self.targetVec = None
            self.fireDistance = 300
            
            self.targetRadius = 0
            self.ropeConstant = 1000
        
        def Fire(self, mousePos: Vec):
            origin = Vec(self.originShape.centerX, self.originShape.centerY)
            angle = Vec.AngleTo(origin, mousePos)
            blocksInRange = set()
            for block in app.levelManager.GetGripBlocks():
                # get all blocks in range of the grappler
                shapeCenter = Vec(block.visual.centerX, block.visual.centerY)
                if (Vec.Dist(origin, shapeCenter) <= self.fireDistance + math.sqrt(block.visual.width**2 + block.visual.height**2)/2):
                    blocksInRange.add(block.visual)
            point = GetNearestCirclePoint(origin, angle, self.fireDistance, blocksInRange)
            if (point != None):
                self.isActive = True
                self.targetVec = point
                # self.targetRadius = Vec.Dist(origin, point) * 1.25
                self.grapple.centerX, self.grapple.centerY = point.x, point.y
                self.rope.x2, self.rope.y2 = point.x, point.y
                self.UpdateVisual()
                self.visual.visible = True
                
        def Collect(self):
            self.isActive = False
            self.targetVec = None
            self.visual.visible = False
        
        def UpdateVisual(self):
            self.rope.x1, self.rope.y1 = self.originShape.centerX, self.originShape.centerY
                
        def GetTensionForce(self):
            if (not self.isActive):
                return Vec.zero()
            else:
                originVec = Vec(self.originShape.centerX, -self.originShape.centerY)
                targetVec = Vec(self.targetVec.x, -self.targetVec.y)
                dir: Vec = Vec.AngleTo(originVec, targetVec)
                forceVec = dir * ((Vec.Dist(originVec, self.targetVec) - self.targetRadius)**2 / self.ropeConstant)
                return forceVec
            
        
        
    def __init__(self, position):
        self.position = position
        self.sprite = Oval(0,0, 20, 30)
        self.sprite.centerX, self.sprite.centerY = self.position.tuple()
        self.visual = Group( self.sprite )
        
        self.grappleGun = Player.GrappleGun(self.sprite)
        
        # Physics
        self.gravity = 12
        self.velocity = Vec(80, 200)
        self.mass = 60
        self.airResistance = 50
        
        self.jumpSpeed = 175
        self.isGrounded = False
        
    def onMousePress(self, pos, button):
        if (button == 0):
            self.grappleGun.Fire(pos)
            
    def onMouseRelease(self, pos, button):
        if (button == 0):
            self.grappleGun.Collect()
        
    
    def HandleForces(self):
        velocity = self.velocity * Time.scaledTime
        mass = self.mass
        gravity = self.gravity * Time.scaledTime
        dragCoef = self.airResistance/8
        
        weightForce = Vec(0, mass * -gravity)
        dragForce = velocity.normalized() * Vec.dot(velocity, velocity) * dragCoef * -1
        grappleForce = self.grappleGun.GetTensionForce()
        
        netForce = weightForce + dragForce + grappleForce
        acceleration = netForce / mass
        
        self.velocity += acceleration * Time.scaledTime
        

    def Destroy(self):
        self.grappleGun.Collect()
        self.visual.visible = False
        app.player = None
        del self
    
    
    def Update(self):
        if (Time.deltaTime == 0): return
    
        self.HandleForces()
        if (self.grappleGun.isActive):
            self.grappleGun.UpdateVisual()
    
        # move the player on the canvas based on their velocity
        velocity = self.velocity * Time.scaledTime
        self.visual.centerX += velocity.x
        self.visual.centerY -= velocity.y
        
        if (self.visual.centerY > 650):
            RespawnPlayer()
        


class LevelManager:
    def __init__(self):
        self.grippableBlocks = set()
    
    def CreateGripBlock(self, position, size):
        gripBlock = GripBlock(position, size)
        self.grippableBlocks.add(gripBlock)
        return gripBlock
        
    def GetGripBlocks(self):
        return self.grippableBlocks.copy()
        
app.levelManager = LevelManager()
    
        
class GripBlock:
    def __init__(self, position, size):
        self.position = position
        self.visual = Circle(0,0, size, fill='gray', border='darkGray')
        self.visual.centerX, self.visual.centerY = position.tuple()
        
        
app.levelManager.CreateGripBlock(Vec(325, 150), 20)
app.levelManager.CreateGripBlock(Vec(100, 300), 30)
app.levelManager.CreateGripBlock(Vec(200, 75), 45)

app.player = None

def RespawnPlayer():
    if (app.player != None):
        app.player.Destroy()
    app.player = Player(Vec(0, 300))
    
    
RespawnPlayer()
    

def onKeyHold(keys):
    Input.Update(keys)
    
app.stepsPerSecond = 60
def onStep():
    Time.Update()
    if (app.player != None): app.player.Update()
    Input.Reset()
    
    
def onMousePress(mx, my, button):
    if (app.player != None): app.player.onMousePress(Vec(mx, my), button)
def onMouseRelease(mx, my, button):
    if (app.player != None): app.player.onMouseRelease(Vec(mx, my), button)
    
    

Label("Mouse to aim, LMB to grapple (scuffed)", 200, 15, size=16, bold=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        