import math
import time
import random

############### ENGINE ############### 

### Vector2
# Stores x, y, and magnitude components.
# When passing a vector as an argument, its own reference is passed in---not a copy of it
# Supports (get; & set;) of the x, y, and magnitude; everything updates itself accordingly.
# Check the bottom of this class for additional functionality.
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self._magnitude = 0.0
        self._x = x
        self._y = y
        self.UpdateMagnitude()
    

    def __imul__(self, scalar):
        self._x *= scalar
        self.y *= scalar
        return self
        
    def __mul__(self, scalar):
        self._x *= scalar
        self.y *= scalar
        return self
        
    def __rmul__(self, scalar):
        self._x *= scalar
        self.y *= scalar
        return self

    def __add__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +: Vector2 and " + type(other).__name__)
    
    def __iadd__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +: Vector2 and " + type(other).__name__)
    
    def __radd__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +: Vector2 and " + type(other).__name__)

    def __sub__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Unsupported operand type for '-': Vector2 and " + type(other).__name__)

    def __isub__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Unsupported operand type for '-': Vector2 and " + type(other).__name__)

    def __rsub__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Unsupported operand type for '-': Vector2 and " + type(other).__name__)
            
    def __eq__(self, other):
        if (isinstance(other, Vector2)):
            return (self.x == other.x and self.y == other.y and self._magnitude == other._magnitude)
        else:
            raise TypeError("Unsupported comparison type for '==': Vector2 and " + type(other).__name__)
            
    def __str__(self):
        return f"({self.x}, {self.y})"
        
        
    @property
    def x (self):
        return self._x
    @x.setter
    def x (self, newX):
        self._x = newX
        self.UpdateMagnitude()
        
        
    @property
    def y (self):
        return self._y
    @y.setter
    def y (self, newY):
        self._y = newY
        self.UpdateMagnitude()
        
        
    @property
    def magnitude (self):
        return self._magnitude
    @magnitude.setter
    def magnitude (self, newMag):
        change = newMag/self.magnitude
        self._magnitude = newMag
        self.UpdateComponents(change)
        
    
        
    def UpdateMagnitude(self):
        self._magnitude = math.sqrt(self.x ** 2 + self.y ** 2)
        
    def UpdateComponents(self, change):
        self._x *= change
        self._y *= change
        
    ### Vector2 - METHODS
    # .normalized --- returns a duplicate of the vector in unit form (magnitude resets to 1; direction is preserved)
    # NOTE: This is purely a getter function; it returns a new Vector2. It does not change the current one.
    @property
    def normalized(self):
        self.UpdateMagnitude()
        if (self._magnitude != 0):
            return Vector2(self.x / self._magnitude, self.y / self._magnitude)
        else:
            return Vector2(0, 0)
    
    # .zero --- shorthand for creating a Vector2(0, 0)
    @staticmethod
    def zero():
        return Vector2(0.0, 0.0)
    # .left --- shorthand for creating a Vector2(-1, 0)
    @staticmethod
    def left():
        return Vector2(-1.0, 0.0)
    # .right --- shorthand for creating a Vector2(1, 0)
    @staticmethod
    def right():
        return Vector2(1.0, 0.0)
    # .up --- shorthand for creating a Vector2(0, 1)
    @staticmethod
    def up():
        return Vector2(0.0, 1.0)
    # .down --- shorthand for creating a Vector2(0, -1)
    @staticmethod
    def down():
        return Vector2(0.0, -1.0)
    # .one --- shorthand for creating a Vector2(1, 1)
    @staticmethod
    def one():
        return Vector2(1.0, 1.0)
        
    # .randomDir(preciseness) --- shorthand for generating a random normalized Vector2.
    # argument: 'preciseness' --- multiple of 10. Every zero represents another decimal place of preciseness when generating.
    # eg. a 'preciseness' of 1 will cause the vector to only generate eight basic directions.
    @staticmethod
    def randomDir(preciseness = 1):
        if (preciseness < 1):
            preciseness = 1
        x = random.randrange(-1*preciseness, 1*preciseness)
        y = random.randrange(-1*preciseness, 1*preciseness)
        newVector = Vector2(x, y).normalized
        return newVector
        
    # .angleTo(x1, y1, x2, y2) --- returns a unit Vector2 pointing from the first set of coordinates to the second.
    @staticmethod
    def angleTo(x1, y1, x2, y2):
        return Vector2(x2-x1, y2-y1).normalized



### Input
# !!! No need to put anything in 'onKeyPress', 'onMousePress', 'onMouseMove' etc...
# In a class w/ an Update() function, use this as a conditional
# eg. "if (Input.GetKey('w') or Input.GetMouseUp(0) or Input.GetKeyDown('space'))"
# LMB - 0, RMB - 1, SCROLL BUTTON - 2
# Use 'Input.mouseX' and 'Input.mouseY' for the mouse position.
class Input:
    
    mouse = Vector2(200, 200)
    
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
     
        
        
### Time
# Only currently used for Time.deltaTime --- get the time in seconds from the last frame. 
# Useful for countdowns/timers, consistent animations, physics corrections, etc..
class Time:
    lastFrame = time.time()
    deltaTime = 0.0
    
    @staticmethod
    def Update():
        Time.deltaTime = time.time() - Time.lastFrame
        Time.lastFrame = time.time()
        
        
        
### GameObject --- IMPORTANT!
# When making a dynamic object (would typically use 'onStep') on the canvas, make it a class that inherits this one.
# Adds an Update() function; override it in the child class to run code every frame.
# Also, if your new class is going to use its own '__init__()', make sure to still call 'super().__init__()' inside of it. Otherwise, the updates will not run.
# Make sure to actually instantiate the class! Otherwise, nothing will happen.
# No need to do anything with the 'onStep' function; use this instead to stay organized!
# To make a GameObject stop updating, USE: "gameObjectInstance.DestroySelf()" or "GameObject.Destroy(targetGameObject)"
# Every game object has its own 'visual' (sprite), 'collider' (hitbox), and 'transform' (stores position & scale)
# The transform is integrated so that the 'visual' & 'collider' will update alongside it.
class GameObject:
    def __init__(self):
        self.visual = Rect(1,1,1,1,opacity=0)
        
        self.collider = Rect(1,1,1,1,opacity=0)
        
        self.transform = Transform(self)
        
        app.gameObjectList.append(self)
        
        # using underscores to try to prevent accidental overrides.
        self._destroyed_ = False
        
    def Update(self):
        # Override this function in the child class to add frame-by-frame behavior.
        pass
    
    def __backendUpdate__(self):
        if (self._destroyed_):
            self.visual.visible = False
            self.visual = None
            self.collider.visible = False
            self.collider = None
            self.transform = None
            app.gameObjectList.remove(self)
    
    def DestroySelf(self):
        self._destroyed_ = True
    
    @staticmethod
    def Destroy(gameObject):
        if (isinstance(gameObject, GameObject)):
            gameObject._destroyed_ = True
        else:
            raise TypeError(f"GameObject.Destroy() accepts type 'GameObject', not '{type(gameObject).__name__}'")
            


### Transform
# Every game object should automatically have its own 'Transform' component.
# Stores an object's Position (Vector2) and Scale (Vector2)
# Automatically updates the parent GameObject's visual & collider to the correct scale & position
class Transform:
    def __init__(self, gameObject):
        self.gameObject = gameObject
        self._position = Vector2(200, 200)
        self._scale = Vector2(1, 1)
        
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._position = value
        
        self.gameObject.visual.centerX = self.position.x
        self.gameObject.visual.centerY = self.position.y
        
        self.gameObject.collider.centerX = self.position.x
        self.gameObject.collider.centerY = self.position.y
        
    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self, value):
        ratioX = value.x / self._scale.x
        ratioY = value.y / self._scale.y
        self._scale = value
        
        self.gameObject.visual.width *= ratioX
        self.gameObject.visual.height *= ratioY
        
        self.gameObject.collider.width *= ratioX
        self.gameObject.collider.height *= ratioY
        
            
        
        
        
### AUDIO --- OKAY TO MODIFY!!
# This is just a 'storage' class for audio clips; instead of making them global or app variables.
# Set a clip inside the class, then access it as (eg. Audio.ATTACK)
class Audio:
    # Add audio clips here (eg. ATTACK = Sound('url'))
    pass

############### ENGINE ############### 


############### ENGINE METHODS ###############
    
# Linearly interpolate between two values at point 't'. ('t' is a value 0-1)
def Lerp(start, end, t):
    if (t == 0): return start
    elif (t < 0): t *= -1
    elif (t > 1): t = 1
    range = end - start
    increment = range * t
    value = start + increment
    return value
    
    
# Prevents the inputted value from going outside of the entered minimum and maximum.
def Clamp(value, max=999999999, min=-999999999):
    if (max < min):
        raise Exception(f"Clamped value's minimum ({min}) is larger than its maximum ({max})!")
        return
    
    if (value > max):
        value = max
    if (value < min):
        value = min
        
    return value
    
    
# Proportionally converts a range (oldMin to oldMax) to a new range (newMin to newMax)
def Remap(value, oldMin, oldMax, newMin, newMax):
    if (oldMin == oldMax):
        return newMin
        
    if (oldMin > oldMax):
        raise Exception(f"Remapped oldMin ({oldMin}) is greater than the oldMax ({oldMax})!")
    if (newMin > newMax):
        raise Exception(f"Remapped newMin ({newMin}) is greater than the newMax ({newMax})!")
        
    return (((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin

############### ENGINE METHODS ###############


############### ENGINE STARTUP ###############

app.background = gradient(rgb(101, 105, 110), rgb(120, 128, 140), start='bottom-right')

# list to store all GameObjects, used for running their Update() methods.
# Don't modify this. GameObjects automatically add themselves (as long as you call super().__init__())
app.gameObjectList = [] 

############### ENGINE STARTUP ###############





























### Change this value if you want; it is just frames per second.
app.stepsPerSecond = 60


### CROSSHAIR ###

class Crosshair(GameObject):
    def __init__(self):
        super().__init__()
        self.visual = Label(chr(0x1f540), 0, 0, size=24, font='symbols', fill='red', opacity=65)
        
        self.followSpeed = 35
        
    def Update(self):
        
        self.transform.position = Vector2(Lerp(self.transform.position.x, Input.mouse.x, self.followSpeed * Time.deltaTime), Lerp(self.transform.position.y, Input.mouse.y-0.75, self.followSpeed * Time.deltaTime))
        # self.transform.position = Vector2(Input.mouse.x, Input.mouse.y-0.75)
        
            
### CROSSHAIR ###
            
            
            
### ENEMY ###

class Enemy(GameObject):
    def __init__(self, spawnPosition):
        super().__init__()
        self.visual = Circle(0, 0, 30, fill='brown', border='black', borderWidth=5)
        self.collider = Circle(0, 0, 30, opacity=0)
        self.transform.position = spawnPosition
    
    
    def Update(self):
        if (Input.GetMouseDown(0)):
            if (self.collider.contains(Input.mouse.x, Input.mouse.y)):
                gameManager.enemyCount -= 1
                Circle(self.transform.position.x, self.transform.position.y, 10, fill='yellow').toBack()
                Circle(self.transform.position.x, self.transform.position.y, 16, fill='orange').toBack()
                self.DestroySelf()

### ENEMY ###



### GAME MANAGER ###

class GameManager(GameObject):
    def __init__(self):
        super().__init__()
        
        self.spawnCooldown = 2
        self.cooldownTimer = .5
        
        self.enemyCount = 0
        
    
    def Update(self):
        self.cooldownTimer -= Time.deltaTime
        if (self.cooldownTimer <= 0):
            self.cooldownTimer = self.spawnCooldown
            
            if (self.enemyCount < 10):
                position = Vector2(random.randint(0, 400), random.randint(0, 400))
                
                Enemy(position)
                self.enemyCount += 1
        
        
            
            

### GAME MANAGER ###



##### START #####

crosshair = Crosshair()

gameManager = GameManager()

##### START #####





























############### ENGINE FUNCTIONS ###############

def onStep():
    for gameObject in app.gameObjectList:
        gameObject.Update()
        gameObject.__backendUpdate__()
    
    
    Input.Update()
    Time.Update()
    
def onKeyPress(key):
    Input.keyDownList.append(key)
    
def onKeyRelease(key):
    Input.keyUpList.append(key)
    
def onKeyHold(keys):
    for key in keys:
        Input.keyHeldList.append(key)
        
def onMouseMove(x, y):
    Input.mouse.x = x
    Input.mouse.y = y
        
def onMouseDrag(x, y):
    Input.mouse.x = x
    Input.mouse.y = y
    
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
    
############### ENGINE FUNCTIONS ###############