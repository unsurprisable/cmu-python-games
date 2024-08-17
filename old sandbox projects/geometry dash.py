import math
import time
from enum import Enum



##### EXTERNAL RESOURCES (CREDITED) #####
class Audio:
    # Songs
    STEREO_MADNESS = Sound('cmu://682887/25287381/Stereo+Madness.mp3')      # "Stereo Madness" by Forever Bound
    BASE_AFTER_BASE = Sound('cmu://682887/25288663/Base+After+Base.mp3')    # "Base After Base" by DJVI
    

class Images:
    # Backgrounds - ALL by: Robtop Games
    BACKGROUND_1 = 'cmu://682887/25288817/Default+GD+Background.png'
    
    # Portals - ALL by: Robtop Games
    YELLOW_PORTAL = 'cmu://682887/25544743/yellow_portal_single.png'    
    BLUE_PORTAL = 'cmu://682887/25544898/blue_portal_single.png'
    
    
    

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
    timeScale = 1
    deltaTime = 0.0
    
    @staticmethod
    def Update():
        Time.deltaTime = (time.time() - Time.lastFrame) * Time.timeScale
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
        del self
        
        
        
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
# Create keyframes that control the values of different variables over time to create animations!
# Keyframes store: (customKeyString, targetValue, timeInterval) --- "Keyframe('scale.x', 2, 5)" creates a keyframe:
# for key 'scale.x' that has a value of 2 at 5 seconds. (the key is just a string; it can be anything, but try to match it with the variable)
# To begin, declare a class that inherits 'Animation' --- "class A_PlayerIdle(Animation):"
# Create a 'Keyframes' function for the clase; inside, return a list of all of your keyframes (and nothing else; only a single return statement)
# (Outside of 'Keyframes()'): Define a 'Keys():' method (must match name exactly) to add the references to the variables you want to modify.
# For example, if you want keyframes to modify something's 'transform.scale.x', make the key that those frames use = 'scale.x':
# Then, inside of the 'Keys()' method, assign "target.transform.scale.x = self.GetKeyValue('scale.x')" (this is why you should name your keys correctly)
# To play an animation, call 'customAnimation.Play()'. To stop, call 'customAnimation.Stop()'. To make it loop, set 'customAnimation.looping = True'
# That was probably really confusing, so here is an example. You can also look at the animations in the "Open World Game" example below.

# Goal: Create an animation to make a player's 'scale.y' start at 1, increase to 2 in one second, then go back to 1 in the next second.
# Line 1:   class PlayerWalkAnimation(Animation):
# Line 2:       def Keyframes(self):
# Line 3:           return [Keyframe('scale.y', 1, 0), Keyframe('scale.y', 2, 1), Keyframe('scale.y', 1, 2)]
# Line 4:       def Keys(self):
# Line 5:           player.transform.scale.y = self.GetKeyValue('scale.y')
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
        # Override this in your child 'Animation' class to set the keys.
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

# app.background = gradient(rgb(101, 105, 110), rgb(120, 128, 140), start='bottom-right')


mainCamera = Camera()

# list to store all GameObjects, used for running their Update() methods.
# Don't modify this. GameObjects automatically add themselves (as long as you call super().__init__())
app.gameObjectList = [] 
app.destroyedGameObjectList = []

app.animationList = []

############### ENGINE STARTUP ###############
















debug = Debug()

Time.timeScale = 1

def Grid(x, y):
    return Vector2(x*35, y*-35)

# Change this value if you want; it is just frames per second.
# The maximum is '240'
app.stepsPerSecond = 240

class ObjectType(Enum):
    SOLID = 0
    HAZARD = 1
    ORB = 2
    PAD = 3
    PORTAL = 4
    DECO = 5

class HitboxType(Enum):
    PHYSICAL = 0
    COLLISION = 1
    SPECIAL = 2
    NONE = 3

class Object(GameObject):
    def __init__(self, x, y, rotation=0):
        self.rotation = rotation
        if (self.rotation%90 != 0):
            raise Exception(f"Object rotation ({rotation}) must be of a 90 degree increment!")
        
        super().__init__()
        
        self.visual.visible = False
        self.collider.visible = False
        
        self.type = None
        self.hitboxType = None
        
        self.position = Grid(x, y).x

        self.transform.position = Vector2(Grid(x, y).x, Grid(x, y).y + levelManager.cameraOffset)
        
        self.hitbox = None
        
        self.hitboxOffset = Vector2()
        self.visualOffset = Vector2()
        
        self.hitboxHeight = None
        self.hitboxWidth = None
        self.hitboxLeft = None
        self.hitboxRight = None
        self.hitboxTop = None
        self.hitboxBottom = None
        
        self.onScreen = False
        self.hitboxesNeeded = False
        self.hitboxesUnrendered = False
        
        self.isPlayersGround = False
        self.playerWasAbove = False
        self.playerWasBelow = False
        
        self.overrideCulling = False
        
    def OnLateLoad(self):
        self.hitboxWidth = self.hitbox.width
        self.hitboxHeight = self.hitbox.height
        
        self.hitboxTop = self.transform.position.y - self.hitboxHeight/2 + self.hitboxOffset.y
        self.hitboxBottom = self.transform.position.y + self.hitboxHeight/2 + self.hitboxOffset.y
        self.hitboxLeft = self.transform.position.x - self.hitboxWidth/2 + self.hitboxOffset.x
        self.hitboxRight = self.transform.position.x - self.hitboxWidth/2 + self.hitboxOffset.x
            
        if (self.hitbox != None):
            self.hitboxTop = self.transform.position.y - self.hitboxHeight/2 + self.hitboxOffset.y
            self.hitboxBottom = self.transform.position.y + self.hitboxHeight/2 + self.hitboxOffset.y
        
        if (self.rotation %360 != 0): 
            if (self.rotation%360 == 90):
                self.visual.rotateAngle = 90
                oldOffset = Vector2(self.visualOffset.x, self.visualOffset.y)
                self.visualOffset.x = -oldOffset.y
                self.visualOffset.y = oldOffset.x
                if (self.hitbox != None): 
                    self.hitbox.rotateAngle = 90
                    oldOffset = Vector2(self.hitboxOffset.x, self.hitboxOffset.y)
                    self.hitboxOffset.x = -oldOffset.y
                    self.hitboxOffset.y = oldOffset.x
            elif (self.rotation%360 == 180):
                self.visual.rotateAngle = 180
                self.visualOffset.x *= -1
                self.visualOffset.y *= -1
                if (self.hitbox != None): 
                    self.hitbox.rotateAngle = 180
                    self.hitboxOffset.x *= -1
                    self.hitboxOffset.y *= -1
            elif (self.rotation%360 == 270):
                self.visual.rotateAngle = 270
                oldOffset = Vector2(self.visualOffset.x, self.visualOffset.y)
                self.visualOffset.x = oldOffset.y
                self.visualOffset.y = -oldOffset.x
                if (self.hitbox != None): 
                    self.hitbox.rotateAngle = 270
                    oldOffset = Vector2(self.hitboxOffset.x, self.hitboxOffset.y)
                    self.hitboxOffset.x = oldOffset.y
                    self.hitboxOffset.y = -oldOffset.x
                    
                    
                    
    def hitsPlayerPhysical(self):
        if (self.hitboxHeight == None or self.hitboxWidth == None or player.collisionTop == None or player.physicalTop == None): return
    
        myTop = self.hitboxTop
        myBottom = self.hitboxBottom
        myLeft = self.hitboxLeft
        myRight = self.hitboxRight
        
        theirTop = player.physicalTop
        theirBottom = player.physicalBottom
        theirLeft = player.physicalLeft
        theirRight = player.physicalRight
        
        rightInside = (theirRight >= myLeft and theirRight <= myRight)
        leftInside = (theirLeft <= myRight and theirLeft >= myLeft)
        bottomInside = (theirBottom >= myTop and theirBottom <= myBottom)
        topInside = (theirTop <= myBottom and theirTop >= myTop)
        
        myRightInside = (myRight >= theirLeft and myRight <= theirLeft)
        myLeftInside = (myLeft <= theirRight and myLeft >= theirLeft)
        myBottomInside = (myBottom >= theirTop and myBottom <= theirBottom)
        myTopInside = (myTop <= theirBottom and myTop >= theirTop)
        
        isColliding = (
            ((bottomInside or topInside) and (leftInside or rightInside)) or        # any of the four courners of the player are contained in the object
            ((myBottomInside or myTopInside) and (myLeftInside or myRightInside))   # any of the object's corners are contained inside of the player
            )
        
        return isColliding
                    
    def hitsPlayerCollision(self):
        if (self.hitboxHeight == None or self.hitboxWidth == None or player.collisionTop == None or player.physicalTop == None): return
    
        myTop = self.hitboxTop
        myBottom = self.hitboxBottom
        myLeft = self.hitboxLeft
        myRight = self.hitboxRight
        
        theirTop = player.collisionTop
        theirBottom = player.collisionBottom
        theirLeft = player.collisionLeft
        theirRight = player.collisionRight
        
        rightInside = (theirRight >= myLeft and theirRight <= myRight)
        leftInside = (theirLeft <= myRight and theirLeft >= myLeft)
        bottomInside = (theirBottom >= myTop and theirBottom <= myBottom)
        topInside = (theirTop <= myBottom and theirTop >= myTop)
        
        myRightInside = (myRight >= theirLeft and myRight <= theirLeft)
        myLeftInside = (myLeft <= theirRight and myLeft >= theirLeft)
        myBottomInside = (myBottom >= theirTop and myBottom <= theirBottom)
        myTopInside = (myTop <= theirBottom and myTop >= theirTop)
        
        isColliding = (
            ((bottomInside or topInside) and (leftInside or rightInside)) or        # any of the player's corners are contained inside of the object
            ((myBottomInside or myTopInside) and (myLeftInside or myRightInside))   # any of the object's corners are contained inside of the player
            )
        
        return isColliding
                
                
    def Update(self):
        
        if (self.transform.position.x < -220 and not self.overrideCulling):
            self.DestroySelf()
            if (self.hitbox != None): self.hitbox.visible = False
            self.hitbox = None
            return
        
        # Move the object across the screen
        self.transform.position.x = self.position - levelManager.position + 220
        
        # Apply the visual offset
        self.visual.centerX += self.visualOffset.x
        self.visual.centerY += self.visualOffset.y       
        
        # Set the hitbox positions
        if (self.hitboxWidth != None):
            self.hitboxLeft = self.transform.position.x - self.hitboxWidth/2 + self.hitboxOffset.x
            self.hitboxRight = self.transform.position.x + self.hitboxWidth/2 + self.hitboxOffset.x
        
        # Return if no hitboxes
        if (self.hitbox == None or self.hitboxType == HitboxType.NONE or self.hitboxLeft == None): 
            return
        
        if (player.physicalRight != None):
            self.hitboxesNeeded = (
                (self.hitboxLeft - 35 < player.physicalRight and self.hitboxRight + 35 > player.physicalLeft) and 
                (self.hitboxTop - 35 < player.physicalBottom and self.hitboxBottom + 35 > player.physicalTop)
                ) or self.overrideCulling
        
        if (self.hitboxesNeeded):
            # Physical Hitbox
            if (self.hitboxType == HitboxType.PHYSICAL):
                # Check if the player has passed/fallen off of its ground object --> starts airtime or gets a new ground
                if (self.isPlayersGround):
                    if (player.physicalLeft > self.hitboxRight):
                        player.LeaveGround()
                        self.isPlayersGround = False
                
                if (self.hitsPlayerPhysical()):
                    if (not player.upsideDown):
                        if (player.ground == None and self.playerWasAbove):
                            player.ground = self
                            self.isPlayersGround = True   
                    elif (player.upsideDown):
                        if (player.ground == None and self.playerWasBelow):
                            player.ground = self
                            self.isPlayersGround = True   
                    player.OnPhysicalIntoPhysical(self, None)
                        
                if (self.hitsPlayerCollision() and not self.isPlayersGround):
                    player.OnCollisionIntoPhysical(self, None)
                
                if (player.collisionBottom != None and player.collisionTop != None):
                    self.playerWasAbove = player.collisionBottom <= self.hitboxTop and player.velocity <= 0
                
                    self.playerWasBelow = player.collisionTop >= self.hitboxBottom and player.velocity >= 0
            
            # Collision Hitbox
            elif (self.hitboxType == HitboxType.COLLISION):
                if (self.hitsPlayerPhysical()):
                    player.OnPhysicalIntoCollision(self, None)
                if (self.hitsPlayerCollision()):
                    player.OnCollisionIntoCollision(self, None)
                    
            # Special Hitbox
            elif (self.hitboxType == HitboxType.SPECIAL):
                if (self.hitsPlayerPhysical()):
                    player.OnPhysicalIntoSpecial(self, self.type)
            
                
            
            
            
### SPIKES ###

class Spike(Object):
    def OnLoad(self):
        self.type = ObjectType.HAZARD
        self.hitboxType = HitboxType.COLLISION
        
        self.visual = Polygon(0, 0, 17.5, -35, 35, 0, border='white', borderWidth=2)
        
        self.hitbox = Rect(0,0, 7.5, 14.25, fill='red', opacity=0)
        self.hitboxOffset.y = .85
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        
class GroundSpikes(Object):
    def OnLoad(self):
        self.type = ObjectType.HAZARD
        self.hitboxType = HitboxType.COLLISION
        
        self.visual = Polygon(0,0, 0,-3.075, 3.15,-8.75, 5.3,-4.85, 10.075,-16.75, 14.15,-5.92, 16.5,-9.25, 19.15,-5.6, 21.325,-8.125, 23,-6.85, 25.9,-14.125, 29.3,-5.06, 32.1,-10.575, 35,-3.06, 35,0)
        self.visualOffset.y = 8.525
        
        self.hitbox = Rect(0,0, 10.75, 7.5, fill='red', opacity=0)
        self.hitboxOffset.y = 16.15
        
### SPIKES ###
        
        
        
### BLOCKS ###
        
class Block(Object):
    def OnLoad(self):
        self.type = ObjectType.SOLID
        self.hitboxType = HitboxType.PHYSICAL
        
        self.visual = Rect(0, 0, 35, 35, border='white', borderWidth=2)
        
        self.hitbox = Rect(0,0, 35, 35, fill='blue', opacity=0)
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.playerWasAbove = False
        
        
class HalfBlock(Object):
    def OnLoad(self):
        self.type = ObjectType.SOLID
        self.hitboxType = HitboxType.PHYSICAL
        
        self.visual = Rect(0, 0, 35, 17.5, border='white', borderWidth=2)
        self.visualOffset.y = -8.75
        
        self.hitbox = Rect(0,0, 35, 17.5, fill='blue', opacity=0)
        self.hitboxOffset.y = -8.75
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.playerWasAbove = False
                
### BLOCKS ###



### ORBS ###

class YellowOrb(Object):
    def OnLoad(self):
        self.type = ObjectType.ORB
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Group(
            Circle(0,0, 11.5, fill=gradient(rgb(255, 255, 30), rgb(255, 235, 0)), border='white', borderWidth=2),
            Circle(0,0, 17.5, fill=None, border='white', borderWidth=2)
            )
        
        self.hitbox = Rect(0,0, 45, 45, fill='lime', opacity=0)
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        self.strength = 735 #733
        
    def OnPlayerClick(self):
        player.velocity = self.strength
        player.isBuffering = False
        player.LeaveGround()
        self.isAvailable = False


class PinkOrb(Object):
    def OnLoad(self):
        self.type = ObjectType.ORB
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Group(
            Circle(0,0, 10.75, fill=gradient(rgb(218, 119, 214), rgb(255, 68, 255)), border='white', borderWidth=2.2),
            Circle(0,0, 17.5, fill=None, border='white', borderWidth=2.2)
            )
        
        self.hitbox = Rect(0,0, 45, 45, fill='lime', opacity=0)
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        self.strength = 545 #550
        
    def OnPlayerClick(self):
        player.velocity = self.strength
        player.isBuffering = False
        player.LeaveGround()
        self.isAvailable = False


class BlueOrb(Object):
    def OnLoad(self):
        self.type = ObjectType.ORB
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Group(
            Circle(0,0, 13, fill=gradient(rgb(0, 245, 250), rgb(0, 250, 255)), border='white', borderWidth=2),
            Circle(0,0, 17.5, fill=None, border='white', borderWidth=2)
            )
        
        self.hitbox = Rect(0,0, 45, 45, fill='lime', opacity=0)
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        self.strength = 545 #550
        
    def OnPlayerClick(self):
        player.ReverseGravity()
        if (not player.upsideDown):
            player.velocity = -self.strength
        else:
            player.velocity = self.strength
        player.isBuffering = False
        player.LeaveGround()
        self.isAvailable = False


class BlackOrb(Object):
    def OnLoad(self):
        self.type = ObjectType.ORB
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Group(
            Circle(0,0, 13, fill=gradient(rgb(30, 30, 30), rgb(5, 5, 5)), border='white', borderWidth=2.6),
            Circle(0,0, 18.5, fill=None, border='white', dashes=(7.65, 6.75), borderWidth=2.6, rotateAngle=-11)
            )
        
        self.hitbox = Rect(0,0, 45, 45, fill='lime', opacity=0)
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        
    def OnPlayerClick(self):
        player.velocity = player.terminalVelocity
        player.isBuffering = False
        player.LeaveGround()
        self.isAvailable = False
        

### ORBS ###



### PADS ###

class YellowPad(Object):
    def OnLoad(self):
        self.type = ObjectType.PAD
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Arc(0,0, 29, 10, 270, 180, fill='yellow', border='white', borderWidth=0.5)
        self.visualOffset.y = 17.5
        
        self.hitbox = Rect(0,0, 28.5, 5, fill='lime', opacity=0)
        self.hitboxOffset.y = 15
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        self.strength = 1055 #1060
        
    def OnPlayerEnter(self):
        player.velocity = self.strength
        player.isBuffering = False
        player.LeaveGround()
        self.isAvailable = False


class PinkPad(Object):
    def OnLoad(self):
        self.type = ObjectType.PAD
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Arc(0,0, 29, 10, 270, 180, fill=rgb(255, 85, 255), border='white', borderWidth=0.35)
        self.visualOffset.y = 17.5
        
        self.hitbox = Rect(0,0, 28.5, 5, fill='lime', opacity=0)
        self.hitboxOffset.y = 15
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        self.strength = 714 #710
        
    def OnPlayerEnter(self):
        player.velocity = self.strength
        player.isBuffering = False
        player.LeaveGround()
        self.isAvailable = False


class BluePad(Object):
    def OnLoad(self):
        self.type = ObjectType.PAD
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Arc(0,0, 29, 13, 270, 180, fill=rgb(45, 200, 255), border='white', borderWidth=0.35)
        self.visualOffset.y = 17.5
        
        self.hitbox = Rect(0,0, 28.5, 5, fill='lime', opacity=0)
        self.hitboxOffset.y = 15
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        self.strength = 545 
        
    def OnPlayerEnter(self):
        player.ReverseGravity()
        if (not player.upsideDown):
            player.velocity = -self.strength
        else:
            player.velocity = self.strength
        player.isBuffering = False
        player.LeaveGround()
        self.isAvailable = False
        
### PADS ###



### PORTALS ###

class YellowPortal(Object):
    def OnLoad(self):
        self.type = ObjectType.PORTAL
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Image(Images.YELLOW_PORTAL, 0, 0)
        self.visual.width *= 0.31
        self.visual.height *= 0.31
        
        self.hitbox = Rect(0,0, 27, 92, fill='lime', opacity=0)
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        
    def OnPlayerEnter(self):
        self.isAvailable = False
        if (not player.upsideDown):
            player.velocity = Clamp(player.velocity, min=player.terminalVelocity/1.85) ### UNCONFIRMED
            player.ReverseGravity()


class BluePortal(Object):
    def OnLoad(self):
        self.type = ObjectType.PORTAL
        self.hitboxType = HitboxType.SPECIAL
        
        self.visual = Image(Images.BLUE_PORTAL, 0, 0)
        self.visual.width *= 0.31
        self.visual.height *= 0.31
        
        self.hitbox = Rect(0,0, 27, 92, fill='lime', opacity=0)
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.isAvailable = True
        
    def OnPlayerEnter(self):
        self.isAvailable = False
        if (player.upsideDown):
            player.velocity = Clamp(player.velocity, max=player.terminalVelocity/1.85) ### UNCONFIRMED
            player.ReverseGravity()
    
### PORTALS ###



class Ground(Object):
    def OnLoad(self):
        self.type = ObjectType.SOLID
        self.hitboxType = HitboxType.PHYSICAL
        
        self.size = 20000
        
        self.visual = Rect(0, 0, self.size, 200, border='white', fill=gradient('gray', 'darkGray', start='left'))
        self.visualOffset.x = self.size/2 - 150
            
        self.hitbox = Rect(0, 0, self.size, 200, fill='blue', opacity=0)
        self.hitboxOffset.x = self.size/2 - 150
        
        self.transform.position = Vector2(self.transform.position.x, self.transform.position.y)
        
        self.overrideCulling = True
    

class LevelManager(GameObject):
    def Awake(self):
        self.cameraOffset = 65
        
        self.moveSpeed = 362.5 #357.3
        
        self.backgroundMoveSpeed = 22.5 #22.5
        self.background = []
        
        self.level = None
        self.playerIsReady = False
        self.loadingTimer = 0
        self.levelHasStarted = False
        self.position = 220
        
        self.nextObjectList = []
        self.nextObjectIndex = 0
        
    def Update(self):
        if (Input.GetKey('space') or Input.GetKey('up') or Input.GetMouse(0)):
            self.playerIsReady = True
        
        if (self.playerIsReady):
            self.loadingTimer += Time.deltaTime
            
        if (self.level != None and self.levelHasStarted):
            for slice in self.background:
                slice.centerX -= self.backgroundMoveSpeed * Time.deltaTime
                if (slice.right < 400 and not slice.hasSpawnedSlice):
                    newSlice = self.GenerateBackgroundSlice(self.level.backgroundType)
                    newSlice.left = slice.right
                    newSlice.toBack()
                    self.background.append(newSlice)
                    slice.hasSpawnedSlice = True
                if (slice.right < 0):
                    self.background.remove(slice)
                    slice.visibile = False
                    
            self.backgroundMask.fill = rgb(self.level.r, self.level.g, self.level.b)
            self.ground.visual.fill = rgb(self.level.r, self.level.g, self.level.b)
            self.position += self.moveSpeed * Time.deltaTime
            
            while (self.nextObjectIndex < len(self.nextObjectList)):
                nextObject = self.nextObjectList[self.nextObjectIndex]
                if (nextObject.position <= self.position):
                    app.gameObjectList.append(nextObject)
                    nextObject.transform.offset.y = 200-mainCamera.position.y
                    self.nextObjectIndex += 1
                else:
                    break
                    
        if (self.loadingTimer > .1 and not self.levelHasStarted):
            self.levelHasStarted = True
            if (self.level.backgroundAnimation != None): self.level.backgroundAnimation.Play()
            if (self.level.song != None): self.level.song.play(restart=True)
        
    def Load(self, levelClass):
        
        self.ground = Ground(0, 116.8/-35)
        self.ground.OnLoad()
        self.ground.OnLateLoad()
        player.ground = self.ground
        
        self.level = levelClass()
        self.position = 220
        
        self.background.clear()
        self.background.append(self.GenerateBackgroundSlice(self.level.backgroundType))
        
        self.nextObjectList.clear()
        
        objectsLeftList = []
        
        for object in self.level.objects:
            if (not object.overrideCulling):
                object.OnLoad()
                object.OnLateLoad()
                objectsLeftList.append(object)
                app.gameObjectList.remove(object)

        for i in range (len(objectsLeftList)):
            nearestObject = None
            for object in objectsLeftList:
                if (nearestObject == None):
                    nearestObject = object
                else:
                    if (object.position < nearestObject.position):
                        nearestObject = object
            self.nextObjectList.append(nearestObject)
            objectsLeftList.remove(nearestObject)
            
        self.nextObjectIndex = 0
        
        self.backgroundMask = Rect(0,0,400,400, fill=rgb(self.level.r, self.level.g, self.level.b))
        self.backgroundMask.toBack()
        self.backgroundMask.opacity = 65
        for slice in self.background:
            slice.toBack()
        
        
    def GenerateBackgroundSlice(self, backgroundType):
        image = Image(backgroundType, 0, 0)
        image.width *= 0.35
        image.height *= 0.35
        image.centerY -= 325
        image.hasSpawnedSlice = False
        return image
        


class Player(GameObject):
    def Awake(self):
        self.physicalHitboxSize = 35
        self.collisionHitboxSize = 10 #10
        
        self.visual = Group(
            Rect(0,0, self.physicalHitboxSize, self.physicalHitboxSize, fill=None, border='black', borderWidth=9, align='center'),
            Rect(0,0, self.physicalHitboxSize-3.75, self.physicalHitboxSize-3.75, fill=None, border=gradient(rgb(255, 220, 0), rgb(235, 203, 0), start='top-left'), borderWidth=5.5, align='center'),
            Rect(0,0, 11, 11, fill=gradient('aqua', 'lightBlue', start='top-left'), border='black', borderWidth=2, align='center')
            )
        
        self.physicalHitbox = Rect(0,0, self.physicalHitboxSize, self.physicalHitboxSize, fill=None, border='red', align='center', borderWidth=1, opacity=0)
        self.collisionHitbox = Rect(0,0, self.collisionHitboxSize, self.collisionHitboxSize, fill=None, border='blue', align='center', borderWidth=1, opacity=0)
        
        self.transform.position = Vector2(-125, 0 + levelManager.cameraOffset)
        
        self.physicalWidth = self.physicalHitboxSize
        self.physicalHeight = self.physicalHitboxSize
        
        self.physicalTop = self.transform.position.y - self.physicalHeight/2
        self.physicalBottom = self.transform.position.y + self.physicalHeight/2
        self.physicalLeft = self.transform.position.x - self.physicalWidth/2
        self.physicalRight = self.transform.position.x + self.physicalWidth/2
        
        self.collisionWidth = self.collisionHitboxSize
        self.collisionHeight = self.collisionHitboxSize
        
        self.collisionTop = self.transform.position.y - self.collisionHeight/2
        self.collisionBottom = self.transform.position.y + self.collisionHeight/2
        self.collisionLeft = self.transform.position.x - self.collisionWidth/2
        self.collisionRight = self.transform.position.x + self.collisionWidth/2
        
        self.velocity = 0
        
        self.jumpHeight = 700 # 648 # 680 #710
        self.gravity = -3300 # -3150 # -3325
        self.terminalVelocity = -917.5
        self.isGrounded = True
        self.ground = None # This is set to the level's ground in 'levelManager.Load()'
        self.groundCheckRayDistance = 0.1
        
        self.airRotationSpeed = 425 #360
        self.lastRotationAngle = 0
        self.isFlat = False
        
        self.isBuffering = False
        
        self.cameraTargetPoint = self.transform.position.y - 65
        
        self.upsideDown = False
        
        
        
        
    def Update(self):
        if (not levelManager.levelHasStarted): return
    
        if (not self.isGrounded):
            if (not self.upsideDown):
                self.velocity = Clamp(self.velocity + (self.gravity * Time.deltaTime), min = self.terminalVelocity)
            else:
                self.velocity = Clamp(self.velocity + (self.gravity * Time.deltaTime), max = self.terminalVelocity)
                
            self.isFlat = False
            
        if (not self.isFlat):
            self.lastRotationAngle = self.visual.rotateAngle
            if (not self.isGrounded):   
                self.visual.rotateAngle += self.airRotationSpeed * Time.deltaTime
            elif (self.isGrounded):
                rotateAngle = self.visual.rotateAngle % 90
                self.rotationFallingRight = rotateAngle >= 45
                if (not self.rotationFallingRight):
                    self.visual.rotateAngle -= 1.25 * self.airRotationSpeed * Time.deltaTime
                elif (self.rotationFallingRight):
                    self.visual.rotateAngle += 1.25 * self.airRotationSpeed * Time.deltaTime
            
        if (self.isGrounded and ((self.lastRotationAngle%90 > self.visual.rotateAngle%90 and self.rotationFallingRight) or (self.lastRotationAngle%90 < self.visual.rotateAngle%90 and not self.rotationFallingRight))):
            self.isFlat = True
            self.rotationFallingRight = False
            self.visual.rotateAngle = 0
        
        if (Input.GetKeyDown('space') or Input.GetKeyDown('up') or Input.GetMouseDown(0) and not self.isGrounded):
            self.isBuffering = True
        
        if (Input.GetKeyUp('space') or Input.GetKeyUp('up') or Input.GetMouseUp(0)):
            self.isBuffering = False
            
            
        # Jump
        if ((Input.GetKey('space') or Input.GetKey('up') or Input.GetMouse(0)) and self.isGrounded):
            self.velocity = self.jumpHeight
            self.isBuffering = False
            self.LeaveGround()
            
        def predictTrajectory():
            if (self.velocity == 0): return 0
            
            vi = self.velocity
            t = Time.deltaTime
            a = self.gravity
            d = vi*t + 0.5*a*(t**2)
            return d
            
        self.transform.position.y -= predictTrajectory()
        
        if (self.ground != None and not self.upsideDown):
            positionFromGround = ((self.ground.transform.position.y - self.ground.hitboxHeight/2 + self.ground.hitboxOffset.y) - (self.transform.position.y + self.physicalHeight/2))
            if (positionFromGround <= 0 and not self.isGrounded):
                self.isGrounded = True
                self.velocity = 0
                self.transform.position.y += positionFromGround
        elif (self.ground != None and self.upsideDown):
            positionFromGround = ((self.ground.transform.position.y + self.ground.hitboxHeight/2 + self.ground.hitboxOffset.y) - (self.transform.position.y - self.physicalHeight/2))
            if (positionFromGround >= 0 and not self.isGrounded):
                self.isGrounded = True
                self.velocity = 0
                self.transform.position.y += positionFromGround
            
        if (self.transform.position.y <= mainCamera.position.y - 90): 
            self.cameraTargetPoint = self.transform.position.y + 90
        elif (self.transform.position.y >= mainCamera.position.y + 100):
            self.cameraTargetPoint = self.transform.position.y - 70
        
        if (mainCamera.position.y + .5 < self.cameraTargetPoint) or (mainCamera.position.y - .5 > self.cameraTargetPoint):
            mainCamera.position.y = Lerp(mainCamera.position.y, self.cameraTargetPoint, 4 * Time.deltaTime)
        else:
            mainCamera.position.y = self.cameraTargetPoint
            
        # Update collision positions after all motion is calculated (leave at the end)
        self.physicalTop = self.transform.position.y - self.physicalHeight/2
        self.physicalBottom = self.transform.position.y + self.physicalHeight/2
        self.physicalLeft = self.transform.position.x - self.physicalWidth/2
        self.physicalRight = self.transform.position.x + self.physicalWidth/2
        
        self.collisionTop = self.transform.position.y - self.collisionHeight/2
        self.collisionBottom = self.transform.position.y + self.collisionHeight/2
            
        
    def OnPhysicalIntoPhysical(self, sender, e):
        pass
        
    def OnPhysicalIntoCollision(self, sender, e):
        print("Hit a spike")
        # self.collider.opacity = 100
        app.stop()
        
    def OnCollisionIntoPhysical(self, sender, e):
        if (not sender.isPlayersGround):
            print("Ran into the side of a block")
            # self.collider.opacity = 100
            app.stop()
            
    def OnCollisionIntoCollision(self, sender, e):
        print("Something has gone terribly wrong...")
        # self.collider.opacity = 100
        app.stop()
        
    def OnPhysicalIntoSpecial(self, sender, e):
        # It's an orb
        if (e == ObjectType.ORB and sender.isAvailable and self.isBuffering):
            sender.OnPlayerClick()
        
        # It's a pad
        if (e == ObjectType.PAD and sender.isAvailable):
            sender.OnPlayerEnter()
            
        # It's a portal
        if (e == ObjectType.PORTAL and sender.isAvailable):
            sender.OnPlayerEnter()
                
                
    def LeaveGround(self):
        self.isGrounded = False
        if (self.ground != None):
            self.ground.isPlayersGround = False
            self.ground = None
            
    def ReverseGravity(self):
        self.airRotationSpeed *= -1
        self.gravity *= -1
        self.jumpHeight *= -1
        self.terminalVelocity *= -1
        self.upsideDown = not self.upsideDown
        self.LeaveGround()
          
          
            
class Level:
    def __init__(self):
        self.backgroundType = Images.BACKGROUND_1
        self.r = 0
        self.g = 77
        self.b = 255
        
        self.backgroundAnimation = None
        
        self.objects = []
        
        self.song = Audio.STEREO_MADNESS
        
        self.OnLoad()
        
    def OnLoad(self):
        # override me
        pass
            
### LEVELS ###
            
class Level_PhysicsTest(Level):
    def OnLoad(self):
    
        self.objects = [
            Block(0, 10),
            Block(6, 1),
            Block(7, 1),
            Block(8, 1),
            Spike(6, 0),
            Spike(7, 0),
            Spike(8, 0),
            
            Spike(10, 0),
            Spike(12.5, 0),
            
            Block(15, 1),
            
            Spike(18.5, 0),
            Spike(21, 0),
            
            Block(23, 1.5),
            
            Spike(25, 3),
            Spike(26.5, 5),
            Block(26, 2),
            Block(27, 2),
            
            Block(30, 1),
            
            Spike(33, 2),
            Block(34, 4),
            Block(34, 1),
            Block(35, 1),
            
            Spike(39.5, 0),
            Spike(40.5, 0),
            Spike(41.5, 0),
            ]
        
class Level_FirstRealLevel(Level):
    def OnLoad(self):
        self.backgroundType = Images.BACKGROUND_1
        self.r = 0
        self.g = 77
        self.b = 255
        
        class Anim_BG(Animation):
            def Keyframes(self):
                return [
                    Keyframe('r', 0, 0),
                    Keyframe('g', 77, 0),
                    Keyframe('b', 255, 0),
                    
                    Keyframe('r', 0, 6.4),
                    Keyframe('g', 141, 6.4),
                    Keyframe('b', 190, 6.4),
                    
                    Keyframe('r', 38, 6.45),
                    Keyframe('g', 203, 6.45),
                    Keyframe('b', 219, 6.45),
                    
                    Keyframe('r', 0, 6.83),
                    Keyframe('g', 153, 6.83),
                    Keyframe('b', 160, 6.83),
                    
                    Keyframe('r', 37, 6.88),
                    Keyframe('g', 203, 6.88),
                    Keyframe('b', 143, 6.88),
                    
                    Keyframe('r', 0, 7.31),
                    Keyframe('g', 160, 7.31),
                    Keyframe('b', 68, 7.31),
                    
                    Keyframe('r', 5, 13.51),
                    Keyframe('g', 112, 13.51),
                    Keyframe('b', 104, 13.51),
                    
                    Keyframe('r', 255, 13.56),
                    Keyframe('g', 88, 13.56),
                    Keyframe('b', 88, 13.56),
                    
                    Keyframe('r', 145, 16.84),
                    Keyframe('g', 42, 16.84),
                    Keyframe('b', 42, 16.84),
                    
                    Keyframe('r', 255, 16.89),
                    Keyframe('g', 88, 16.89),
                    Keyframe('b', 88, 16.89),
                    
                    Keyframe('r', 145, 17.70),
                    Keyframe('g', 42, 17.70),
                    Keyframe('b', 42, 17.70),
                    
                    Keyframe('r', 255, 17.75),
                    Keyframe('g', 88, 17.75),
                    Keyframe('b', 88, 17.75),
                    
                    Keyframe('r', 145, 18.09),
                    Keyframe('g', 42, 18.09),
                    Keyframe('b', 42, 18.09),
                    
                    Keyframe('r', 255, 18.14),
                    Keyframe('g', 144, 18.14),
                    Keyframe('b', 88, 18.14),
                    
                    Keyframe('r', 145, 18.48),
                    Keyframe('g', 74, 18.48),
                    Keyframe('b', 42, 18.48),
                    
                    Keyframe('r', 255, 18.53),
                    Keyframe('g', 192, 18.53),
                    Keyframe('b', 88, 18.53),
                    
                    Keyframe('r', 145, 18.87),
                    Keyframe('g', 108, 18.87),
                    Keyframe('b', 42, 18.87),
                    
                    Keyframe('r', 167, 20.31),
                    Keyframe('g', 68, 20.31),
                    Keyframe('b', 10, 20.31),
                    
                    ]
                    
            def Keys(self):
                levelManager.level.r = self.GetKeyValue('r')
                levelManager.level.g = self.GetKeyValue('g')
                levelManager.level.b = self.GetKeyValue('b')
                
        self.backgroundAnimation = Anim_BG()
        
        self.objects = [
            
            Spike(19, 38, 180),
            Spike(20, 35),
            Spike(35, 77, 180),
            
            Spike(7, 0,),
            Spike(8, 0),
            Block(9, 0),
            Block(10, 0),
            GroundSpikes(11, 0),
            GroundSpikes(12, 0),
            GroundSpikes(13, 0),
            Block(14, 0),
            Block(15, 0),
            Block(16, 0),
            Spike(16, 1),
            Block(17, 0),
            Spike(17, 1),
            
            Block(21, 1),
            Spike(21, 2),
            
            Spike(24, 0),
            Block(25, 0),
            Block(25, 1),
            Block(26, 1),
            Block(27, 1),
            Block(27, 0),
            GroundSpikes(28, 0),
            Block(29, 0),
            Block(29, 1),
            Spike(29, 2),
            
            Block(32, 2),
            Block(32, 3),
            Block(32, 4),
            Block(32, 5),
            Block(32, 6),
            Block(32, 7),
            Block(32, 8),
            Block(32, 9),
            
            Block(35, 0),
            Block(35, 1),
            Block(36, 1),
            Block(37, 1),
            Block(37, 0),
            Block(38, 0),
            Block(39, 0),
            Block(40, 0),
            GroundSpikes(41, 0),
            Block(42, 0),
            Block(42, 1),
            Spike(42, 2),
            Spike(43, 0),
            
            Spike(46.5, 0),
            Spike(47.5, 0),
            
            Block(52, 0),
            Block(52, 1),
            Block(53, 0),
            Block(53, 1),
            Block(54, 0),
            Spike(54, 1),
            Block(55, 0),
            Spike(55, 1),
            Block(56, 0),
            Block(56, 1),
            Block(56, 2),
            Block(56, 3),
            Block(57, 0),
            Spike(57, 1),
            Block(58, 0),
            Spike(58, 1),
            
            Block(61, 1),
            Block(61, 2),
            Block(61, 3),
            Block(61, 4),
            Block(61, 5),
            Block(61, 6),
            Block(61, 7),
            Block(61, 8),
            
            Block(65, 0),
            Block(65, 1),
            Block(65, 3),
            Block(65, 4),
            Block(65, 5),
            Block(65, 6),
            Block(65, 7),
            Block(65, 8),
            
            GroundSpikes(66, 0),
            GroundSpikes(67, 0),
            
            Block(68, 0),
            Block(68, 1),
            Block(68, 2),
            Block(68, 3),
            Block(68, 5),
            Block(68, 6),
            Block(68, 7),
            Block(68, 8),
            
            Block(69, 3),
            Block(70, 3),
            Block(70, 2),
            Block(71, 2),
            Block(72, 2),
            Block(72, 1),
            Block(73, 1),
            Block(74, 1),
            Block(74, 0),
            Block(75, 0),
            Spike(75, 1),
            Block(76, 0),
            Spike(76, 1),
            Block(77, 0),
            Spike(77, 1),
            Block(75, 5),
            Block(76, 5),
            Block(77, 5),
            Block(78, 5),
            
            GroundSpikes(78, 0),
            GroundSpikes(79, 0),
            GroundSpikes(80, 0),
            GroundSpikes(81, 0),
            GroundSpikes(82, 0),
            GroundSpikes(83, 0),
            GroundSpikes(84, 0),
            GroundSpikes(85, 0),
            
            YellowOrb(79.5, 1),
            HalfBlock(83, 3),
            
            Block(86, 0),
            Block(86, 1),
            Block(86, 2),
            Spike(86, 3),
            GroundSpikes(87, 0),
            GroundSpikes(88, 0),
            GroundSpikes(89, 0),
            YellowOrb(88, 1.5),
            Block(90, 0),
            Block(90, 1),
            Spike(90, 2),
            
            GroundSpikes(91, 0),
            GroundSpikes(92, 0),
            GroundSpikes(93, 0),
            GroundSpikes(94, 0),
            GroundSpikes(95, 0),
            GroundSpikes(96, 0),
            HalfBlock(92, 2),
            HalfBlock(94, 1),
            HalfBlock(96, 0),
            
            Spike(100, 0),
            Spike(101, 0),
            YellowOrb(101, 2),
            Block(102, 0),
            Spike(102, 1),
            GroundSpikes(103, 0),
            GroundSpikes(104, 0),
            GroundSpikes(105, 0),
            GroundSpikes(106, 0),
            GroundSpikes(107, 0),
            GroundSpikes(108, 0),
            GroundSpikes(109, 0),
            GroundSpikes(110, 0),
            GroundSpikes(111, 0),
            GroundSpikes(112, 0),
            GroundSpikes(113, 0),
            GroundSpikes(114, 0),
            GroundSpikes(115, 0),
            GroundSpikes(116, 0),
            GroundSpikes(117, 0),
            GroundSpikes(118, 0),
            GroundSpikes(119, 0),
            GroundSpikes(120, 0),
            Block(121, 0),
            Spike(121, 1),
            HalfBlock(104, 3),
            HalfBlock(106, 2),
            HalfBlock(107, 2),
            Block(106, 5),
            Spike(106, 6),
            PinkOrb(111, 2.5),
            PinkOrb(113, 3.5),
            HalfBlock(115, 4),
            HalfBlock(116, 4),
            HalfBlock(115.5, 6),
            
            HalfBlock(118.5, 4),
            HalfBlock(119.5, 4),
            Spike(118.5, 5),
            Spike(119.5, 5),
            
            Spike(125, 0),
            Spike(126, 0),
            
            Spike(130, 0),
            Block(131, 0),
            Block(131, 1),
            Block(131, 3),
            HalfBlock(132, 1),
            GroundSpikes(132, 0),
            GroundSpikes(133, 0),
            GroundSpikes(134, 0),
            Block(135, 0),
            Spike(135, 1),
            
            YellowPad(137.5, 0),
            
            Block(140, 0),
            Spike(140, 1),
            GroundSpikes(141, 0),
            GroundSpikes(142, 0),
            PinkOrb(142, 3),
            GroundSpikes(143, 0),
            HalfBlock(143.5, 2),
            Spike(143.5, 3),
            GroundSpikes(144, 0),
            GroundSpikes(145, 0),
            YellowOrb(144.5, 4.5),
            GroundSpikes(146, 0),
            YellowOrb(146.5, 1),
            GroundSpikes(147, 0),
            Block(147, 7),
            Block(147, 8),
            Block(147, 6),
            GroundSpikes(148, 0),
            HalfBlock(148.5, 1),
            Spike(148.5, 2),
            GroundSpikes(149, 0),
            HalfBlock(149.5, 1),
            GroundSpikes(150, 0),
            HalfBlock(150.5, 1),
            PinkPad(150.5, 2),
            GroundSpikes(151, 0),
            GroundSpikes(152, 0),
            YellowOrb(152, 4),
            GroundSpikes(153, 0),
            GroundSpikes(154, 0),
            Block(154, 5),
            Block(154, 6),
            Block(154, 7),
            GroundSpikes(155, 0),
            PinkOrb(155, 0.5),
            GroundSpikes(156, 0),
            GroundSpikes(157, 0),
            
            Block(158, 0),
            YellowPad(158, 1),
            
            Spike(159, 0),
            Spike(160, 0),
            
            Block(161, 0), Spike(161, 1),
            Block(162, 0), Spike(162, 1), HalfBlock(162, 4), HalfBlock(162, 6),
            Block(163, 0), Spike(163, 1),
            HalfBlock(163.5, 3.5), HalfBlock(163.5, 5.5),
            Block(164, 0), Spike(164, 1),
            Spike(165, 0), HalfBlock(165, 3), HalfBlock(165, 5),
            Spike(166, 0),
            HalfBlock(166.5, 2.5), HalfBlock(166.5, 4.5),
            Spike(167, 0),
            Spike(168, 0),
            Spike(169, 0),
            Spike(170, 0),
            Spike(171, 0),
            Block(172, 0), Block(172, 1), Block(172, 2), YellowPad(172, 3),
            
            GroundSpikes(173, 0),
            GroundSpikes(174, 0),
            GroundSpikes(175, 0),
            GroundSpikes(176, 0),
            HalfBlock(176.5, 6), Spike(176.5, 8.5, 180), Block(176.5, 9.5),
            GroundSpikes(177, 0),
            HalfBlock(177.5, 6),
            GroundSpikes(178, 0),
            HalfBlock(178.5, 6), Spike(178.5, 7),
            GroundSpikes(179, 0),
            BlackOrb(179.5, 9),
            GroundSpikes(180, 0),
            GroundSpikes(181, 0), Spike(181, 8, 180), Block(181, 9), Block(181, 10), Block(181, 11), Block(181, 12), Block(181, 13), Block(181, 14),
            HalfBlock(181.5, 3),
            GroundSpikes(182, 0), PinkPad(182, 4), 
            HalfBlock(182.5, 3),
            GroundSpikes(183, 0),
            Block(183.5, 3.5), Spike(183.5, 4.5),
            GroundSpikes(184, 0),
            GroundSpikes(185, 0),
            YellowOrb(185.5, 3.5), Spike(185.5, 6.5, 180), Block(185.5, 7.5),
            GroundSpikes(186, 0),
            GroundSpikes(187, 0),
            Block(187.5, 3.5), Spike(187.5, 4.5),
            GroundSpikes(188, 0),
            GroundSpikes(189, 0),
            GroundSpikes(190, 0), YellowOrb(190, 3.5), Spike(190, 6.5, 180), Block(190, 7.5),
            GroundSpikes(191, 0),
            GroundSpikes(192, 0),
            GroundSpikes(193, 0),
            GroundSpikes(194, 0), HalfBlock(194, 3),
            GroundSpikes(195, 0),
            GroundSpikes(196, 0), HalfBlock(196, 2), Spike(196, 6, 270),
            GroundSpikes(197, 0), HalfBlock(197, 2), Block(197, 6),
            GroundSpikes(198, 0), HalfBlock(198, 2), Spike(198, 3),
            GroundSpikes(199, 0), HalfBlock(199, 2), Spike(199, 3), Spike(199, 6, 180), Block(199, 7),
            GroundSpikes(200, 0), PinkOrb(200, 4.5),
            GroundSpikes(201, 0),
            HalfBlock(201.5, 5), YellowPad(201.5, 6),
            GroundSpikes(202, 0),
            GroundSpikes(203, 0),
            GroundSpikes(204, 0),
            GroundSpikes(205, 0),
            Block(206, 0), Spike(206, 1),
            
            YellowPortal(208, 4, 90),
            
            HalfBlock(212, 8, 180),
            HalfBlock(214, 9, 180), Spike(214, 6), Block(214, 5),
            HalfBlock(215, 9, 180),
            HalfBlock(216, 9, 180), Spike(216, 8, 180),
            BlackOrb(217.5, 6),
            HalfBlock(218, 9, 180), YellowPad(218, 8, 180), Spike(218, 3), HalfBlock(218, 2),
            
            ]
            
        self.song = Audio.BASE_AFTER_BASE
        
class Level_PortalTest(Level):
    def OnLoad(self):
        
        self.objects = [
            PinkPad(2, 0),
        
            Block(5, 0), PinkPad(5, 1),
            Block(8, 2), Block(8, 1), Block(8, 0), PinkPad(8, 3),
            Block(11, 4), Block(11, 3), Block(11, 2), Block(11, 1), Block(11, 0),
            
            YellowPortal(14, 4), Spike(14, 6, 180), Block(14, 7, 180),
            HalfBlock(15, 7, 180),
            HalfBlock(16, 7, 180),
            HalfBlock(17, 7, 180),
            HalfBlock(18, 7, 180), Spike (18, 6, 180),
            HalfBlock(19, 7, 180), Spike (19, 6, 180),
            HalfBlock(20, 7, 180), Spike (20, 6, 180),
            
            BluePortal(22, 7, 270),
            
            YellowOrb(26, 3),
            
            GroundSpikes(25, 0),
            GroundSpikes(26, 0),
            GroundSpikes(27, 0),
            GroundSpikes(28, 0),
            GroundSpikes(29, 0),
            GroundSpikes(30, 0),
            GroundSpikes(31, 0),
            GroundSpikes(32, 0),
            GroundSpikes(33, 0),
            GroundSpikes(34, 0),
            GroundSpikes(35, 0),
            GroundSpikes(36, 0),
            GroundSpikes(37, 0),
            GroundSpikes(38, 0),
            GroundSpikes(39, 0),
            GroundSpikes(40, 0),
            GroundSpikes(41, 0),
            GroundSpikes(42, 0),
            GroundSpikes(43, 0),
            GroundSpikes(44, 0),
            GroundSpikes(45, 0),
            GroundSpikes(46, 0),
            GroundSpikes(47, 0),
            
            YellowPortal(31, 1, 90),
            BluePortal(34, 3, 270),
            YellowPortal(37, 1, 90),
            BluePortal(40, 3, 270),
            YellowPortal(43, 1, 90),
            BluePortal(46, 3, 270),
            
            YellowPad(49.5, 0), YellowPad(49.5, 0, 180), YellowPad(49.5, 1), YellowPad(49.5, 1, 180), YellowPad(49.5, 2), YellowPad(49.5, 2, 180), YellowPad(49.5, 3),
            
            HalfBlock(53, 3), 
            HalfBlock(54, 3), 
            HalfBlock(55, 3), 
            HalfBlock(56, 3), BluePad(56, 4),
            HalfBlock(57, 7, 180),
            HalfBlock(58, 7, 180),
            HalfBlock(59, 7, 180),
            HalfBlock(61, 8, 180),
            HalfBlock(64, 10, 180),
        ]
        
class Level_Test(Level):
    def OnLoad(self):
    
        self.objects = [
            Block(3, 3),
            Block(4, 3),
            Block(5, 3),
            Block(6, 3),
            Block(7, 3),
            Block(8, 3),
            Block(9, 3),
            Block(10, 3),
            Block(11, 3),
            Block(12, 3),
            Block(13, 3),
            Block(14, 3),
            Block(15, 3),
            Block(16, 3),
            Block(17, 3),
            Block(18, 3),
            Block(19, 3),
            Block(20, 3),
            Block(21, 3),
            Block(22, 3),
            ]        
        
### LEVELS ###
        
levelManager = LevelManager()

player = Player()

levelManager.Load(Level_FirstRealLevel)




Label("This is still very early in development.", 5, 5, fill='white', align='top-left')
Label("You should 100% expect to randomly die from a bug :)", 5, 20, fill='white', align='top-left')




























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