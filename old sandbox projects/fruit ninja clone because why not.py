# October 2023

### CMUnity Engine -- v0.31 ###

import math
import time
import random
from enum import Enum

############### ENGINE ############### 

### Events
# First note: the event class is the only engine class that was not written by me; this stuff was a little too complicated. Credits to ChatGPT
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



# Everything below this line was hand-typed by me! Obviously I have to look up some syntax-related things that 
# I didn't initially know about Python, but the general functionality was developed by me (INSPIRED by Unity, of course).


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
    
    lastMouse = Vector2(200, 200)
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
# 'Time.deltaTime' will give you the time since the last frame. This allows for accurate timers, countdowns, animations, etc..
# 'Time.timeScale' scales the value of 'Time.deltaTime.' By default it is 1, but setting it to lower/higher values will simulate time moving slower/faster.
# 'Time.realDeltaTime' provides the time since the last frame, regardless of 'Time.timeScale.'
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
    
    def Awake(self):
        # Override this function to run code right when the instance is created
        pass
        
    def __init__(self):
        self.visual = Rect(1,1,1,1,opacity=0)
        
        self.collider = Rect(1,1,1,1,opacity=0)
        
        self.transform = Transform(self)
        
        app.gameObjectList.append(self)
        
        self._destroyed_ = False
        
        self.framesPassed = 0
        
        self.Awake()
        
    
    def __destroySelf__(self):
        self.visual.visible = False
        self.visual = None
        self.collider.visible = False
        self.collider = None
        self.transform = None
        app.gameObjectList.remove(self)
        
        
        
    def Start(self):
        # Override this function in the child class to run code one frame after the object is created
        pass
        
    def LateStart(self):
        # Override this function in the child class to run code two frames after the object is created
        pass
        
    def Update(self):
        # Override this function in the child class to add frame-by-frame behavior.
        pass
    
    def LateUpdate(self):
        # Override this function in the child class to run code every frame right after Update() runs
        pass
    
    def __backendUpdate__(self):
        if (self.framesPassed == 0):
            self.Start()
        if (self.framesPassed == 1):
            self.LateStart()
        self.framesPassed += 1
    
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
        
        
        
### RENDERER
# class Renderer:
#     def __init__(self):
#         self.sprite = Rect(0,0,1,1,opacity=0)
#         self.top = self.sprite.top
#         self.right = self.sprite.right
#         self.left = self.sprite.left
#         self.bottom = self.sprite.bottom
        
#         self.offscreen = False
#         self.unrendered = False
        
#     def Update(self):
#         self.offscreen = (self.top > 400 or self.bottom < 0 or self.left > 400 or self.right < 0)
        
#         if (not self.unrendered and self.offscreen):
#             self.unrendered = True
#             self.sprite.visible = False
            
#         if (not self.unrendered):
#             self.UpdateCaches()
            
        
#     def UpdateCaches(self):
        
    
        
    
    
    
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
# Create keyframes that control the values of different variables over time to forn animations!
# Keyframes store: (customKeyString, targetValue, timeInterval) --- "Keyframe('scale.x', 2, 5)" creates a keyframe:
# for key 'scale.x' that has a value of 2 at 5 seconds. (the key is just a string; it can be anything, but try to match it with the variable)
# To begin, declare a class that inherits 'Animation' --- "class A_PlayerIdle(Animation):"
# Create a 'Keyframes' function for the class; inside, return a list of all of your keyframes (and nothing else; only a single return statement)
# (Outside of 'Keyframes()'): Define a 'Keys():' method (must match name exactly) to add the references to the variables you want to modify.
# For example, if you want keyframes to modify something's 'transform.scale.x', make the key that those frames use = 'scale.x':
# Then, inside of the 'Keys()' method, assign "target.transform.scale.x = self.SetKey('scale.x')" (this is why you should name your keys correctly)
# To play an animation, call 'customAnimation.Play()'. To stop, call 'customAnimation.Stop()'. To make it loop, set 'customAnimation.looping = True'
# That was probably really confusing, so here is an example. You can also look at the animations in the "Open World Game" example below.

# Goal: Create an animation to make a player's 'scale.y' start at 1, increase to 2 in one second, then go back to 1 in the next second.
# Line 1:   class PlayerWalkAnimation(Animation):
# Line 2:       def Keyframes(self):
# Line 3:           return [Keyframe('scale.y', 1, 0), Keyframe('scale.y', 2, 1), Keyframe('scale.y', 1, 2)]
# Line 4:       def Keys(self):
# Line 5:           player.transform.scale.y = self.SetKey('scale.y')
class Animation:
    def Keyframes(self):
        # Override this in your child 'Animation' class with "return [Keyframes]" to set up the keyframes.
        raise Exception("'KeyframeList' method was not overriden in an 'Animation' child class!")
    
    def __init__(self):
        
        self.time = 0
        self.endTime = 0
        
        self.looping = False
        
        self.isPlaying = False
        self.keyframes = self.Keyframes()
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
    
        self.time += Time.realDeltaTime
        self.UpdateKeyframes(self.time, self.time - Time.realDeltaTime)
        
        if (self.time >= self.endTime):
            self.Stop()
            if (self.looping):
                self.Play()
                self.OnAnimationLooped.Invoke(self, None)
            
            self.Keys()
            self.OnAnimationEnd.Invoke(self, None)
        else:
            self.Keys()
            
    def Keys(self):
        # Override this in your child 'Animation' class to set the keys.
        raise Exception("'Keys' method was not overriden in an 'Animation' child class!")
       
    def Play(self, restart=False):
        if (restart):
            self.Stop()
        
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
            valueRange = targetKeyframe.value - activeKeyframe.value
            intervalTime = Remap01(unmappedIntervalTime, 0, range)
            
            value = 0
            if (targetKeyframe.easing == Easing.LINEAR):
                value = Lerp(activeKeyframe.value, targetKeyframe.value, intervalTime)
                
            elif (targetKeyframe.easing == Easing.SIN_IN):
                offset = 1 - math.cos((intervalTime * math.pi) / 2)
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.SIN_OUT):
                offset = math.sin((intervalTime * math.pi) / 2)
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.SIN_IN_OUT):
                offset = -(math.cos(math.pi * intervalTime) - 1) / 2
                value = activeKeyframe.value + offset * valueRange
                
            elif (targetKeyframe.easing == Easing.QUAD_IN):
                offset = intervalTime**2
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.QUAD_OUT):
                offset = 1-(1-intervalTime)**2
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.QUAD_IN_OUT):
                offset = 2 * intervalTime**2 if (intervalTime < 0.5) else 1-(-2 * intervalTime + 2)**2 / 2
                value = activeKeyframe.value + offset * valueRange
                
            elif (targetKeyframe.easing == Easing.CUBIC_IN):
                offset = intervalTime**3
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.CUBIC_OUT):
                offset = 1-(1-intervalTime)**3
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.CUBIC_IN_OUT):
                offset = 4 * intervalTime**3 if (intervalTime < 0.5) else 1-(-2 * intervalTime + 2)**3 / 2
                value = activeKeyframe.value + offset * valueRange
                
            elif (targetKeyframe.easing == Easing.QUART_IN):
                offset = intervalTime**4
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.QUART_OUT):
                offset = 1-(1-intervalTime)**4
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.QUART_IN_OUT):
                offset = 8 * intervalTime**4 if (intervalTime < 0.5) else 1-(-2 * intervalTime + 2)**3 / 2
                value = activeKeyframe.value + offset * valueRange
                
            elif (targetKeyframe.easing == Easing.BACK_IN):
                offset = (2.70158 * intervalTime**3) - (1.70158 * intervalTime**2)
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.BACK_OUT):
                offset = 1 + (2.70158 * (intervalTime-1)**3) + (1.70158 * (intervalTime-1)**2)
                value = activeKeyframe.value + offset * valueRange
            elif (targetKeyframe.easing == Easing.BACK_IN_OUT):
                offset = (2 * intervalTime)**2 * (7.18982 * intervalTime - 2.59491) / 2 if (intervalTime < 0.5) else ((2 * intervalTime - 2)**2 * (3.59491 * (2 * intervalTime - 2) + 2.59491) + 2) / 2
                value = activeKeyframe.value + offset * valueRange
                
            elif (targetKeyframe.easing == Easing.BOUNCE_OUT):
                n1 = 7.5625
                d1 = 2.75
                if (intervalTime < 1 / d1):
                    offset = n1 * intervalTime**2
                elif (intervalTime < 2 / d1):
                    intervalTime -= 1.5 / d1
                    offset = n1 * intervalTime**2 + 0.75
                elif (intervalTime < 2.5 / d1):
                    intervalTime -= 2.25 / d1
                    offset = n1 * intervalTime**2 + 0.9375
                else:
                    intervalTime -= 2.625 / d1
                    offset = n1 * intervalTime**2 + 0.984375
                value = activeKeyframe.value + offset * valueRange

            self.__currentKeyValueDict__[keyString] = value
                
    def SetKey(self, keyString):
        if (not keyString in self.__keyframeDict__):
            raise Exception(f"Inputted key '{key}' does not exist!")
        return self.__currentKeyValueDict__[keyString]
        
class Easing(Enum):
    LINEAR = 0
    
    SIN_IN = 14
    SIN_OUT = 15
    SIN_IN_OUT = 16
    
    QUAD_IN = 1
    QUAD_OUT = 2
    QUAD_IN_OUT = 3
    
    CUBIC_IN = 4
    CUBIC_OUT = 5
    CUBIC_IN_OUT = 6
    
    QUART_IN = 7
    QUART_OUT = 8
    QUART_IN_OUT = 9
    
    BACK_IN = 10
    BACK_OUT = 11
    BACK_IN_OUT = 12
    
    BOUNCE_OUT = 13
    
    
    
    
           
### KEYFRAME
class Keyframe:
    def __init__(self, key, value, time, easing = Easing.LINEAR):
        self.key = key
        self.value = float(value)
        self.time = float(time)
        
        self.index = None
        
        self.easing = easing
        
    def __str__(self):
        return f"Keyframe('{self.key}': {self.value}, at '{self.time}s')"
    def __repr__(self):
        return f"({self.value}, at {self.time} sec)" 
        
        
        

### BUTTON
# Quickly and easily create buttons that do things when you click, hold, and release them!
# Also have support for custom visuals when hovering, holding, and releasing.
# To make a button, create a class that inherits this one.
# Create your own visual for the button by overriding 'Awake(self)' and changing 'self.visual' and 'self.text'.
# Add your own functionality by simply overriding 'OnPressed()', 'OnHeld()', or 'OnReleased()'. 
# Any code that you place inside of these functions will run whenever the correlated event happens.
# There is also 'OnHeldVisual()', 'OnReleasedVisual()', and 'OnHoveredVisual()' which can help you make custom button animations.
class Button:
    def Awake(self):
        # Override this in a child class to initialize your button's visual and text
        pass

    def __init__(self):
        self.visual = Rect(200, 200, 100, 40, fill='snow', border='gainsboro', borderWidth=4, align='center')
        self.text = Label("Button", 200, 200, size=16)
        
        app.buttonList.append(self)
        
        self.hoverTint = 'black'
        self.hoverOpacity = 20
        
        self.holdTint = 'black'
        self.holdOpacity = 8
        
        self.isHovered = False # implement this
        
        self.Awake()
        
        self.hoverOverlay = Rect(self.visual.centerX, self.visual.centerY, self.visual.width, self.visual.height, align='center', fill=self.hoverTint, opacity=0)
        self.holdOverlay = Rect(self.visual.centerX, self.visual.centerY, self.visual.width, self.visual.height, align='center', fill=self.holdTint, opacity=0)

                
    def OnPressed(self):
        # Override this in a child class to specify what code runs when the button is clicked
        pass
        
    def OnHeld(self):
        # Override this in a child class to specify what code runs when the button is held down
        pass
        
    def OnReleased(self):
        # Override this in a child class to specify what code runs when the button is released
        pass
    
    def OnHeldVisual(self):
        # Override this if you want to make custom animations for the button when it is held down
        self.holdOverlay.opacity = self.holdOpacity
        self.hoverOverlay.opacity = 0
        
    def OnReleasedVisual(self):
        # Override this if you want to make custom animations for the button when it is released
        self.holdOverlay.opacity = 0
        
    def OnHoveredVisual(self):
        # Override this if you want to make custom animations for the button when it is hovered over
        self.hoverOverlay.opacity = self.hoverOpacity
        
    def OnUnhoveredVisual(self):
        # Override this if you want to make custom animations for the button when it is no longer hovered over.
        self.hoverOverlay.opacity = 0
        
        
        
    # Destroy the button (no longer visible & no more events)
    def DestroySelf(self):
        self.visual.visible = False
        self.text.visible = False
        self.hoverOverlay.visible = False
        self.holdOverlay.visible = False
        app.buttonList.remove(self)
        if (self in app.heldButtonList):
            app.heldButtonList.remove(self)
        
        




### DEBUG
# For now this only creates a real-time FPS display in the top-right corner
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

app.background = gradient('sienna', 'saddleBrown', 'sienna', start='bottom-right')


mainCamera = Camera()

# list to store all GameObjects, used for running their Update() methods.
# Don't modify this. GameObjects automatically add themselves (as long as you call super().__init__())
app.gameObjectList = [] 
app.destroyedGameObjectList = []

app.animationList = []

app.buttonList = []
app.heldButtonList = []

############### ENGINE STARTUP ###############























# Change this value if you want; it is just frames per second.
# The maximum is '240'
app.stepsPerSecond = 60



##### Place your code here!
##### NOTE: LEAVE "ENGINE FUNCTIONS" AT THE VERY BOTTOM OF THE SCRIPT!!!
##### You shouldn't have to touch anything inside the "ENGINE FUNCTIONS" if you use
##### the engine correctly. Read the documentation for 'GameObject' and 'Input' above.

class FruitType(Enum):
    COCONUT = 0
    WATERMELON = 1
    APPLE = 2
    CHERRY = 3
    ORANGE = 4
    BOMB = 5
    
    
class Splatter(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2
    
    
class Fruit(GameObject):
    def Awake(self):
        self.velocity = Vector2()
        self.gravity = -900
        
        self.sliceRequirement = SliceSpeed.SLOW
        
        self.splatter = Splatter.SMALL
        self.splatterColor = 'red'
        
        self.wasSliced = False
        
        self.isHazardous = False
        
        self.hurtPlayer = False
        
    def LateStart(self):
        @event_handler(player.OnGameLose)
        def Player_OnGameLose(sender, e):
            self.DestroySelf()
    
    def Update(self):
        self.velocity.y += self.gravity * Time.deltaTime
        
        self.transform.position.x += self.velocity.x * Time.deltaTime
        self.transform.position.y -= self.velocity.y * Time.deltaTime
        
        
        if (not gameManager.gameOver and not self.wasSliced and player.sliceState.value >= self.sliceRequirement.value and player.initialSlice.hitsShape(self.collider)):
            if (not self.isHazardous):
                gameManager.OnFruitSliced.Invoke(self, None)
                self.wasSliced = True
                splatter = None
                if (self.splatter == Splatter.SMALL):
                    splatter = SmallSplatter()
                elif (self.splatter == Splatter.MEDIUM):
                    splatter = MediumSplatter()
                elif (self.splatter == Splatter.LARGE):
                    splatter = LargeSplatter()
                splatter.visual.fill = self.splatterColor
                splatter.visual.rotateAngle = random.random() * 360
                splatter.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
                splatter.visual.toBack()
                self.DestroySelf()
            else:
                self.DestroySelf()
                gameManager.OnFruitFell.Invoke(self, None)
                    
            
        if (self.transform.position.y > 300 and not self.isHazardous):
            gameManager.OnFruitFell.Invoke(self, None)
            self.DestroySelf()
            


class Coconut(Fruit):
    def Awake(self):
        super().Awake()
        self.visual = Circle(0,0, 55, fill='peru', border='sienna', borderWidth=5.5)
        self.collider = Circle(0,0, 55, opacity=0)
        
        self.sliceRequirement = SliceSpeed.CRAZY
        
        self.splatter = Splatter.LARGE
        self.splatterColor = 'mintCream'
        
class Watermelon(Fruit):
    def Awake(self):
        super().Awake()
        self.visual = Oval(0,0, 100, 75, fill='lime', border='lightCoral', borderWidth=4.25)
        self.collider = Oval(0,0, 100, 75, opacity=0)
        
        self.sliceRequirement = SliceSpeed.HIGH
        
        self.splatter = Splatter.LARGE
        self.splatterColor = 'lightCoral'
        
class Orange(Fruit):
    def Awake(self):
        super().Awake()
        self.visual = Circle(0,0, 35, fill='orange', border='darkOrange', borderWidth=3.5)
        self.collider = Circle(0,0, 33, opacity=0)
        
        self.sliceRequirement = SliceSpeed.MEDIUM
        
        self.splatter = Splatter.MEDIUM
        self.splatterColor = 'darkOrange'
        
class Apple(Fruit):
    def Awake(self):
        super().Awake()
        self.visual = Circle(0,0, 32, fill='red', border='fireBrick', borderWidth=3.2)
        self.collider = Circle(0,0, 33, opacity=0)
        
        self.sliceRequirement = SliceSpeed.MEDIUM
        
        self.splatter = Splatter.MEDIUM
        self.splatterColor = 'gold'
        
class Cherry(Fruit):
    def Awake(self):
        super().Awake()
        self.visual = Circle(0,0, 15, fill='crimson', border='darkRed', borderWidth=1.5)
        self.collider = Circle(0,0, 15, opacity=0)
        
        self.sliceRequirement = SliceSpeed.SLOW
        
        self.splatter = Splatter.SMALL
        self.splatterColor = 'red'
        
class Bomb(Fruit):
    def Awake(self):
        super().Awake()
        self.visual = Group(
            Circle(0,0, 35, fill='gray', border='dimGray', borderWidth=3.5),
            Rect(0, 0, 9, 40, align='center', fill='fireBrick', rotateAngle=45), 
            Rect(0, 0, 9, 40, align='center', fill='fireBrick', rotateAngle=-45),
            )
        self.collider = Circle(0,0, 35, opacity=0)
        
        self.sliceRequirement = SliceSpeed.DANGER
        self.isHazardous = True
    

        

def SpawnFruit(fruitType, position, velocity):
    if (fruitType == FruitType.COCONUT):
        fruit = Coconut()
    elif (fruitType == FruitType.WATERMELON):
        fruit = Watermelon()
    elif (fruitType == FruitType.APPLE):
        fruit = Apple()
    elif (fruitType == FruitType.CHERRY):
        fruit = Cherry()
    elif (fruitType == FruitType.ORANGE):
        fruit = Orange()
    elif (fruitType == FruitType.BOMB):
        fruit = Bomb()
        
    fruit.transform.position = position
    fruit.velocity = velocity
    fruit.visual.rotateAngle = random.randrange(0, 360)
    
    return fruit
    
    
        
        
class SplatterObject(GameObject):
    def Start(self):
        self.fadeSpeed = 10
        self.fadeTimer = 3
        
        self.slideSpeed = 0.825
        
        self.velocity = Vector2()
    
    def Update(self):
        self.fadeTimer -= Time.deltaTime
        
        self.velocity.y += self.slideSpeed * Time.deltaTime
        
        self.transform.position.y += self.velocity.y * Time.deltaTime
        
        if (self.fadeTimer <= 0):
        
            self.visual.opacity = Clamp(self.visual.opacity - self.fadeSpeed * Time.deltaTime, min=0)
            if (self.visual.opacity == 0):
                self.DestroySelf()
            
        
    
    
        
class SmallSplatter(SplatterObject):
    def Awake(self):
        self.visual = Group(
            Circle(-9, 0, 7),
            Circle(10, 4, 3),
            Circle(8, 6.2, 11),
            Circle(-8, 10, 3.5),
            Circle(5, -8.7, 4),
            )
        self.visual.fill = 'red'
        self.visual.opacity = 40
        
        
class MediumSplatter(SplatterObject):
    def Awake(self):
        self.visual = Group(
            Circle(-9, 0, 16),
            Circle(-8, -5, 3),
            Circle(1, 10, 5),
            Circle(20, 2, 13),
            Circle(-20, 18, 8),
            Circle(-31, -12, 11),
            Circle(7, -22, 6),
            Circle(12, 23, 7),
            )
        self.visual.fill = 'red'
        self.visual.opacity = 40
        
        
class LargeSplatter(SplatterObject):
    def Awake(self):
        self.visual = Group(
            Circle(-11, 0, 20),
            Circle(-10, 0, 4),
            Circle(3, -16, 5),
            Circle(23, 3, 15),
            Circle(-24, -25, 10),
            Circle(-43, 14, 13),
            Circle(6, 26, 7),
            Circle(-15, 29, 8),
            Circle(14, -25, 6),
            )
        self.visual.width *= 1.1
        self.visual.height *= 1.1
        self.visual.fill = 'red'
        self.visual.opacity = 40
        



class GameManager(GameObject):
    def Awake(self):
        self.OnFruitFell = Event()
        self.OnFruitSliced = Event()
        self.pointVisual = Label(0, 15, 30, size=36, fill='white', align='left', font='sacramento', bold=True)
        
        self.fruitTypeList = [FruitType.COCONUT, FruitType.WATERMELON, FruitType.APPLE, FruitType.CHERRY, FruitType.ORANGE, FruitType.BOMB]
        
        self.fruitCooldownMax = 200 #200
        self.fruitCooldownMin = 100 #100
        
        self.fruitCooldownDecreaseRate = .75 #.75
        
        self.fruitCooldownTimer = 1
        
        self.fruitVelocityMax = Vector2(150, 890)
        self.fruitVelocityMin = Vector2(-150, 790)
        
        self.gameOver = True
    
    def Start(self):
        @event_handler(self.OnFruitSliced)
        def GameManager_OnFruitSliced(sender, e):
            self.pointVisual.value += 50
            self.pointVisual.left = 15
            Anim_TextPointsScored.Play(restart=True)
        
        @event_handler(self.OnFruitFell)
        def GameManager_OnFruitFell(sender, e):
            if (not sender.wasSliced and not sender.hurtPlayer and not self.gameOver):
                sender.hurtPlayer = True
                player.LoseLife()
                Anim_TextPointsLost.Play(restart=True)
        
    def Update(self):
        if (self.gameOver): return
        
        self.fruitCooldownTimer -= Time.deltaTime
        
        self.fruitCooldownMin = Clamp(self.fruitCooldownMin - self.fruitCooldownDecreaseRate * Time.deltaTime, min=18)
        self.fruitCooldownMax = Clamp(self.fruitCooldownMax - self.fruitCooldownDecreaseRate * Time.deltaTime * 2, min = 36)
        
        
        if (self.fruitCooldownTimer <= 0):
            position = Vector2()
            velocity = Vector2()
            
            position.y = 299
            
            position.x = random.random() * 380 - 190
            if (position.x < 0):
                 velocity.x = random.randrange(5, self.fruitVelocityMax.x)
            elif (position.x >= 0):
                velocity.x = random.randrange(self.fruitVelocityMin.x, -5)
            velocity.y = random.randrange(self.fruitVelocityMin.y, self.fruitVelocityMax.y)
            
            fruitType = self.fruitTypeList[random.randint(0, len(self.fruitTypeList)-1)]
            
            SpawnFruit(fruitType, position, velocity)
            self.fruitCooldownTimer = random.randrange(int(self.fruitCooldownMin), int(self.fruitCooldownMax)) / 100
            
            
class Anim_TextPointsScored(Animation):
    def Keyframes(self):
        return [
            Keyframe('size', 36, 0),
            Keyframe('size', 56, 0.08),
            Keyframe('size', 56, 0.1),
            Keyframe('size', 36, 0.3),
            
            Keyframe('rotate', 0, 0),
            Keyframe('rotate', 18, 0.045),
            Keyframe('rotate', -15, 0.09),
            Keyframe('rotate', 0, 0.2),
            
            Keyframe('r', 255, 0),
            Keyframe('r', 30, 0.1),
            Keyframe('r', 255, 0.3),
            
            Keyframe('b', 255, 0),
            Keyframe('b', 30, 0.066),
            Keyframe('b', 255, 0.3),
            ]
            
    def Keys(self):
        gameManager.pointVisual.size = self.SetKey('size')
        gameManager.pointVisual.fill = rgb(self.SetKey('r'), 255, self.SetKey('b'))
        gameManager.pointVisual.rotateAngle = self.SetKey('rotate')
        
class Anim_TextPointsLost(Animation):
    def Keyframes(self):
        return [
            Keyframe('size', 36, 0),
            Keyframe('size', 48, 0.04),
            Keyframe('size', 48, 0.08),
            Keyframe('size', 36, 0.2),
            
            Keyframe('rotate', 0, 0),
            Keyframe('rotate', 12, 0.04),
            Keyframe('rotate', -8, 0.08),
            Keyframe('rotate', 0, 0.16),
            
            Keyframe('g', 255, 0),
            Keyframe('g', 110, 0.05),
            Keyframe('g', 110, 0.15),
            Keyframe('g', 255, 0.2),
            
            Keyframe('b', 255, 0),
            Keyframe('b', 110, 0.05),
            Keyframe('b', 110, 0.15),
            Keyframe('b', 255, 0.2),
            ]
            
    def Keys(self):
        gameManager.pointVisual.size = self.SetKey('size')
        gameManager.pointVisual.fill = rgb(255, self.SetKey('g'), self.SetKey('b'))
        gameManager.pointVisual.rotateAngle = self.SetKey('rotate')
        
Anim_TextPointsScored = Anim_TextPointsScored()
Anim_TextPointsLost = Anim_TextPointsLost()
            
            
            
class SliceSpeed(Enum):
    NONE = 0
    SLOW = 20
    MEDIUM = 45
    HIGH = 60
    CRAZY = 70
    DANGER = 85
    
            
class Player(GameObject):
    def Awake(self):
        
        self.slashParticleList = []
        self.particleFadeSpeed = 500
        
        self.initialSlice = None
        
        self.sliceSpeed = 0
            
        self.sliceSpeedList = [SliceSpeed.NONE, SliceSpeed.SLOW, SliceSpeed.MEDIUM, SliceSpeed.HIGH, SliceSpeed.CRAZY, SliceSpeed.DANGER]
            
        self.sliceState = SliceSpeed.NONE
        self.sliceStateIndex = 0
        
        self.sliceMomentumBuffer = 0.1
        self.sliceMomentumTimer = 0
        
        self.livesLeft = 3
        
        self.OnGameLose = Event()
        
        border = Group(Rect(305, 25, 9.5, 27, align='center', fill='black', rotateAngle=45), Rect(305, 25, 9.5, 27, align='center', fill='black', rotateAngle=-45))
        border.width *= 1.25
        border.height *= 1.25
        self.healthOne = Group(Rect(305, 25, 6, 28, align='center', fill='dimGray', rotateAngle=45), Rect(305, 25, 6, 27, align='center', fill='dimGray', rotateAngle=-45))
        self.healthOneGroup = Group(border, self.healthOne)
        
        border = Group(Rect(340, 25, 9.5, 27, align='center', fill='black', rotateAngle=45), Rect(340, 25, 9.5, 28, align='center', fill='black', rotateAngle=-45))
        border.width *= 1.25
        border.height *= 1.25
        self.healthTwo = Group(Rect(340, 25, 6, 28, align='center', fill='dimGray', rotateAngle=45), Rect(340, 25, 6, 28, align='center', fill='dimGray', rotateAngle=-45))
        self.healthTwoGroup = Group(border, self.healthTwo)
        
        border = Group(Rect(375, 25, 9.5, 27, align='center', fill='black', rotateAngle=45), Rect(375, 25, 9.5, 28, align='center', fill='black', rotateAngle=-45))
        border.width *= 1.25
        border.height *= 1.25
        self.healthThree = Group(Rect(375, 25, 6, 28, align='center', fill='dimGray', rotateAngle=45), Rect(375, 25, 6, 28, align='center', fill='dimGray', rotateAngle=-45))
        self.healthThreeGroup = Group(border, self.healthThree)
    
    def LoseLife(self):
        if (self.livesLeft == 3):
            self.healthOne.fill = 'red'
        elif (self.livesLeft == 2):
            self.healthTwo.fill = 'red'
        elif (self.livesLeft == 1):
            self.healthThree.fill = 'red'
            self.LoseGame()
            
        self.livesLeft -= 1
        
        
        
    def LoseGame(self):
        Time.timeScale = 0.35
        Rect(0,0,400,400, opacity=50)
        Label("Game Over!", 200, 200, size=50, font='monospace', bold=True, fill='white')
        gameManager.gameOver = True
        Anim_GameLostSlowdown.Play()
        
        
        
    
    def Update(self):
        if (gameManager.gameOver): return
    
        if ((Input.GetMouse(0) or Input.GetKey('space')) and Input.lastMouse != Input.mouse):
            self.sliceSpeed = distance(Input.lastMouse.x, Input.lastMouse.y, Input.mouse.x, Input.mouse.y)
            if (self.sliceSpeed >= SliceSpeed.DANGER.value):
                self.sliceStateIndex = 5
                self.sliceMomentumTimer = self.sliceMomentumBuffer
            elif (self.sliceSpeed >= SliceSpeed.CRAZY.value and not self.sliceState.value > SliceSpeed.CRAZY.value):
                self.sliceStateIndex = 4
                self.sliceMomentumTimer = self.sliceMomentumBuffer
            elif (self.sliceSpeed >= SliceSpeed.HIGH.value and not self.sliceState.value > SliceSpeed.HIGH.value):
                self.sliceStateIndex = 3
                self.sliceMomentumTimer = self.sliceMomentumBuffer
            elif (self.sliceSpeed >= SliceSpeed.MEDIUM.value and not self.sliceState.value > SliceSpeed.MEDIUM.value):
                self.sliceStateIndex = 2
                self.sliceMomentumTimer = self.sliceMomentumBuffer
            elif (self.sliceSpeed >= SliceSpeed.SLOW.value and not self.sliceState.value > SliceSpeed.SLOW.value):
                self.sliceStateIndex = 1
                self.sliceMomentumTimer = self.sliceMomentumBuffer
                
            newParticle = Line(Input.lastMouse.x, Input.lastMouse.y, Input.mouse.x, Input.mouse.y, fill=rgb(143, 244, 247), opacity=100, lineWidth=12.5)
            if (self.sliceState == SliceSpeed.CRAZY or self.sliceState == SliceSpeed.DANGER):
                newParticle.opacity = 100 
                newParticle.lineWidth = 12.5
            elif (self.sliceState == SliceSpeed.HIGH):
                newParticle.opacity = 80
                newParticle.lineWidth = 10
            elif (self.sliceState == SliceSpeed.MEDIUM):
                newParticle.opacity = 64
                newParticle.lineWidth = 8
            elif (self.sliceState == SliceSpeed.SLOW):
                newParticle.opacity = 48
                newParticle.lineWidth = 6
            else:
                newParticle.opacity = 24
                newParticle.lineWidth = 3
                
            self.initialSlice = newParticle
                
            self.slashParticleList.append(newParticle)
                
                
        self.sliceMomentumTimer -= Time.deltaTime
        if (self.sliceMomentumTimer <= 0 and self.sliceStateIndex-1 >= 0):
            self.sliceStateIndex -= 1
            self.sliceMomentumTimer = self.sliceMomentumBuffer
                
        self.sliceState = self.sliceSpeedList[self.sliceStateIndex]
        
        
        
        for particle in self.slashParticleList:
            particle.opacity = Clamp(particle.opacity - self.particleFadeSpeed * Time.deltaTime, min=0)
            particle.lineWidth = Clamp(particle.lineWidth - self.particleFadeSpeed / 8 * Time.deltaTime, min=0.001)
            if (particle.opacity == 0):
                self.slashParticleList.remove(particle)
                particle.visible = False
                continue
            
            if (self.sliceState == SliceSpeed.DANGER):
                particle.fill = rgb(255, 14, 39)
            elif (self.sliceState == SliceSpeed.CRAZY):
                particle.fill = rgb(255, 60, 126)
            elif (self.sliceState == SliceSpeed.HIGH):
                particle.fill = rgb(152, 51, 163)
            elif (self.sliceState == SliceSpeed.MEDIUM):
                particle.fill = rgb(143, 82, 217)
            elif (self.sliceState == SliceSpeed.SLOW):
                particle.fill = rgb(82, 176, 217)
            else:
                particle.fill = rgb(143, 244, 247)
                
                
                
class Anim_GameLostSlowdown(Animation):
    def Keyframes(self):
        return [
            Keyframe('timeScale', 1, 0),
            Keyframe('timeScale', 0.15, 0.75, Easing.SIN_OUT),
            Keyframe('timeScale', 0.15, 4),
            Keyframe('timeScale', 1, 5, Easing.QUAD_IN_OUT),
            ]
            
    def Keys(self):
        Time.timeScale = self.SetKey('timeScale')
        
Anim_GameLostSlowdown = Anim_GameLostSlowdown()
            
            

gameManager = GameManager()

player = Player()

class TutorialButton(Button):
    def Awake(self):
        self.text.value = "Play"
        self.text.size = 36
        self.text.fill = 'darkGreen'
        self.text.bold = True
        
        self.visual.fill = 'lime'
        self.visual.border = 'green'
        
        self.visual.width = 200
        self.visual.height = 65
        
        self.visual.centerX = 200
        self.visual.centerY = 280
        self.text.centerY = 280
        
    def OnReleased(self):
        gameManager.gameOver = False
        tutorialScreen.visible = False
        self.DestroySelf()
        
tutorialScreen = Group(
    Rect(0,0, 400, 400, opacity=60),
    Rect(0, 75, 400, 135, opacity=30),
    
    Label("Slice the fruit before they fall!", 200, 95, size=20, fill='white'),
    Label("Every fruit requires a certin slice speed;", 200, 128, size=20, fill='white'),
    Label("your mouse trail indicates this.", 200, 152, size=20, fill='white'),
    Label("Don't slice the bombs or you will explode!", 195, 185, size=20, fill='white'),
    )
    
TutorialButton()



























############### ENGINE FUNCTIONS ###############

def onStep():
    for gameObject in app.gameObjectList:
        gameObject.__backendUpdate__()
        gameObject.Update()
        gameObject.LateUpdate()
        if (gameObject._destroyed_):
            app.destroyedGameObjectList.append(gameObject)
            
    for gameObject in app.destroyedGameObjectList:
        gameObject.__destroySelf__()
        
        app.destroyedGameObjectList.clear()
        
    for animation in app.animationList:
        animation.Update()
        
    for button in app.heldButtonList:
        button.OnHeld()
        button.OnHeldVisual()
    
    
    Input.Update()
    Input.lastMouse = Vector2(Input.mouse.x, Input.mouse.y)
    
    Time.Update()
    
def onKeyPress(key):
    Input.keyDownList.append(key)
    
def onKeyRelease(key):
    Input.keyUpList.append(key)
    
def onKeyHold(keys):
    for key in keys:
        Input.keyHeldList.append(key)
        
def onMouseMove(x, y):
    Input.lastMouse = Vector2(Input.mouse.x, Input.mouse.y)
    Input.mouse = Vector2(x, y)
    
    for button in app.buttonList:
        if (button.visual.hits(x, y)):
            button.OnHoveredVisual()
        else:
            button.OnUnhoveredVisual()
        
def onMouseDrag(x, y):
    Input.lastMouse = Vector2(Input.mouse.x, Input.mouse.y)
    Input.mouse = Vector2(x, y)
    
    for button in app.buttonList:
        if (button.visual.hits(x, y)):
            button.OnHoveredVisual()
        else:
            button.OnUnhoveredVisual()
    
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
        
    for button in app.buttonList:
        if (button.visual.hits(x, y)):
            button.OnPressed()
            if (not button in app.heldButtonList):
                app.heldButtonList.append(button)
    
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
        
    for button in app.buttonList:
        if (button in app.heldButtonList):
            app.heldButtonList.remove(button)
            button.OnReleasedVisual()
            if (button.visual.hits(x, y)):
                button.OnReleased()
    
############### ENGINE FUNCTIONS ###############