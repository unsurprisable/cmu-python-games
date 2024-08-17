# October 2023

import math
import time

# i cant do math...
# project on hold until i figure out how to rotate a velocity in a perfect circle

############### ENGINE ############### 

### Events
# First note: this is the only engine class that was not written by me; this stuff was a little too complicated. Credits to ChatGPT
# To create an event, simply define a variable of type 'Event()' --- "OnExampleEvent = Event()"
# To add a listener to that event, create a method using the decorator 'event_handler' --- "@event_handler(OnExampleEvent)"
# Every method that is added as a listener to an event will be executed when that event is invoked
# To invoke an event, simply use the syntax "OnExampleEvent.Invoke(self, 'anyCustomDataToPassToTheListeners')"
class Event:
    def __init__(self):
        self.handlers = []
        
    def Subscribe(self, handler):
        self.handlers.append(handler)
        
    def Unsubscribe(self, handler):
        self.handlers.remove(handler)
        
    def Invoke(self, *args, **kwargs):
        #print(f"Invoke ran! 'self.handlers' = {self.handlers}")
        for handler in self.handlers:
            #print(f"Invoking handler: {handler}")
            try:
                handler(*args, **kwargs)
            except Exception as e:
                print(f"Handler {handler} raised an exception: {e}")
            
def event_handler(event):
    def decorator(func):
        event.Subscribe(func)
        #print(f"{func.__name__} subscribed: \n{event} = {event.handlers}\n")
        return func
        
    return decorator



### Vector2
# Stores x, y, and magnitude components.
# When passing a vector as an argument, its own reference is passed in---not a copy of it
# Supports (get; & set;) of the x, y, and magnitude; everything updates itself accordingly.
# Check the bottom of this class for additional functionality.
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y
        self._magnitude = math.sqrt(self.x ** 2 + self.y ** 2)
        
        self.OnModifiedX = Event()
        self.OnModifiedY = Event()

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
        if (newX != self._x):
            lastValue = Vector2(self._x, self._y)
            self._x = newX
            self.UpdateMagnitude()
            self.OnModifiedX.Invoke(self, lastValue)
        
        
    @property
    def y (self):
        return self._y
    @y.setter
    def y (self, newY):
        if (newY != self._y):
            lastValue = Vector2(self._x, self._y)
            self._y = newY
            self.UpdateMagnitude()
            self.OnModifiedY.Invoke(self, lastValue)
        
        
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
        self = Vector2(self._x, self._y)
        
    def UpdateComponents(self, change):
        self._x *= change
        self._y *= change
        self = Vector2(self._x, self._y)
        
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
# Also, if your new class is going to use its own '__init__()', make sure to still call 'super().__init__()' inside of it. 
# !!! IF YOUR CLASS IS NOT UPDATING, MAKE SURE YOU DID THIS ^^^^^ !!!
# Make sure to actually instantiate the class! Otherwise, nothing will happen.
# No need to do anything with the 'onStep' function; use this instead to stay organized!
# To make a GameObject stop updating, USE: "gameObjectInstance.DestroySelf()" or "GameObject.Destroy(targetGameObject)"
# Every game object has its own '.visual' (sprite), '.collider' (hitbox), and '.transform' (stores position & scale)
# The transform is integrated so that the 'visual' & 'collider' will update alongside it.
# Note that the transform's coordinate system is SEPARATE from the canvas coordinate system:
# A transform of (0, 0) will render a visual at the canvas point (200, 200):
# --> (transform coordinate) = (a canvas coordinate) - 200
class GameObject:
    def __init__(self):
        self.visual = Rect(1,1,1,1,opacity=0)
        
        self.collider = Rect(1,1,1,1,opacity=0)
        
        self.transform = Transform(self)
        
        app.gameObjectList.append(self)
        
        self._destroyed_ = False
        
        self.lateStartRan = False
        
    def LateStart(self):
        # Override this function in the child class to run code one frame after the object is created
        pass
        
    def Update(self):
        # Override this function in the child class to add frame-by-frame behavior.
        pass
    
    def __backendUpdate__(self):
        if (not self.lateStartRan):
            self.LateStart()
            self.lateStartRan = True
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
        self._position = Vector2(0, 0)
        self._scale = Vector2(1, 1)
        self._offset = Vector2(200, 200)
        
        self.PositionSubscriptions()
        self.ScaleSubscriptions()
        self.OffsetSubscriptions()
        
    
    def PositionSubscriptions(self):
        @event_handler(self._position.OnModifiedX)
        def Position_OnModifiedX(sender, e):
            self.UpdateVisuals()
        @event_handler(self._position.OnModifiedY)
        def Position_OnModifiedY(sender, e):
            self.UpdateVisuals()
    
    def ScaleSubscriptions(self):
        @event_handler(self._scale.OnModifiedX)
        def Scale_OnModifiedX(sender, e):
            self.UpdateScales(e, self._scale)
        @event_handler(self._scale.OnModifiedY)
        def Scale_OnModifiedY(sender, e):
            self.UpdateScales(e, self._scale)
    
    def OffsetSubscriptions(self):
        @event_handler(self._offset.OnModifiedX)
        def Offset_OnModifiedX(sender, e):
            self.UpdateVisuals()
        @event_handler(self._offset.OnModifiedY)
        def Offset_OnModifiedY(sender, e):
            self.UpdateVisuals()
        
        
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._position = value
        self.UpdateVisuals()
        self.PositionSubscriptions()
        
    @property
    def offset(self):
        return self._offset
    @offset.setter
    def offset(self, newOffset):
        self._offset = newOffset
        self.UpdateVisuals()
        self.OffsetSubscriptions()
        
    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self, value):
        lastValue = self._scale
        newValue = value
        self._scale = value
        self.UpdateScales(lastValue, newValue)
        self.ScaleSubscriptions()
        
        
            
    def UpdateScales(self, lastValue, newValue):
        
        ratioX = newValue.x / lastValue.x
        ratioY = newValue.y / lastValue.y

        self.gameObject.visual.width *= ratioX
        self.gameObject.visual.height *= ratioY
        
        self.gameObject.collider.width *= ratioX
        self.gameObject.collider.height *= ratioY
        
    def UpdateVisuals(self):
        self.gameObject.visual.centerX = self.position.x + self.offset.x
        self.gameObject.visual.centerY = self.position.y + self.offset.y
        
        self.gameObject.collider.centerX = self.position.x + self.offset.x
        self.gameObject.collider.centerY = self.position.y + self.offset.y 
        
        
        
### CAMERA
# Acts like a camera! (ONLY affects GameObjects !!!)
# Move the camera by modifying 'mainCamera.position' (Vector2)
# Automatically changes the canvas position that GameObjects' '.visual' and '.collider' are rendered to, simulating a moving camera
# This will NOT work on any shapes that are not specifically under those two properties of a GameObject.
# The coordinates of this are exactly like a transform: '.position of (0, 0)' equals 'canvas point of (200, 200)' 
# If you don't want to utilize a dynamic camera, simply don't mess with 'mainCamera.position'!
# To create UI (constant canvas position), simply don't make the shape under 'gameObjectInstance.visual' or 'gameObjectInstance.collider'
class Camera:
    def __init__(self):
        self._position = Vector2(0, 0)
        self.Subscriptions()
        
    def UpdateOffsets(self):
        for gameObject in app.gameObjectList:
            if (isinstance(gameObject, Camera)): return
        
            gameObject.transform.offset.x = 200-self.position.x
            gameObject.transform.offset.y = 200-self.position.y
    
    def Subscriptions(self):
        @event_handler(self._position.OnModifiedX)
        def Position_OnModifiedX(sender, e):
            self.UpdateOffsets()
        @event_handler(self._position.OnModifiedY)
        def Position_OnModifiedY(sender, e):
            self.UpdateOffsets()

                
    
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, newPos):
        if (newPos != self._position):
            self._position = newPos
            self.Subscriptions()



### ANIMATION
# Create keyframes that control the values of different variables over time to create animations!
# Keyframes store: (customKeyString, targetValue, timeInterval) --- "Keyframe('scale.x', 2, 5)" creates a keyframe:
# for key 'scale.x' that has a value of 2 at 5 seconds. (the key is just a string; it can be anything, but try to match it with the variable)
# To begin, declare a class that inherits 'Animation' --- "class A_PlayerIdle(Animation):"
# Create an '__init__' function for the class, and inside declare 'super().__init__()' and pass in a list of keyframes into that '__init__()' method
# (Outside of __init__()): Define a 'Keys():' method (must match name exactly) to add the references to the variables you want to modify.
# For example, if you want keyframes to modify something's 'transform.scale.x', make the key that those frames use = 'scale.x':
# Then, inside of the 'Keys()' method, assign "target.transform.scale.x = self.GetKeyValue('scale.x')" (this is why you should name your keys correctly)
# To play an animation, call 'customAnimation.Play()'. To stop, call 'customAnimation.Stop()'. To make it loop, set 'customAnimation.looping = True'
# That was probably really confusing, so here is an example. You can also look at the animations in the "Open World Game" example below.

# Goal: Create an animation to make a player's 'scale.y' start at 1, increase to 2 in one second, then go back to 1 in the next second.
# Line 1:   class PlayerWalkAnimation(Animation):
# Line 2:       def __init__(self):
# Line 3:           super().__init__([Keyframe('scale.y', 1, 0), Keyframe('scale.y', 2, 1), Keyframe('scale.y'), 1, 2])
# Line 4:       def Keys(self):
# Line 5:           player.transform.scale.y = self.GetKeyValue('scale.y')
class Animation:
    def __init__(self, keyframeList):
        
        self.time = 0
        self.endTime = 0
        
        self.looping = False
        
        self.isPlaying = False
        self.keyframes = keyframeList
        self.__keyframeDict__ = self.OrganizeKeyframes()
        self.__activeKeyframeDict__ = self.InitializeActiveKeyframesDict()
        self.__targetKeyframeDict__ = self.InitializeTargetKeyframesDict()
        self.__currentKeyValueDict__ = self.InitializeCurrentKeyValuesDict()
        
        self.OnAnimationPlay = Event()
        self.OnAnimationStop = Event()
        self.OnAnimationLooped = Event()
        self.OnAnimationEnd = Event()
        
        app.animationList.append(self)
        
    def Update(self):
        if (not self.isPlaying): return
    
        self.time += Time.deltaTime
        self.UpdateKeyframes(self.time, self.time - Time.deltaTime)
        
        if (self.time >= self.endTime):
            self.Stop()
            if (self.looping):
                self.Play()
                self.OnAnimationLooped.Invoke(self, None)
            
            self.OnAnimationEnd.Invoke(self, None)
            
        self.Keys()
            
    def Keys(self):
        raise Exception("'Keys' method was not overriden in an 'Animation' child class!")
       
    def Play(self):
        
        self.isPlaying = True
        
        self.OnAnimationPlay.Invoke(self, None)
   
    def Stop(self):
        self.time = 0
        self.isPlaying = False
        self.__activeKeyframeDict__ = self.InitializeActiveKeyframesDict()
        self.__targetKeyframeDict__ = self.InitializeTargetKeyframesDict()
        self.__currentKeyValueDict__ = self.InitializeCurrentKeyValuesDict()
        
        self.OnAnimationStop.Invoke(self, None)
   
    def OrganizeKeyframes(self):
        organizedKeyframes = {}
        for keyframe in self.keyframes:
            # Sets 'self.endTime' to the greatest time interval out of all keyframes
            if (keyframe.time > self.endTime):
                self.endTime = keyframe.time
            if (not keyframe.key in organizedKeyframes):
                organizedKeyframes[keyframe.key] = [keyframe]
            else:
                organizedKeyframes[keyframe.key].append(keyframe)
        
        # Finds the lowest time valued keyframe for each key, and moves it to its respective place in order of time.
        for keyString in organizedKeyframes:
            keyValue = organizedKeyframes[keyString]
            
            keyframeList = keyValue.copy()
            for i in range(len(keyValue)): # iterate for the amount of keyframes a key holds
                lowestTimeKeyframe = None
                for keyframe in keyframeList:
                    if (lowestTimeKeyframe == None):
                        lowestTimeKeyframe = keyframe
                    else:
                        if (keyframe.time < lowestTimeKeyframe.time):
                            lowestTimeKeyframe = keyframe
                keyframeList.remove(lowestTimeKeyframe)
                keyValue.remove(lowestTimeKeyframe)
                keyValue.insert(i, lowestTimeKeyframe)
                lowestTimeKeyframe.index = i
                
        return organizedKeyframes
        
    def InitializeActiveKeyframesDict(self):
        startingKeyframeDict = {}
        for keyString in self.__keyframeDict__:
            keyValue = self.__keyframeDict__[keyString]
            startingKeyframeDict[keyString] = keyValue[0]
        return startingKeyframeDict
        
    def InitializeCurrentKeyValuesDict(self):
        startingKeyframeDict = {}
        for keyString in self.__keyframeDict__:
            keyValue = self.__keyframeDict__[keyString]
            startingKeyframeDict[keyString] = keyValue[0].value
        return startingKeyframeDict
    
    def InitializeTargetKeyframesDict(self):
        targetKeyframeDict = {}
        for keyString in self.__keyframeDict__:
            keyValue = self.__keyframeDict__[keyString]
            targetKeyframeDict[keyString] = keyValue[1]
        return targetKeyframeDict
            
    def UpdateKeyframes(self, time, lastTime):
        for keyString in self.__keyframeDict__:
            activeKeyframe = self.__activeKeyframeDict__[keyString]
            targetKeyframe = self.__targetKeyframeDict__[keyString]
            
            if (targetKeyframe.time >= lastTime and targetKeyframe.time <= time):
                activeKeyframe = targetKeyframe
                if (targetKeyframe.index < len(self.__keyframeDict__[keyString]) - 1):
                    targetKeyframe = self.__keyframeDict__[keyString][targetKeyframe.index + 1]
                
                self.__activeKeyframeDict__[keyString] = activeKeyframe
                self.__targetKeyframeDict__[keyString] = targetKeyframe
                
            unmappedIntervalTime = self.time - activeKeyframe.time
            range = targetKeyframe.time - activeKeyframe.time
            intervalTime = Remap01(unmappedIntervalTime, 0, range)
            self.__currentKeyValueDict__[keyString] = Lerp(activeKeyframe.value, targetKeyframe.value, intervalTime)
                
    def GetKeyValue(self, keyString):
        if (not keyString in self.__keyframeDict__):
            raise Exception(f"Inputted key '{key}' does not exist!")
        return self.__currentKeyValueDict__[keyString]
           
### KEYFRAME
class Keyframe:
    def __init__(self, key, value, time):
        self.key = key
        self.value = float(value)
        self.time = float(time)
        
        self.index = None
        
    def __str__(self):
        return f"Keyframe('{self.key}': {self.value}, at '{self.time}s')"
    def __repr__(self):
        return f"({self.value}, at {self.time} sec)" 
                
                
        
### AUDIO --- OKAY TO MODIFY!!
# This is just a 'storage' class for audio clips; instead of making them global or app variables.
# Set a clip inside the class, then access it as (eg. Audio.ATTACK)
class Audio:
    # Add audio clips here (eg. ATTACK = Sound('url'))
    pass



### DEBUG
# For now, creates a real-time FPS display in the top-right corner
# To enable, just make an instance of it somewhere in your code: "debug = Debug()"
class Debug(GameObject):
    def __init__(self):
        super().__init__()
        self.display = Label(f"{app.stepsPerSecond} FPS", 360, 10, size=20, fill='lime', bold=True, border='black', borderWidth=.25)
        self.timer = 0
        self.sampleLength = 0.25
        self.counter = 0

    def Update(self):
        self.display.toFront()
        self.display.right = 395
        
        self.timer += Time.deltaTime
        self.counter += 1
        
        if (self.timer >= self.sampleLength):
            fps = Clamp(self.counter / self.sampleLength, max=app.stepsPerSecond)
            self.display.value = f"{int(fps)} FPS"
            self.timer = 0
            self.counter = 0

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
        tempMax = oldMin
        oldMin = oldMax
        oldMax = tempMax
    if (newMin > newMax):
        tempMax = newMin
        newMin = newMax
        newMax = tempMax
        
    return (((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
    
    
# Proportionally converts a range (oldMin to oldMax) to a range of 0-1
def Remap01(value, oldMin, oldMax):
    if (oldMin == oldMax):
        return 0
        
    if (oldMin > oldMax):
        tempMax = oldMin
        oldMin = oldMax
        oldMax = tempMax
        
    return ((value - oldMin) / (oldMax - oldMin))

############### ENGINE METHODS ###############


############### ENGINE STARTUP ###############

app.background = gradient(rgb(101, 105, 110), rgb(120, 128, 140), start='bottom-right')

mainCamera = Camera()

# list to store all GameObjects, used for running their Update() methods.
# Don't modify this. GameObjects automatically add themselves (as long as you call super().__init__())
app.gameObjectList = [] 

app.animationList = []

############### ENGINE STARTUP ###############





























debug = Debug()

# Change this value if you want; it is just frames per second.
# The maximum is '240'
app.stepsPerSecond = 240

class Player(GameObject):
    def __init__(self):
        super().__init__()
        
        self.visual = Circle(0,0, 10, fill='dodgerBlue', border='black')
        self.collider = Circle(0,0, 5, opacity=0)
        
        self.transform.position = Vector2(0, -150)
        
        self.velocity = Vector2(50, 0)
        self.hookedVelocity = Vector2()
        
        self.cameraScrollSpeed = 50
        self.verticalCameraSpeed = 5
        
        self.gravity = -750
        self.terminalVelocity = -575
        
        self.knobsInRangeList = []
        self.nearestKnob = None
        self.OnNewNearestKnob = Event()
        
        self.isHooked = False
        self.hookedKnob = None
        self.hookVisual = Line(0,0,0,0, lineWidth=5, dashes=(7, 4), fill='white', opacity=0)
        
        self.hookedRotationSpeed = 0.5
        self.hookedRotationAngle = 0
        
        
        
    def LateStart(self):
        
        @event_handler(knobSpawner.OnKnobCreated)
        def KnobSpawner_OnKnobCreated(sender, e):
            @event_handler(e.OnPlayerEntered)
            def Knob_OnPlayerEntered(sender, e):
                self.knobsInRangeList.append(sender)
                sender.visual.children[1].fill = 'yellow'
                
            @event_handler(e.OnPlayerExited)
            def Knob_OnPlayerExited(sender, e):
                if (sender == self.nearestKnob):
                    self.nearestKnob = None
                self.knobsInRangeList.remove(sender)
                sender.visual.children[1].fill = 'red'
        
    def Update(self):
        self.velocity.y = Clamp(self.velocity.y + self.gravity * Time.deltaTime, min=self.terminalVelocity)
        
        if (Input.GetKeyDown('space')):
            self.velocity.y = 300
            
        if (Input.GetMouseDown(0) and self.nearestKnob != None):
            self.hookedKnob = self.nearestKnob
            self.isHooked = True
            self.hookVisual.opacity = 100
            self.hookedRotationAngle = math.atan((self.transform.position.y - self.hookedKnob.transform.position.y) / (self.transform.position.x - self.hookedKnob.transform.position.x))
            self.hookedVelocity = Vector2(self.velocity.x, self.velocity.y)
        if (Input.GetMouseUp(0) and self.isHooked):
            self.hookedKnob = None
            self.isHooked = False
            self.hookVisual.opacity = 0
            self.velocity = self.hookedVelocity
        
        if (self.isHooked):
            
            self.hookVisual.x1 = self.visual.centerX
            self.hookVisual.y1 = self.visual.centerY
            self.hookVisual.x2 = self.hookedKnob.visual.centerX
            self.hookVisual.y2 = self.hookedKnob.visual.centerY
            
            vectorToKnob = Vector2.angleTo(
                self.transform.position.x, self.transform.position.y,
                self.hookedKnob.transform.position.x, self.hookedKnob.transform.position.y
            )
            
            vectorToKnob.x *= self.hookedKnob.distanceFromPlayer
            vectorToKnob.y *= self.hookedKnob.distanceFromPlayer
            
            self.hookedVelocity.x += vectorToKnob.x * Time.deltaTime
            self.hookedVelocity.y -= vectorToKnob.y * Time.deltaTime
            
            self.hookedVelocity.magnitude = self.velocity.magnitude
            
            # angleChange = self.hookedRotationSpeed * Time.deltaTime
            # finalAngle = self.hookedRotationAngle - angleChange
            # rotatedDirection = Vector2(
            #     (self.velocity.x * math.cos(finalAngle) - self.velocity.y * math.sin(finalAngle)) + self.hookedKnob.distanceFromPlayer,
            #     self.hookedKnob.distanceFromPlayer - (self.velocity.x * math.sin(finalAngle) + self.velocity.y * math.cos(finalAngle))
            #     )
            
            # rotationSpeed = self.hookedKnob.distanceFromPlayer
            
            # if (self.hookedVelocity.x < 0):
            #     self.hookedVelocity.x += rotationSpeed * Time.deltaTime
            # else:
            #     self.hookedVelocity.x -= rotationSpeed * Time.deltaTime
            # if (self.hookedVelocity.y < 0):
            #     self.hookedVelocity.y += rotationSpeed * Time.deltaTime
            # else:
            #     self.hookedVelocity.y -= rotationSpeed * Time.deltaTime
                
            
            # self.velocity.x = rotatedDirection.x
            # self.velocity.y = rotatedDirection.y
            
            self.transform.position.x += self.hookedVelocity.x * Time.deltaTime
            self.transform.position.y -= self.hookedVelocity.y * Time.deltaTime
            
        if (not self.isHooked):
            self.transform.position.x += self.velocity.x * Time.deltaTime
            self.transform.position.y -= self.velocity.y * Time.deltaTime
        
        
        #mainCamera.position.x += self.cameraScrollSpeed * Time.deltaTime
        mainCamera.position.x = Lerp(mainCamera.position.x, self.transform.position.x, self.verticalCameraSpeed * Time.deltaTime)
        mainCamera.position.y = Lerp(mainCamera.position.y, self.transform.position.y, self.verticalCameraSpeed * Time.deltaTime)
        
        oldNearestKnob = self.nearestKnob
        for knob in self.knobsInRangeList:
            if (self.nearestKnob == None):
                self.nearestKnob = knob
            
            if (knob.distanceFromPlayer < self.nearestKnob.distanceFromPlayer):
                self.nearestKnob = knob
        if (self.nearestKnob != oldNearestKnob):
            self.OnNewNearestKnob.Invoke(self, self.nearestKnob)
        

                
        
player = Player()

class KnobSpawner(GameObject):
    def __init__(self):
        super().__init__()
        self.OnKnobCreated = Event()
    
    def LateStart(self):
        self.SpawnKnob(Vector2(200, -100))
        self.SpawnKnob(Vector2(250, 125))
        self.SpawnKnob(Vector2(300, 0))
        self.SpawnKnob(Vector2(450, 150))
    
    def SpawnKnob(self, position):
        knob = Knob(position)
        self.OnKnobCreated.Invoke(self, knob)
        
knobSpawner = KnobSpawner()

class Knob(GameObject):
    def __init__(self, position):
        super().__init__()
        
        self.visual = Group(
            Circle(0,0, 18, fill='gray'),
            Circle(0,0, 9, fill='red', border='black')
            )
        self.visual.toBack()
        self.hitboxRadius = 115
        self.collider = Circle(0,0, self.hitboxRadius-5, fill='gray', border='darkGray', opacity=25)
        
        self.transform.position = position
        
        self.OnPlayerEntered = Event()
        self.OnPlayerExited = Event()
        
        self.playerInside = False
        self.distanceFromPlayer = 0
        
    def LateStart(self):
        @event_handler(player.OnNewNearestKnob)
        def Player_OnNewNearestKnob(sender, e):
            if (self == e):
                self.visual.children[1].fill = 'lime'
            elif (self.playerInside):
                self.visual.children[1].fill = 'yellow'
            else:
                self.visual.children[1].fill = 'red'
        
    def Update(self):
        self.distanceFromPlayer = distance(player.transform.position.x, player.transform.position.y, self.transform.position.x, self.transform.position.y)
        
        if (self.distanceFromPlayer <= self.hitboxRadius and not self.playerInside):
            self.playerInside = True
            self.OnPlayerEntered.Invoke(self, None)
        
        if (self.distanceFromPlayer > self.hitboxRadius and self.playerInside):
            self.playerInside = False
            self.OnPlayerExited.Invoke(self, None)
        
        



























############### ENGINE FUNCTIONS ###############

def onStep():
    for gameObject in app.gameObjectList:
        gameObject.Update()
        gameObject.__backendUpdate__()
        
    for animation in app.animationList:
        animation.Update()
    
    
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
    Input.mouse.x = y
    
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