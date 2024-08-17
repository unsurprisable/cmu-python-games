# November 2023

import math
import time
import datetime
import random
from enum import Enum



class Audio:
    # PLAYER
    PLAYER_SHOOT_1 = Sound('cmu://682887/26594441/ROR2+Player+Shoot+1.mp3')
    PLAYER_SHOOT_2 = Sound('cmu://682887/26594443/ROR2+Player+Shoot+2.mp3')
    PLAYER_HURT_1 = Sound('cmu://682887/26659165/ROR2+Player+Hurt+1.mp3')
    PLAYER_HURT_2 = Sound('cmu://682887/26659168/ROR2+Player+Hurt+2.mp3')
    PLAYER_HURT_3 = Sound('cmu://682887/26659169/ROR2+Player+Hurt+3.mp3')
    
    # SOUND EFFECTS
    TELEPORTER_ACTIVATE = Sound('cmu://682887/26620959/ROR2+Teleporter+Activate.mp3')
    TELEPORTER_CHARGED = Sound('cmu://682887/26593768/ROR2+Teleporter+Charged.mp3')
    
    # SOUNDTRACK
    STAGE_1_SONG = Sound('cmu://682887/26594530/Chris+Christodoulou+-+Evapotranspiration.mp3')
    STAGE_1_BOSS_SONG = Sound('cmu://682887/26594125/Chris+Christodoulou+-+Thermodynamic+Equilibrium.mp3')
    STAGE_1_BOSS_OVER = Sound('cmu://682887/26594133/Thermodynamic+Equilibrium+Ending.mp3')
    
    STAGE_2_SONG = Sound('cmu://682887/26658086/Chris+Christodoulou+-+Terra+Pluviam.mp3')
    STAGE_2_BOSS_SONG = Sound('cmu://682887/26658281/Chris+Christodoulou+-+Hydrophobia.mp3')
    STAGE_2_BOSS_OVER = Sound('cmu://682887/26658283/Hydrophobia+Ending.mp3')
    
    STAGE_3_SONG = Sound('cmu://682887/26658509/Chris+Christodoulou+-+The+Rain+Formerly+Known+as+Purple.mp3')
    STAGE_3_BOSS_SONG = Sound('cmu://682887/26658584/Chris+Christodoulou+-+Antarctic+Oscillation.mp3')
    STAGE_3_BOSS_OVER = Sound('cmu://682887/26658681/Antarctic+Oscillation+Ending.mp3')
    
    STAGE_4_SONG = Sound('cmu://682887/26657960/Chris+Christodoulou+-+...con+lentitud+poderosa.mp3')
    
    # ENEMIES
    LEMURIAN_DEATH = Sound('cmu://682887/26594513/ROR2+Lemurian+Death+1.mp3')
    BEETLE_DEATH = Sound('cmu://682887/26594469/ROR2+Beetle+Death+1.mp3')
    GOLEM_DEATH = Sound('cmu://682887/26594498/ROR2+Golem+Death+3.mp3')



###### ENGINE
class Event:
    def __init__(self):
        self.handlers = []
        
    def Subscribe(self, handler):
        self.handlers.append(handler)
        
    def Unsubscribe(self, handler):
        self.handlers.remove(handler)
        
    def Invoke(self, *args, **kwargs):
        for handler in self.handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                pass
            
def event_handler(event):
    def decorator(func):
        event.Subscribe(func)
        return func
        
    return decorator

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
    
    def __iadd__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x + other.x, self.y + other.y)
    
    def __radd__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        if (isinstance(other, Vector2)):
            return Vector2(self.x - other.x, self.y - other.y)
            
    def __eq__(self, other):
        if (isinstance(other, Vector2)):
            return (self.x == other.x and self.y == other.y and self._magnitude == other._magnitude)
            
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
        
    @property
    def normalized(self):
        self.UpdateMagnitude()
        if (self._magnitude != 0):
            return Vector2(self.x / self._magnitude, self.y / self._magnitude)
        else:
            return Vector2(0, 0)
            
    def copy(self):
        return Vector2(self._x, self._y)
        
    @staticmethod
    def angleTo(x1, y1, x2, y2):
        return Vector2(x2-x1, y2-y1).normalized

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
     
        
class Time:
    lastFrame = time.time()
    timeScale = 1
    realTimeScale = 1
    deltaTime = 0.0
    realDeltaTime = 0.0
    
    @staticmethod
    def Update():
        Time.deltaTime = (time.time() - Time.lastFrame) * Time.timeScale
        Time.realDeltaTime = (time.time() - Time.lastFrame) * Time.realTimeScale
        Time.lastFrame = time.time()
        
class GameObject:
    
    def Awake(self):
        pass
        
    def __init__(self):
        self.visual = None
        
        self.collider = None
        
        self.transform = Transform(self)
        
        self.unrenderBuffer = -1
        self.unrendered = False
        
        app.gameObjectList.append(self)
        
        self._destroyed_ = False
        
        self.framesPassed = 0
        
        self.Awake()
        
        mainCamera.UpdateOffsets()
        
    def __destroySelf__(self):
        if (self.visual != None):
            self.visual.visible = False
        if (self.collider != None):
            self.collider.visible = False
        app.gameObjectList.remove(self)
        del self.visual
        del self.collider
        del self.transform
        del self
        
        
        
    def Start(self):
        pass
        
    def LateStart(self):
        pass
        
    def Update(self):
        pass
    
    def LateUpdate(self):
        pass
    
    def __backendUpdate__(self):
        if (self.framesPassed == 0):
            self.Start()
            self.transform.UpdateVisuals(True)
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
            

class Transform:
    def __init__(self, gameObject):
        self.gameObject = gameObject
        self._position = Vector2(0, 0)
        
        self.PositionSubscriptions()
        
    
    def PositionSubscriptions(self):
        @event_handler(self._position.OnModifiedX)
        def Position_OnModifiedX(sender, e):
            self.UpdateVisuals()
        @event_handler(self._position.OnModifiedY)
        def Position_OnModifiedY(sender, e):
            self.UpdateVisuals()
        
    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._position = value
        self.UpdateVisuals()
        self.PositionSubscriptions()
        
    def UpdateVisuals(self, overrideUnrender=False):
        if (self.gameObject.framesPassed >= 3 and self.gameObject.unrenderBuffer >= 0 and overrideUnrender == False and ((self.position.x > mainCamera.position.x + 200 + self.gameObject.unrenderBuffer or self.position.x < mainCamera.position.x - 200 - self.gameObject.unrenderBuffer) or (self.position.y > mainCamera.position.y + 200 + self.gameObject.unrenderBuffer or self.position.y < mainCamera.position.y - 200 - self.gameObject.unrenderBuffer))):
            if (not self.gameObject.unrendered): 
                self.gameObject.unrendered = True
                self.gameObject.visual.visible = False
                self.gameObject.collider.visible = False
                app.unrenderedGameObjects += 1
            return
        elif (self.gameObject.unrendered):
            self.gameObject.unrendered = False
            self.gameObject.visual.visible = True
            self.gameObject.collider.visible = True
            app.unrenderedGameObjects -= 1
        
        if (self.gameObject.visual != None):
            self.gameObject.visual.centerX = self.position.x + mainCamera.offset.x
            self.gameObject.visual.centerY = self.position.y + mainCamera.offset.y
        
        if (self.gameObject.collider != None):
            self.gameObject.collider.centerX = self.position.x + mainCamera.offset.x
            self.gameObject.collider.centerY = self.position.y + mainCamera.offset.y
        
    
class Camera:
    def __init__(self):
        self._position = Vector2()
        self.offset = Vector2(200, 200)
        self.Subscriptions()
        
    def UpdateOffsets(self):
        for gameObject in app.gameObjectList:
            if (isinstance(gameObject, Camera)): return
        
            self.offset = Vector2(200-self.position.x, 200-self.position.y)
            gameObject.transform.UpdateVisuals()
    
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



class Animation:
    def Keyframes(self):
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
        
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None
        self.arg4 = None
        
        app.animationList.append(self)
        
    def Update(self):
        if (not self.isPlaying): return
    
        self.time += Time.realDeltaTime
        self.UpdateKeyframes(self.time, self.time - Time.realDeltaTime)
        
        if (self.time >= self.endTime):
            self.Keys()
            self.Stop()
            if (self.looping):
                self.Play()
                self.OnAnimationLooped.Invoke(self, None)
            
            self.OnAnimationEnd.Invoke(self, None)
        else:
            self.Keys()
            
    def Keys(self):
        raise Exception("'Keys' method was not overriden in an 'Animation' child class!")
       
    def Play(self, restart=False, arg1=None, arg2=None, arg3=None, arg4=None):
        
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg4 = arg4
        
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
            if (keyframe.time > self.endTime):
                self.endTime = keyframe.time
            if (not keyframe.key in organizedKeyframes):
                organizedKeyframes[keyframe.key] = [keyframe]
            else:
                organizedKeyframes[keyframe.key].append(keyframe)
        
        for keyString in organizedKeyframes:
            keyValue = organizedKeyframes[keyString]
            
            keyframeList = keyValue.copy()
            for i in range(len(keyValue)):
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
            
            elif (targetKeyframe.easing == Easing.QUART_OUT):
                offset = 1-(1-intervalTime)**4
                value = activeKeyframe.value + offset * valueRange
                
            elif (targetKeyframe.easing == Easing.BACK_OUT):
                offset = 1 + (2.70158 * (intervalTime-1)**3) + (1.70158 * (intervalTime-1)**2)
                value = activeKeyframe.value + offset * valueRange

            self.__currentKeyValueDict__[keyString] = value
                
    def SetKey(self, keyString):
        if (not keyString in self.__keyframeDict__):
            raise Exception(f"Inputted key '{key}' does not exist!")
        return self.__currentKeyValueDict__[keyString]
        
    
    def DestroySelf(self):
        self.Stop()
        if (self in app.animationList):
            app.animationList.remove(self)  
        del self
        
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
        
        
class Button:
    def Awake(self):
        pass

    def __init__(self):
        self.group = Group()
        
        self.enabled = True
        
        self.visual = Rect(0, 0, 100, 40, fill='snow', border='gainsboro', borderWidth=4, align='center')
        self.group.add(self.visual)
        self.text = Label("Button", 0, 0, size=16)
        self.group.add(self.text)
        
        app.buttonList.append(self)
        
        self.hoverTint = 'black'
        self.hoverOpacity = 20
        
        self.holdTint = 'black'
        self.holdOpacity = 8
        
        self.isHovered = False # implement this
        
        self.Awake()
        
        self.hoverOverlay = Rect(self.visual.centerX, self.visual.centerY, self.visual.width, self.visual.height, align='center', fill=self.hoverTint, opacity=0)
        self.group.add(self.hoverOverlay)
        self.holdOverlay = Rect(self.visual.centerX, self.visual.centerY, self.visual.width, self.visual.height, align='center', fill=self.holdTint, opacity=0)
        self.group.add(self.holdOverlay)

                
    def OnPressed(self):
        pass
        
    def OnHeld(self):
        pass
        
    def OnReleased(self):
        pass
    
    def OnHeldVisual(self):
        self.holdOverlay.opacity = self.holdOpacity
        self.hoverOverlay.opacity = 0
        
    def OnReleasedVisual(self):
        self.holdOverlay.opacity = 0
        
    def OnHoveredVisual(self):
        self.hoverOverlay.opacity = self.hoverOpacity
        
    def OnUnhoveredVisual(self):
        self.hoverOverlay.opacity = 0
        
        
    def DestroySelf(self):
        self.visual.visible = False
        self.text.visible = False
        self.hoverOverlay.visible = False
        self.holdOverlay.visible = False
        app.buttonList.remove(self)
        if (self in app.heldButtonList):
            app.heldButtonList.remove(self)

    
def Lerp(start, end, t):
    if (t == 0): return start
    elif (t < 0): t *= -1
    elif (t > 1): t = 1
    range = end - start
    increment = range * t
    value = start + increment
    return value
    
    
def Clamp(value, max=None, min=None):
    if (max == None and min == None):
        return value
    elif (max != None or min != None):
        if (max != None and value > max):
            value = max
        if (min != None and value < min):
            value = min
    
    return value
    
    
def Remap01(value, oldMin, oldMax):
    if (oldMin == oldMax):
        return 0
        
    if (oldMin > oldMax):
        tempMax = oldMin
        oldMin = oldMax
        oldMax = tempMax
        
    return ((value - oldMin) / (oldMax - oldMin))

def WorldToCanvasPoint(worldPosition):
    return worldPosition + mainCamera.offset
    
def CanvasToWorldPoint(canvasPosition):
    return canvasPosition - mainCamera.offset
    

app.background = gradient(rgb(101, 105, 110), rgb(120, 128, 140), start='bottom-right')


mainCamera = Camera()

app.gameObjectList = [] 
app.destroyedGameObjectList = []

app.unrenderedGameObjects = 0

app.animationList = []

app.buttonList = []
app.heldButtonList = []


app.background = 'cadetBlue'

app.stepsPerSecond = 60

app.enemyList = []


##### 
#####
#####
#####


class Player(GameObject):
    def Awake(self):
        self.visual = Circle(0,0, 8, fill='dodgerBlue', border='black')
        self.collider = Rect(0,0, 8, 8, opacity=0)
        self.transform.position = Vector2(0, 0)
        
        self.gunVisual = Group(
            Rect(12,0, 15, 4, fill='gray', border='black', borderWidth=1),
            Rect(-12,0, 15, 4, opacity=0)
            )
        
        self.upgradeDict = {}
        
        self.inputDir = Vector2()
        
        self.unrenderBuffer = -1
    
        self.moveSpeed = 160 #*
        
        self.dashBonusSpeed = 160 #*
        self.dashLength = 0.6
        self.dashCooldownTime = 3.5 #*
        self.dashCooldown = 0
        self.dashImmunityLength = 0.3
        self.dashSpeed = 0
        self.dashEasing = Easing.QUAD_OUT
        self.dashDir = Vector2()
        
        class DashAnimation(Animation):
            def Keyframes(self):
                return [
                    Keyframe('width', 16, 0),
                    Keyframe('width', 24, 0.1, Easing.QUART_OUT),
                    Keyframe('width', 16, 0.5, Easing.BACK_OUT),
                    
                    Keyframe('height', 16, 0),
                    Keyframe('height', 13, 0.1, Easing.QUART_OUT),
                    Keyframe('height', 16, 0.5, Easing.BACK_OUT),
                    ]
            def Keys(self):
                rotateAngle = app.player.visual.rotateAngle
                app.player.visual.rotateAngle = 0
                app.player.visual.width = self.SetKey('width')
                app.player.visual.height = self.SetKey('height')
                app.player.visual.rotateAngle = rotateAngle
        self.dashAnimation = DashAnimation()
        
        self.lookDirection = Vector2()
        
        self.bulletSpeed = 700
        self.shootSpeed = 0.2
        self.shootTimer = 0
        self.bulletDamage = 20 #*
        self.shootSoundIndex = 0
        class ShootAnimation(Animation):
            def Keyframes(self):
                return [
                    Keyframe('wid', 39, 0),
                    Keyframe('wid', 34, 0.035, Easing.SIN_OUT),
                    Keyframe('wid', 39, 0.125, Easing.SIN_IN_OUT),
                    ]
            def Keys(self):
                app.player.gunVisual.rotateAngle = 0
                app.player.gunVisual.width = self.SetKey('wid')
                app.player.gunVisual.rotateAngle = app.player.rotateAngle
                app.player.gunVisual.centerX = app.player.visual.centerX
                app.player.gunVisual.centerY = app.player.visual.centerY
        self.shootAnimation = ShootAnimation()
        
        self.grenadeSpeed = 900
        self.grenadeCooldownTime = 7 #*
        self.grenadeCooldown = 0
        self.grenadeDamage = 120 #*
        self.grenadeRadius = 50 #*
        
        self.maxHealth = 50 #*
        self.health = self.maxHealth
        self.immunityLength = 0.5
        self.immunityTimer = 0
        self.regenSpeed = 250 #***
        self.regenTimer = self.regenSpeed / self.maxHealth
        self.hurtSoundIndex = 0
        
        self.money = 0
        
        self.rotateAngle = 0
        
    def Start(self):
        self.dashMotion = PlayerDashMotion()
        self.GainMoney(15)
        
    def Update(self):
        self.inputDir = Vector2()
        
        if (Input.GetKey('w') or Input.GetKey('up')):
            self.inputDir.y += 1
        if (Input.GetKey('s') or Input.GetKey('down')):
            self.inputDir.y -= 1
        if (Input.GetKey('a') or Input.GetKey('left')):
            self.inputDir.x -= 1
        if (Input.GetKey('d') or Input.GetKey('right')):
            self.inputDir.x += 1
        
        moveDir = self.inputDir.normalized * self.moveSpeed
        moveDir = Vector2(moveDir.x + self.dashDir.x * self.dashSpeed, moveDir.y + self.dashDir.y * self.dashSpeed)
        
        if (not app.gameManager.cutscenePlaying):
            mainCamera.position.x = Lerp(mainCamera.position.x, self.transform.position.x, 15 * Time.deltaTime)
            mainCamera.position.y = Lerp(mainCamera.position.y, self.transform.position.y, 15 * Time.deltaTime)
        
        if (moveDir.magnitude <= 3 * self.moveSpeed + 2 * self.dashBonusSpeed):
            self.transform.position.x += moveDir.x * Time.deltaTime
            self.transform.position.y -= moveDir.y * Time.deltaTime
        else:
            print(f"The player is moving too quickly: {moveDir}")
        
        if (self.lookDirection.x == 0 and self.lookDirection.y < 0):
            self.rotateAngle = 90
        elif (self.lookDirection.x == 0 and self.lookDirection.y >= 0):
            self.rotateAngle = 270
        elif (self.lookDirection.x > 0):
            self.rotateAngle = (180/math.pi) * math.atan(-self.lookDirection.y/self.lookDirection.x)
        elif (self.lookDirection.x < 0):
            self.rotateAngle = (180/math.pi) * math.atan(self.lookDirection.y/-self.lookDirection.x) + 180
            
        self.gunVisual.rotateAngle = self.rotateAngle
        self.visual.rotateAngle = self.rotateAngle
        
        self.gunVisual.centerX = self.visual.centerX
        self.gunVisual.centerY = self.visual.centerY
        
        if (self.health == self.maxHealth):
            self.regenTimer = self.regenSpeed / self.maxHealth
            
        self.shootTimer = Clamp(self.shootTimer - Time.deltaTime, min=0)
        self.grenadeCooldown = Clamp(self.grenadeCooldown - Time.deltaTime, min=0)
        self.dashCooldown = Clamp(self.dashCooldown - Time.deltaTime, min=0)
        self.immunityTimer = Clamp(self.immunityTimer - Time.deltaTime, min=0)
        self.regenTimer = Clamp(self.regenTimer - Time.deltaTime, min=0)
        
        if (Input.GetMouse(0) and self.shootTimer == 0):
            self.Shoot()
            
        if ((Input.GetKeyDown('g') or Input.GetMouseDown(1)) and self.grenadeCooldown == 0):
            self.Grenade()
            
        if ((Input.GetKeyDown('space') or Input.GetKeyDown('shift')) and self.dashCooldown == 0):
            self.Dash()
            
        if (self.regenTimer == 0):
            self.Heal(1)
            self.regenTimer = self.regenSpeed / self.maxHealth
            
        # if (Input.GetKeyDown('t')):
        #     self.transform.position = app.teleporter.transform.position.copy()
            
        # if (Input.GetKeyDown('c')):
        #     app.teleporter.charge = 98.9
            
        # if (Input.GetKeyDown('m')):
        #     self.transform.position = Vector2(0, 750)
            
        worldMousePosition = CanvasToWorldPoint(Input.mouse)
        self.lookDirection = Vector2.angleTo(self.transform.position.x, -self.transform.position.y, worldMousePosition.x, -worldMousePosition.y)
        
        
    def DestroySelf(self):
        self.gunVisual.visible = False
        self.dashAnimation.DestroySelf()
        self.dashMotion.DestroySelf()
        super().DestroySelf()    
        
    def Shoot(self):
        PlayerBullet.Shoot(self.transform.position.copy(), self.lookDirection * self.bulletSpeed, self.bulletDamage, self.rotateAngle)
        self.shootTimer = self.shootSpeed
        if (self.shootSoundIndex == 0):
            Audio.PLAYER_SHOOT_1.play(restart=True)
        elif (self.shootSoundIndex == 1):
            Audio.PLAYER_SHOOT_2.play(restart=True)
        self.shootSoundIndex = (self.shootSoundIndex + 1) % 2
        if app.LDM: return #-
        self.shootAnimation.Play(restart=True)
        
    def Grenade(self):
        PlayerGrenade.Throw(self.transform.position.copy(), self.lookDirection * self.grenadeSpeed, self.grenadeDamage, self.grenadeRadius)
        self.grenadeCooldown = self.grenadeCooldownTime
        
    def Dash(self):
        self.dashDir = self.lookDirection.copy()
        self.dashMotion = PlayerDashMotion()
        self.dashMotion.Play(restart=True)
        self.dashCooldown = self.dashCooldownTime
        self.dashAnimation.Play(restart=True)
        
    
    def GainMoney(self, amount):
        self.money += amount
        app.playerHUD.UpdateMoney()
        
    def TakeDamage(self, amount, overrideImmunity=False):
        if (app.gameManager.isLoading):
            return
        if (not overrideImmunity and not (self.immunityTimer == 0 and self.dashCooldownTime - self.dashCooldown > self.dashImmunityLength)):
            return
        self.health = 1 if (self.health >= self.maxHealth/4 and self.health-amount <= 0) else int(self.health-amount)
        app.playerHUD.UpdateHealth()
            
        if (not overrideImmunity):
            self.immunityTimer = self.immunityLength 
        if (self.hurtSoundIndex == 0):
            Audio.PLAYER_HURT_1.play(restart=True)
        elif (self.hurtSoundIndex == 1):
            Audio.PLAYER_HURT_2.play(restart=True)
        elif (self.hurtSoundIndex == 2):
            Audio.PLAYER_HURT_3.play(restart=True)
        self.hurtSoundIndex = (self.hurtSoundIndex + 1) % 3
        
        if (self.health <= 0):
            self.Die()
        
            
            
    def Heal(self, amount):
        self.health = Clamp(self.health + int(amount), max=self.maxHealth)
        app.playerHUD.UpdateHealth()
        
    
    def Die(self):
        app.stop()
        
class PlayerDashMotion(Animation):
    def Keyframes(self):
        return [
            Keyframe('speed', app.player.dashBonusSpeed + app.player.moveSpeed, 0),
            Keyframe('speed', 0, app.player.dashLength, app.player.dashEasing)
            ]
            
    def Keys(self):
        app.player.dashSpeed = self.SetKey('speed')
    
        

class DamageType(Enum):
    BULLET = 'white'
    CRIT = 'yellow'
    EXPLOSION = 'yellow'
    
        
        
class PlayerBullet(GameObject):
    activeBullets = []
    def Awake(self):
        self.visual = Rect(0,0, 20, 0.75, fill=gradient('yellow', 'red', start='right'))
        self.collider = Rect(0,0, 30, .75, opacity=0)
        
        self.damage = 0
        
        self.velocity = Vector2()
        
        self.destroyRadius = 210
    
    def Update(self):
        self.transform.position.x += self.velocity.x * Time.deltaTime
        self.transform.position.y -= self.velocity.y * Time.deltaTime
        
        if ((self.transform.position.x > mainCamera.position.x + self.destroyRadius or self.transform.position.x < mainCamera.position.x - self.destroyRadius) or (self.transform.position.y > mainCamera.position.y + self.destroyRadius or self.transform.position.y < mainCamera.position.y - self.destroyRadius)):
            self.DestroySelf()
                
        
    @staticmethod
    def Shoot(position, velocity, damage, angle):
        bullet = PlayerBullet()
        bullet.transform.position = position
        bullet.velocity = velocity
        bullet.damage = damage
        bullet.visual.rotateAngle = angle
        bullet.collider.rotateAngle = angle
        PlayerBullet.activeBullets.append(bullet)
        return bullet
        
    def DestroySelf(self):
        if (self in PlayerBullet.activeBullets):
            PlayerBullet.activeBullets.remove(self)
        super().DestroySelf()
        
        
        
class PlayerGrenade(GameObject):
    def Awake(self):
        self.visual = Circle(0,0, 8, fill='forestGreen', border='darkGreen')
        self.collider = Circle(0,0, 1, fill=None, opacity=15, border='black', borderWidth=5)
        
        self.damage = 0
        
        self.friction = 4
        self.releasedFrictionMultiplier = 24
        self.velocity = Vector2()
        
        self.radius = 0
        
        self.fuseTimer = 1
        self.fuseVisual = Circle(0,0, 25, fill='red', opacity=10)
    
    def Update(self):
        if (Input.GetKeyUp('g') or Input.GetMouseUp(1)):
            self.friction = self.releasedFrictionMultiplier
        
        fusePercentage = 1 - Remap01(self.fuseTimer, 0, 1)
        self.fuseVisual.radius = Lerp(25, self.radius, fusePercentage)
        
        self.fuseTimer -= Time.deltaTime
        if (self.fuseTimer <= 0):
            self.Explode()
        
        self.velocity *= math.exp(-self.friction * Time.deltaTime)
        
        self.transform.position.x += self.velocity.x * Time.deltaTime
        self.transform.position.y -= self.velocity.y * Time.deltaTime
        
        self.fuseVisual.centerX = self.visual.centerX
        self.fuseVisual.centerY = self.visual.centerY
            
    def Explode(self):
        self.collider.fill = 'red'
        self.fuseVisual.visible = False
        hitEnemies = []
        for enemy in app.enemyList:
            if (self.collider.hitsShape(enemy.collider)):
                hitEnemies.append(enemy)
        for enemy in hitEnemies:
            enemy.Damage(self.damage, DamageType.EXPLOSION)
        self.DestroySelf()
        
    def DestroySelf(self):
        self.fuseVisual.visible = False
        super().DestroySelf()
        
        
        
    @staticmethod
    def Throw(position, velocity, damage, radius):
        grenade = PlayerGrenade()
        grenade.transform.position = position
        grenade.velocity = velocity
        grenade.damage = damage
        grenade.radius = radius
        grenade.collider.radius = radius
        return grenade
        
        
class DamageNumber(GameObject):
    def Awake(self):
        self.visual = Label(0, 0,0, fill='white', size=8.5, bold=True, opacity=75)
        self.velocity = Vector2(random.randint(-35, 35), random.randint(150, 200))
        self.gravity = 700
        self.rotationVelocity = self.velocity.x * 1.25
        
        class OpacityAnimation(Animation):
            def Keyframes(self):
                return [
                    Keyframe('opacity', 75, 0),
                    Keyframe('opacity', 75, 0.3),
                    Keyframe('opacity', 0, .65, Easing.QUAD_IN_OUT)
                    ]
            def Keys(self):
                self.arg1.opacity = Clamp(self.SetKey('opacity'), min=0, max=100)
                    
        self.opacityAnimation = OpacityAnimation()
                
        self.opacityAnimation.Play(arg1=self.visual)
        
        @event_handler(self.opacityAnimation.OnAnimationEnd)
        def OnAnimationEnd(sender, e):
            self.DestroySelf()
            
            
    def Update(self):
        self.velocity.y -= self.gravity * Time.deltaTime
        
        self.visual.rotateAngle += self.rotationVelocity * Time.deltaTime
        
        self.transform.position.x += self.velocity.x * Time.deltaTime
        self.transform.position.y -= self.velocity.y * Time.deltaTime
    
    
    @staticmethod
    def Spawn(position, damage, color='white'):
        num = DamageNumber()
        num.transform.position = position
        num.visual.value = damage
        num.visual.fill = color
        
            
    def DestroySelf(self):
        self.opacityAnimation.DestroySelf()
        super().DestroySelf()
        
        
class Enemy(GameObject):
    def Awake(self):
        
        self.hurtAnimation = EnemyHurtAnim()
        
        self.moneyValue = 0
        
        self.timeSinceLastDamage = 3
        self.healthBarCutoffTime = 3
        
        self.healthBarAnimation = EnemyHealthFadeOutAnim()
        
        self.healthBorder = Rect(0,0, 30, 5, align='center', opacity=0)
        self.healthBar = Rect(0,0, 27, 2, fill=rgb(255, 50, 50), align='center', opacity=0)
        
        self.fromTeleporter = False
    
    def Update(self):
        if (self.unrendered): return
        for bullet in PlayerBullet.activeBullets:
            if (self.collider.hitsShape(bullet.collider)):
                self.Damage(bullet.damage, DamageType.BULLET)
                bullet.DestroySelf()
                break
    
    def LateUpdate(self):
        self.timeSinceLastDamage += Time.deltaTime
        
        if (self.timeSinceLastDamage >= self.healthBarCutoffTime and self.healthBorder.opacity == 100):
            self.healthBarAnimation.Play(restart=True, arg1=self.healthBorder, arg2=self.healthBar)
            
        if (self.healthBorder.opacity != 0):
            self.healthBorder.centerX = self.visual.centerX
            self.healthBar.left = self.healthBorder.left + 1.5
            self.healthBorder.centerY = self.visual.bottom + 5
            self.healthBar.centerY = self.visual.bottom + 5
        
    def Damage(self, damageAmount, damageType):
        self.health -= damageAmount
        if not app.LDM: #-
            DamageNumber.Spawn(self.transform.position.copy(), damageAmount, damageType.value)
        if (self.health <= 0):
            app.player.GainMoney(self.moneyValue)
            self.deathSound.play(restart=True)
            self.DestroySelf()
            return
        
        self.hurtAnimation.Play(restart=True, arg1=self)
        self.timeSinceLastDamage = 0
        self.healthBorder.opacity = 100
        self.healthBar.opacity = 100
        self.healthBarAnimation.Stop()
        
        healthPercent = Remap01(self.health, 0, self.maxHealth)
        self.healthBar.width = Lerp(0, 27, healthPercent)
        
        self.healthBorder.centerX = self.visual.centerX
        self.healthBar.left = self.healthBorder.left + 1.5
        self.healthBorder.centerY = self.visual.bottom + 5
        self.healthBar.centerY = self.visual.bottom + 5
        
    def DestroySelf(self):
        self.healthBorder.visible = False
        self.healthBar.visible = False
        if (self in app.enemyList):
            app.enemyList.remove(self)
        if (self in app.teleporter.teleporterEnemyList):
            app.teleporter.teleporterEnemyList.remove(self)
        self.healthBarAnimation.DestroySelf()
        self.hurtAnimation.DestroySelf()
        super().DestroySelf()
        
        
    @staticmethod    
    def Spawn(position, enemyType, fromTeleporter=False):
        enemy = enemyType()
        enemy.transform.position = position
        enemy.maxHealth *= 1 + 0.3 * (app.difficultyManager.enemyLevel - 1)
        enemy.damage *= 1 + 0.2 * (app.difficultyManager.enemyLevel - 1)
        enemy.health = enemy.maxHealth
        enemy.fromTeleporter = fromTeleporter
        rewardMultiplier = 0.1425 if (not enemy.fromTeleporter) else 0.029
        enemy.moneyValue = 2 * app.difficultyManager.coeff * enemy.monsterValue * rewardMultiplier
        if (enemy.fromTeleporter):
            app.teleporter.teleporterEnemyList.append(enemy)
        app.enemyList.insert(0, enemy)
        return enemy
        
        
        

class EnemyHurtAnim(Animation):
    def Keyframes(self):
        return [
            Keyframe('opacity', 75, 0),
            Keyframe('opacity', 0, 0.3)
            ]
            
    def Keys(self):
        self.arg1.collider.opacity = self.SetKey('opacity')
        
class EnemyHealthFadeOutAnim(Animation):
    def Keyframes(self):
        return [
            Keyframe('opacity', 100, 0),
            Keyframe('opacity', 0, 0.5)
            ]
            
    def Keys(self):
        self.arg1.opacity = self.SetKey('opacity')
        self.arg2.opacity = self.SetKey('opacity')
    
    

class Lemurian(Enemy):
    def Awake(self):
        self.visual = Oval(0,0, 22, 28, fill='darkOrchid', border='black')
        self.collider = Oval(0,0, 22, 28, fill='crimson', opacity=0)
        self.unrenderBuffer = 30
        
        self.moveSpeed = 100
        self.maxHealth = 100
        self.monsterValue = 11
        self.damage = 5
        self.deathSound = Audio.LEMURIAN_DEATH
        
        super().Awake()
        
    def Update(self):
        directionToPlayer = Vector2.angleTo(self.transform.position.x, self.transform.position.y, app.player.transform.position.x, app.player.transform.position.y)
        
        moveDir = directionToPlayer * self.moveSpeed        

        self.transform.position.x += moveDir.x * Time.deltaTime
        self.transform.position.y += moveDir.y * Time.deltaTime
        
        if (distance(app.player.transform.position.x, app.player.transform.position.y, self.transform.position.x, self.transform.position.y) <= 40):
            if (self.collider.hitsShape(app.player.collider)):
                app.player.TakeDamage(self.damage)
        
        super().Update()
        
class Beetle(Enemy):
    def Awake(self):
        self.visual = Oval(0,0, 35, 30, fill='wheat', border='black')
        self.collider = Oval(0,0, 35, 30, fill='crimson', opacity=0)
        self.unrenderBuffer = 30
        
        self.moveSpeed = 75
        self.maxHealth = 50
        self.monsterValue = 8
        self.damage = 3
        self.deathSound = Audio.BEETLE_DEATH
        
        super().Awake()
        
    def Update(self):
        directionToPlayer = Vector2.angleTo(self.transform.position.x, self.transform.position.y, app.player.transform.position.x, app.player.transform.position.y)
        
        moveDir = directionToPlayer * self.moveSpeed        

        self.transform.position.x += moveDir.x * Time.deltaTime
        self.transform.position.y += moveDir.y * Time.deltaTime
        
        if (distance(app.player.transform.position.x, app.player.transform.position.y, self.transform.position.x, self.transform.position.y) <= 40):
            if (self.collider.hitsShape(app.player.collider)):
                app.player.TakeDamage(self.damage)
        
        super().Update()
        
        
class Golem(Enemy):
    def Awake(self):
        self.visual = Group(
            Oval(0,0, 48, 40, fill='dimGray', border='gray', borderWidth=3),
            Circle(0, 7, 5, fill='red', border='black')
            )
        self.collider = Oval(0,0, 48, 40, fill='crimson', opacity=0)
        self.unrenderBuffer = 40
        
        self.moveSpeed = 50
        self.maxHealth = 500
        self.monsterValue = 40
        self.damage = 8
        self.deathSound = Audio.GOLEM_DEATH
        
        super().Awake()
        
    def Update(self):
        directionToPlayer = Vector2.angleTo(self.transform.position.x, self.transform.position.y, app.player.transform.position.x, app.player.transform.position.y)
        
        moveDir = directionToPlayer * self.moveSpeed        

        self.transform.position.x += moveDir.x * Time.deltaTime
        self.transform.position.y += moveDir.y * Time.deltaTime
        
        distToPlayer = distance(app.player.transform.position.x, app.player.transform.position.y, self.transform.position.x, self.transform.position.y)
        if (distToPlayer <= 40):
            if (self.collider.hitsShape(app.player.collider)):
                app.player.TakeDamage(self.damage)
                
        super().Update()
        
        
        
class EnemyType(Enum):
    LEMURIAN = Lemurian
    BEETLE = Beetle
    GOLEM = Golem
        
        
class Stage(GameObject):
    def Awake(self):
        
        self.playerDamageCooldown = 0.4
        self.playerDamageTimer = self.playerDamageCooldown
        self.playerHealthDamagePercent = 0.05
        
        self.transform.position = Vector2()
        
        self.ambientSong = None
        self.bossSong = None
        self.bossOverSong = None
        
        self.basicLevelSize = 5120
        
        self.chests = 25
        
        if (app.gameManager.stage == 1):
            self.ambientSong = Audio.STAGE_1_SONG
            self.bossSong = Audio.STAGE_1_BOSS_SONG
            self.bossOverSong = Audio.STAGE_1_BOSS_OVER
            img = Image('cmu://682887/26659944/noise+background.png', 0,0)
            img.width /= 1.5
            img.height /= 1.5
            self.visual = Group(img, Rect(0,0, self.basicLevelSize, self.basicLevelSize, fill=gradient(rgb(134, 176, 113), rgb(90, 116, 78)), opacity=88))
            app.background = rgb(190, 255, 231)
            self.chests = 24
            Chest.Spawn(Vector2(0, 100))
        if (app.gameManager.stage == 2):
            self.ambientSong = Audio.STAGE_2_SONG
            self.bossSong = Audio.STAGE_2_BOSS_SONG
            self.bossOverSong = Audio.STAGE_2_BOSS_OVER
            img = Image('cmu://682887/26659944/noise+background.png', 0,0)
            img.width *= 2/3
            img.height *= 2/3
            self.visual = Group(img, Rect(0,0, self.basicLevelSize, self.basicLevelSize, fill=gradient(rgb(176, 137, 76), rgb(152, 113, 65)), opacity=88))
            app.background = rgb(239, 237, 222)
            self.chests = 30
        if (app.gameManager.stage == 3):
            self.ambientSong = Audio.STAGE_3_SONG
            self.bossSong = Audio.STAGE_3_BOSS_SONG
            self.bossOverSong = Audio.STAGE_3_BOSS_OVER
            img = Image('cmu://682887/26659944/noise+background.png', 0,0)
            img.width /= 1.5
            img.height /= 1.5
            self.visual = Group(img, Rect(0,0, self.basicLevelSize, self.basicLevelSize, fill=gradient(rgb(115, 59, 140), rgb(70, 45, 126)), opacity=88))
            app.background = rgb(200, 175, 217)
            self.chests = 35
        elif (app.gameManager.stage == 4):
            self.ambientSong = Audio.STAGE_4_SONG
            groundFill = rgb(89, 116, 148)
            self.visual = Group(
                Rect(-20000, 0, 1, 1), Rect(20000, 0, 1, 1), Rect(0, 20000, 1, 1), Rect(0, -20000, 1, 1), 
                Rect(-7500, 15000, 350, 350, align='center'),
                Rect(-7500, 15000, 200, 3750, align='bottom'),
                Circle(-7500, 11250, 200),
                Rect(-7500, 11250, 2121, 200, rotateAngle=-45, align='bottom-left'),
                Rect(-6000, 9750, 425, 425, rotateAngle=-45, align='center'),
                Rect(-6000, 9750, 3000, 200, align='left'),
                Rect(-3000, 9750, 425, 425, align='center'),
                Rect(-3000, 9750, 2250, 200, align='left'),
                RegularPolygon(-750, 9750, 200, 8),
                Rect(-750, 9750, 2121, 200, rotateAngle=-45, align='bottom-left'),
                Circle(750, 8250, 200),
                Rect(750, 8250, 2121, 200, rotateAngle=-45, align='bottom-left'),
                Rect(2250, 6750, 425, 425, rotateAngle=-45, align='center'),
                Rect(2250, 6750, 1060.5, 200, rotateAngle=45, align='bottom-right'),
                RegularPolygon(1500, 6000, 200, 8),
                Rect(1500, 6000, 1500, 200, align='right'),
                Circle(0, 6000, 200),
                Rect(0, 6000, 200, 6000, align='bottom'),
                Circle(0, 0, 600, border='black', borderWidth=10),
                )
            self.visual.fill = groundFill
            app.background = rgb(195, 220, 232)
            self.visual.add(Label("so i planned to have the Mithrix (final boss) fight... but apparently,", 0, -30, size=11, bold=True))
            self.visual.add(Label("CMU CS Academy limits the filesize to only 100KB, so...", 0, -15, size=11, bold=True))
            self.visual.add(Label("CMU devs please increase the filesize limit to like 1MB or something :)", 0, 5, size=11, bold=True))
            self.visual.add(Label("I really wanted to work on this more, but the current filesize restriction", 0, 20, size=11, bold=True))
            self.visual.add(Label("is just a little too limiting for a Teaching Program that's meant to teach", 0, 35, size=11, bold=True))
            self.visual.add(Label("students computer science by allowing them to explore their creativity.", 0, 50, size=11, bold=True))
            self.visual.add(Label("and sorry to anyone else who got here; i literally can't add more to the game :/", 0, 70, size=11, bold=True))
        
        self.ambientSong.play(restart=True, loop=True)
        self.visual.toBack()
        
    def Update(self):
        self.playerDamageTimer = Clamp(self.playerDamageTimer - Time.deltaTime, min=0)
        
        if (self.visual.containsShape(app.player.collider)):
            self.playerDamageTimer = self.playerDamageCooldown
            
        if (self.playerDamageTimer == 0):
            app.player.TakeDamage(app.player.maxHealth*self.playerHealthDamagePercent, overrideImmunity=True)
            self.playerDamageTimer = self.playerDamageCooldown
            
    def DestroySelf(self):
        self.ambientSong.pause()
        self.bossSong.pause()
        self.bossOverSong.pause()
        super().DestroySelf()
            

class UpgradeType(Enum):
    HEALTH = "Max Health"
    BULLET_DAMAGE = "Bullet Damage"
    MOVE_SPEED = "Move Speed"
    DASH_SPEED = "Dash Speed"
    DASH_COOLDOWN = "Dash Cooldown"
    GRENADE_DAMAGE = "Grenade Damage"
    GRENADE_RANGE = "Grenade Range"
    GRENADE_COOLDOWN = "Grenade Cooldown"

            
class Upgrade:
    upgradeList = [UpgradeType.HEALTH, UpgradeType.BULLET_DAMAGE, UpgradeType.MOVE_SPEED, UpgradeType.DASH_SPEED, UpgradeType.DASH_COOLDOWN, UpgradeType.GRENADE_DAMAGE, UpgradeType.GRENADE_RANGE, UpgradeType.GRENADE_COOLDOWN]
    availableUpgradeList = upgradeList.copy()
    
    def TrackUpgrade(upgrade):
        if (not upgrade in app.player.upgradeDict):
            app.player.upgradeDict[upgrade] = 1
        else:
            app.player.upgradeDict[upgrade] += 1
    
    def Health():
        app.player.maxHealth += 25
        app.player.Heal(25)
        Upgrade.TrackUpgrade(UpgradeType.HEALTH)
    
    def BulletDamage():
        app.player.bulletDamage += 16
        Upgrade.TrackUpgrade(UpgradeType.BULLET_DAMAGE)
    
    def MoveSpeed():
        app.player.moveSpeed += 15
        Upgrade.TrackUpgrade(UpgradeType.MOVE_SPEED)
        
    def DashSpeed():
        app.player.dashBonusSpeed += 45
        Upgrade.TrackUpgrade(UpgradeType.DASH_SPEED)
        
    def DashCooldown():
        app.player.dashCooldownTime = Clamp(app.player.dashCooldownTime - 0.375, min=0.5)
        Upgrade.TrackUpgrade(UpgradeType.DASH_COOLDOWN)
        
    def GrenadeDamage():
        app.player.grenadeDamage += 70
        Upgrade.TrackUpgrade(UpgradeType.GRENADE_DAMAGE)
        
    def GrenadeRange():
        app.player.grenadeRadius += 9
        Upgrade.TrackUpgrade(UpgradeType.GRENADE_RANGE)
        
    def GrenadeCooldown():
        app.player.grenadeCooldownTime = Clamp(app.player.grenadeCooldownTime - 0.65, min=1.5)
        Upgrade.TrackUpgrade(UpgradeType.GRENADE_COOLDOWN)
            
            
class UpgradeButton(Button):
    def Awake(self):
        self.upgrade = self.GenerateNewUpgrade()
        self.visual.width = 110
        self.text.centerX = 5
        self.text.size = 12
        self.visual.height = 90
        self.visual.fill = 'powderBlue'
        self.visual.border = 'lightSteelBlue'
        
    def OnReleased(self):
        app.upgradePopup.OnUpgradeChosen(self.upgrade)
        
    def GenerateNewUpgrade(self):
        index = random.randint(0, len(Upgrade.availableUpgradeList)-1)
        upgrade = Upgrade.availableUpgradeList.pop(index)
        self.text.value = upgrade.value
        return upgrade
            
            
class UpgradePopup:
    def __init__(self):
        self.background = Rect(0,0, 400, 400, opacity=75)
        
        self.title1 = Label("CHOOSE AN", 200, 45, size=48, fill='red', bold=True, border='black')
        self.title2 = Label("UPGRADE", 200, 95, size=48, fill='crimson', bold=True, border='black')
        self.subtitle = Label("You can only pick one...", 200, 140, size=24, fill='salmon', bold=True, border='black', borderWidth=1)
        
        self.upgradeButton1 = UpgradeButton()
        self.upgradeButton1.group.centerX = 75
        self.upgradeButton1.group.centerY = 235
        self.upgradeButton2 = UpgradeButton()
        self.upgradeButton2.group.centerX = 200
        self.upgradeButton2.group.centerY = 235
        self.upgradeButton3 = UpgradeButton()
        self.upgradeButton3.group.centerX = 325
        self.upgradeButton3.group.centerY = 235
        
        self.descriptionBox = Rect(200, 345, 375, 50, opacity=50, align='center')
        
        self.descriptionText = Label("-----------------------------------------------------------------", 200, 345, size=14, fill='white')
        
        self.group = Group(
            self.background,
            self.title1,
            self.title2,
            self.subtitle,
            self.upgradeButton1.group,
            self.upgradeButton2.group,
            self.upgradeButton3.group,
            self.descriptionBox,
            self.descriptionText,
            )
        
        self.Hide()
    
    def OnUpgradeChosen(self, upgrade):
        if (upgrade == UpgradeType.HEALTH):
            Upgrade.Health()
        elif (upgrade == UpgradeType.BULLET_DAMAGE):
            Upgrade.BulletDamage()
        elif (upgrade == UpgradeType.MOVE_SPEED):
            Upgrade.MoveSpeed()
        elif (upgrade == UpgradeType.DASH_SPEED):
            Upgrade.DashSpeed()
        elif (upgrade == UpgradeType.DASH_COOLDOWN):
            Upgrade.DashCooldown()
        elif(upgrade == UpgradeType.GRENADE_DAMAGE):
            Upgrade.GrenadeDamage()
        elif (upgrade == UpgradeType.GRENADE_RANGE):
            Upgrade.GrenadeRange()
        elif (upgrade == UpgradeType.GRENADE_COOLDOWN):
            Upgrade.GrenadeCooldown()
        
        self.Hide()
    
    
    def Show(self):
        Time.timeScale = 0
        Upgrade.availableUpgradeList = Upgrade.upgradeList.copy()
        
        self.upgradeButton1.upgrade = self.upgradeButton1.GenerateNewUpgrade()
        self.upgradeButton1.enabled = True
        self.upgradeButton2.upgrade = self.upgradeButton2.GenerateNewUpgrade()
        self.upgradeButton2.enabled = True
        self.upgradeButton3.upgrade = self.upgradeButton3.GenerateNewUpgrade()
        self.upgradeButton3.enabled = True
        
        self.group.visible = True
        self.group.toFront()
        
        app.gameManager.fullscreenShapeVisible = True
        
    def Hide(self):
        Time.timeScale = 1
        
        self.upgradeButton1.enabled = False
        self.upgradeButton2.enabled = False
        self.upgradeButton3.enabled = False
        
        self.group.visible = False
        app.gameManager.fullscreenShapeVisible = False


class Chest(GameObject):
    def Awake(self):
        self.visual = Group(
            Rect(0,0, 30, 20, fill='sandyBrown', align='center', border='sienna'),
            Arc(0, -10, 30, 16, 270, 180, fill='gold', border='yellow')
            )
        
        self.basePrice = 25
        self.price = int(self.basePrice * (app.difficultyManager.coeff**1.25))
        
        self.priceLabelShadow = Label(f"${self.price}", 1, -29, size=16, fill='black', bold=True, opacity=40)
        self.priceLabel = Label(f"${self.price}", 0, -30, size=16, fill='white', bold=True)
        self.visual.add(self.priceLabelShadow)
        self.visual.add(self.priceLabel)
        
        self.collider = Circle(0,-5, 48, opacity=0)
        
        self.unrenderBuffer = 30
        
        self.promptShown = False
        
        
    def Update(self):
        if (Input.GetKeyDown('e') and not app.gameManager.teleporterCharging and not app.upgradePopup.group.visible and self.collider.hitsShape(app.player.collider)):
            if (app.player.money >= self.price):
                app.player.GainMoney(-self.price)
                app.upgradePopup.Show()
                self.priceLabel.visible = False
                app.playerHUD.HideInteract()
                self.DestroySelf()
                
        if app.LDM: return
    
        if (not app.gameManager.teleporterCharging and not self.promptShown and distance(self.collider.centerX, self.collider.centerY, app.player.collider.centerX, app.player.collider.centerY) <= self.collider.radius):
            self.promptShown = True
            app.playerHUD.SetPrompt(f"Open Chest ({self.priceLabel.value})")
        elif (self.promptShown and distance(self.collider.centerX, self.collider.centerY, app.player.collider.centerX, app.player.collider.centerY) > self.collider.radius):
            self.promptShown = False
            app.playerHUD.HideInteract()
                
                
    @staticmethod
    def Spawn(position):
        chest = Chest()
        chest.transform.position = position
        return chest
        
        
class Teleporter(GameObject):
    def Awake(self):
        self.visual = Group(
            Circle(0,0, 1100, opacity=3.5, fill='red'),
            Circle(0,0, 115, opacity=10),
            Circle(0,0, 125, opacity=3),
            Circle(0,0, 110, fill=gradient(rgb(110, 100, 100), rgb(65, 65, 65))),
            Circle(0,0, 80, fill=rgb(90, 75, 75)),
            Circle(0,0, 70, fill=rgb(110, 90, 90)),
            Circle(0,0, 55, fill=gradient(rgb(105, 95, 95), rgb(125, 105, 105))),
            Oval(-72, 0, 80, 20, opacity=4),
            Oval(-87, 0, 32, 22, fill=rgb(55, 45, 45)),
            Oval(-93, 0, 28, 21, fill=rgb(58, 48, 48)),
            Oval(-89, 0, 26, 20, fill=rgb(64, 54, 54)),
            Oval(-84, 0, 38, 18, fill=rgb(70, 60, 60)),
            Oval(-77, 0, 34, 15.5, fill=rgb(75, 65, 65)),
            Oval(-64, 0, 28, 10.75, fill=rgb(80, 70, 70)),
            Oval(-51, 0, 20, 5, fill=rgb(85, 75, 75)),
            Oval(-47, 0, 20, 2, fill=rgb(80, 70, 70)),
            Oval(72, 0, 80, 20, opacity=4),
            Oval(87, 0, 32, 22, fill=rgb(55, 45, 45)),
            Oval(93, 0, 28, 21, fill=rgb(58, 48, 48)),
            Oval(89, 0, 26, 20, fill=rgb(64, 54, 54)),
            Oval(84, 0, 38, 18, fill=rgb(70, 60, 60)),
            Oval(77, 0, 34, 15.5, fill=rgb(75, 65, 65)),
            Oval(64, 0, 28, 10.75, fill=rgb(80, 70, 70)),
            Oval(51, 0, 20, 5, fill=rgb(85, 75, 75)),
            Oval(47, 0, 20, 2, fill=rgb(80, 70, 70)),
            )
        self.visual.width *= 0.8
        self.visual.height *= 0.8
        
        self.unrenderBuffer = 900
        
        self.collider = Circle(0,0, 70, opacity=0)
        self.promptShown = False
        
        self.chargeRange = 240
        self.chargeVisual = Circle(0,0, 1, fill=None, border=gradient('red', 'orangeRed', 'crimson', 'orangeRed', start='left'), borderWidth=5, opacity=0)
        self.chargeVisualFill = Circle(0,0, 1, fill=gradient('gray', 'red'), opacity=0)
        self.chargeVisualFinished = Circle(0,0, 1, fill=gradient('gray', 'darkTurquoise', 'gray'), opacity=0)
        self.chargeOrb = Circle(0,0, 10, fill=rgb(61, 196, 215), border=rgb(61-30, 196-30, 215-30), borderWidth=2)
        self.visual.add(self.chargeVisual)
        self.visual.add(self.chargeVisualFill)
        self.visual.add(self.chargeVisualFinished)
        self.visual.add(self.chargeOrb)
        self.chargeVisualRotateSpeed = 100
        self.chargeScreenVisual = Rect(0,0,400,400, fill='red', opacity=0)
        
        self.hasBeenActivated = False
        self.readyToCharge = False
        self.finishedCharging = False
        self.teleportationActive = False
        
        self.charge = 0
        self.chargeRate = 10/9
        self.teleporterEnemyList = []
        
        self.chargeDisplayBackground = Rect(275, 101.5, 120, 25, fill=gradient('black', 'crimson', start='top-left'), opacity=20)
        self.chargeDisplay = Label("Charging: 0%", 333, 114, size=14, fill='mistyRose', bold=True)        
        self.chargeDisplayShadow = Label("Charging: 0%", self.chargeDisplay.centerX+1.5, self.chargeDisplay.centerY+1.5, size=14, fill='black', bold=True, opacity=20)
        self.chargeDisplay.toFront()
        self.chargeDisplayBackground.visible = False
        self.chargeDisplay.visible = False
        self.chargeDisplayShadow.visible = False
        
        
    def Start(self):
        self.activationAnimation = TeleporterActivationAnimation()
        self.activationCameraAnimation = TeleporterActivationAnimation_Camera()
        self.finishedAnimation = TeleporterFinishedAnimation()
        
        
    def Update(self):
        if (not self.hasBeenActivated and Input.GetKeyDown('e') and self.collider.hitsShape(app.player.collider)):
            self.visual.toBack()
            app.stage.visual.toBack()
            app.stage.ambientSong.pause()
            Audio.TELEPORTER_ACTIVATE.play(restart=True)
            app.stage.bossSong.play(restart=True, loop=True)
            self.activationCameraAnimation = TeleporterActivationAnimation_Camera()
            self.activationAnimation.Play(restart=True)
            self.activationCameraAnimation.Play(restart=True)
            app.gameManager.cutscenePlaying = True
            self.hasBeenActivated = True
            self.promptShown = False
            app.playerHUD.HideInteract()
            
            @event_handler(self.activationCameraAnimation.OnAnimationEnd)
            def OnCameraAnimationOver(sender, e):
                app.gameManager.cutscenePlaying = False
                
            @event_handler(self.activationAnimation.OnAnimationEnd)
            def OnActivationAnimationOver(sender, e):
                self.readyToCharge = True
                self.chargeDisplayBackground.visible = True
                self.chargeDisplayShadow.visible = True
                self.chargeDisplay.visible = True
                app.gameManager.teleporterCharging = True
                app.enemyManager.onNormalTimeScale = False
                
                
        elif (not self.teleportationActive and self.finishedCharging and Input.GetKeyDown('e') and self.collider.hitsShape(app.player.collider)):
            app.gameManager.LoadNextStage()
            self.teleportationActive = True
            self.promptShown = False
            app.playerHUD.HideInteract()
                
        if (self.readyToCharge and not app.LDM):
            self.chargeVisual.rotateAngle += self.chargeVisualRotateSpeed * Time.deltaTime
            
        if (self.readyToCharge):
            if (distance(self.transform.position.x, self.transform.position.y, app.player.transform.position.x, app.player.transform.position.y) <= self.chargeRange):
                self.charge = Clamp(self.charge + self.chargeRate * Time.deltaTime, max=99)
            
            if (self.charge == 99):
                app.enemyManager.spawnsEnabled = False
                if (len(self.teleporterEnemyList) == 0):
                    self.charge = 100
                    
            self.chargeDisplay.value = f"Charging: {int(self.charge)}%"
            self.chargeDisplayShadow.value = self.chargeDisplay.value
            
            if (self.charge >= 100):
                Audio.TELEPORTER_CHARGED.play(restart=True)
                app.stage.bossSong.pause()
                app.stage.bossOverSong.play(restart=True)
                app.gameManager.teleporterCharging = False
                self.finishedAnimation.Play()
                self.readyToCharge = False
                self.finishedCharging = True
                self.chargeDisplayBackground.visible = False
                self.chargeDisplayShadow.visible = False
                self.chargeDisplay.visible = False
                
        if app.LDM: return #-
                
        if (not self.promptShown and not self.hasBeenActivated and distance(self.collider.centerX, self.collider.centerY, app.player.collider.centerX, app.player.collider.centerY) <= self.collider.radius):
            self.promptShown = True
            app.playerHUD.SetPrompt("Activate Teleporter..?")
        elif (not self.teleportationActive and not self.promptShown and self.finishedCharging and distance(self.collider.centerX, self.collider.centerY, app.player.collider.centerX, app.player.collider.centerY) <= self.collider.radius):
            self.promptShown = True
            app.playerHUD.SetPrompt("Enter Teleporter")
        if (self.promptShown and distance(self.collider.centerX, self.collider.centerY, app.player.collider.centerX, app.player.collider.centerY) > self.collider.radius):
            self.promptShown = False
            app.playerHUD.HideInteract()
        
        
    def DestroySelf(self):
        self.activationAnimation.DestroySelf()
        self.activationCameraAnimation.DestroySelf()
        self.finishedAnimation.DestroySelf()
        self.chargeScreenVisual.visible = False
        self.chargeDisplayBackground.visible = False
        self.chargeDisplay.visible = False
        self.chargeDisplayShadow.visible = False
        super().DestroySelf()
                
        
class TeleporterActivationAnimation(Animation):
    def Keyframes(self):
        return [
            Keyframe('orb.r', 61, 0),
            Keyframe('orb.g', 196, 0),
            Keyframe('orb.b', 215, 0),
            Keyframe('orb.r', 61, 2.75),
            Keyframe('orb.g', 196, 2.75),
            Keyframe('orb.b', 215, 2.75),
            Keyframe('orb.r', 32, 2.85),
            Keyframe('orb.g', 117, 2.85),
            Keyframe('orb.b', 126, 2.85),
            Keyframe('orb.r', 157, 4.25, Easing.QUAD_OUT),
            Keyframe('orb.g', 60, 4.25, Easing.QUAD_OUT),
            Keyframe('orb.b', 60, 4.25, Easing.QUAD_OUT),
            
            Keyframe('fillRadius', 0.01, 0),
            Keyframe('fillRadius', 0.01, 2.75),
            Keyframe('fillRadius', 750, 3.5),
            Keyframe('fillOpacity', 0, 0),
            Keyframe('fillOpacity', 0, 2.75),
            Keyframe('fillOpacity', 40, 2.85),
            Keyframe('fillOpacity', 0, 3.25, Easing.QUAD_OUT),
            
            Keyframe('radius', 0.01, 0),
            Keyframe('radius', 0.01, 2.75),
            Keyframe('radius', 240, 4, Easing.SIN_OUT),
            
            Keyframe('opacity', 0, 0),
            Keyframe('opacity', 0, 2.75),
            Keyframe('opacity', 100, 2.85, Easing.CUBIC_OUT),
            Keyframe('opacity', 100, 3.25),
            Keyframe('opacity', 50, 3.75, Easing.QUAD_IN_OUT),
            
            Keyframe('screen', 0, 0),
            Keyframe('screen', 40, 2.25, Easing.SIN_IN),
            Keyframe('screen', 40, 2.8),
            Keyframe('screen', 0, 3.2, Easing.SIN_IN_OUT)
            ]
    def Keys(self):
        app.teleporter.chargeVisual.radius = self.SetKey('radius')
        app.teleporter.chargeVisualFill.radius = self.SetKey('fillRadius')
        app.teleporter.chargeVisual.opacity = self.SetKey('opacity')
        app.teleporter.chargeVisualFill.opacity = self.SetKey('fillOpacity')
        
        app.teleporter.chargeOrb.fill = rgb(self.SetKey('orb.r'), self.SetKey('orb.g'), self.SetKey('orb.b'))
        app.teleporter.chargeOrb.border = rgb(self.SetKey('orb.r')-30, self.SetKey('orb.g')-30, self.SetKey('orb.b')-30)
        
        app.teleporter.chargeScreenVisual.opacity = self.SetKey('screen')
        
class TeleporterActivationAnimation_Camera(Animation):
    def Keyframes(self):
        telX = app.teleporter.transform.position.x
        telY = app.teleporter.transform.position.y
        return [
            Keyframe('cam.x', app.player.transform.position.x, 0),
            Keyframe('cam.y', app.player.transform.position.y, 0),
            Keyframe('cam.x', telX, 0.25, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY, 0.25, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX, 0.3),
            Keyframe('cam.y', telY, 0.3),
            Keyframe('cam.x', telX + 2, 0.4, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 2, 0.4, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 1, 0.5, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 5, 0.5, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 3, 0.6, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 3, 0.6, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 6, 0.7, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 3, 0.7, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 5, 0.8, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 4, 0.8, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 3, 0.9, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 8, 0.9, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 3, 1.0, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 6, 1.0, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 10, 1.1, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 5, 1.1, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 6, 1.2, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 5, 1.2, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 4, 1.3, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 10, 1.3, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 7, 1.4, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 4, 1.4, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 11, 1.5, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 7, 1.5, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 5, 1.6, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 5, 1.6, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 5, 1.7, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 10, 1.7, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 7, 1.8, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 4, 1.8, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 6, 1.9, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 11, 1.9, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 5, 2.0, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 8, 2.0, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 7, 2.1, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 3, 2.1, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 5, 2.2, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 5, 2.2, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX + 3, 2.3, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY - 3, 2.3, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 4, 2.4, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 3, 2.4, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 3, 2.5, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 1, 2.5, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX - 5, 2.6, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY + 3, 2.6, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX, 2.65, Easing.SIN_IN_OUT),
            Keyframe('cam.y', telY, 2.65, Easing.SIN_IN_OUT),
            Keyframe('cam.x', telX, 3.25),
            Keyframe('cam.y', telY, 3.25),
            ]
    def Keys(self):
        mainCamera.position.x = self.SetKey('cam.x')
        mainCamera.position.y = self.SetKey('cam.y')
        
class TeleporterFinishedAnimation(Animation):
    def Keyframes(self):
        return [
            Keyframe('radius', 240, 0),
            Keyframe('radius', 0.01, 0.4, Easing.SIN_IN_OUT),
            
            Keyframe('opacity', 50, 0),
            Keyframe('opacity', 0, 0.5, Easing.QUAD_OUT),
            
            Keyframe('swoosh', 750, 0),
            Keyframe('swoosh', 0.01, 0.15, Easing.SIN_OUT),
            Keyframe('swooshOp', 0, 0),
            Keyframe('swooshOp', 35, 0.075),
            Keyframe('swooshOp', 0, 0.125, Easing.SIN_OUT),
            
            Keyframe('orb.r', 157, 0),
            Keyframe('orb.g', 60, 0),
            Keyframe('orb.b', 60, 0),
            Keyframe('orb.r', 157, 0.1),
            Keyframe('orb.g', 60, 0.1),
            Keyframe('orb.b', 60, 0.1),
            Keyframe('orb.r', 32, 0.2),
            Keyframe('orb.g', 117, 0.2),
            Keyframe('orb.b', 126, 0.2),
            Keyframe('orb.r', 61, 1.3, Easing.QUAD_OUT),
            Keyframe('orb.g', 196, 1.3, Easing.QUAD_OUT),
            Keyframe('orb.b', 215, 1.3, Easing.QUAD_OUT),
            ]
        
    def Keys(self):
        app.teleporter.chargeVisual.radius = self.SetKey('radius')
        app.teleporter.chargeVisual.opacity = self.SetKey('opacity')
        
        app.teleporter.chargeVisualFinished.radius = self.SetKey('swoosh')
        app.teleporter.chargeVisualFinished.opacity = self.SetKey('swooshOp')
        
        app.teleporter.chargeOrb.fill = rgb(self.SetKey('orb.r'), self.SetKey('orb.g'), self.SetKey('orb.b'))
        app.teleporter.chargeOrb.border = rgb(self.SetKey('orb.r')-30, self.SetKey('orb.g')-30, self.SetKey('orb.b')-30)
        
        
class EnemyManager(GameObject):
    def Awake(self):
        self.enemyTypeList = [
            EnemyType.LEMURIAN, EnemyType.LEMURIAN,
            EnemyType.BEETLE, EnemyType.BEETLE, EnemyType.BEETLE,
            EnemyType.GOLEM
            ]
        self.waveLengthRange = Vector2(5.0, 10.0)
        self.enemyIntervalRange = Vector2(1.5, 4.0)
        self.waveGapRange = Vector2(20.0, 45.0)
        self.randomEnemyChance = 12 # defined as one enemy for every __ seconds (on average)
        self.randomEnemyChanceTimer = 1
        self.normalTimeScale = 1
        self.teleporterTimeScale = self.normalTimeScale * 2.5
        self.timeScale = 1
        self.spawnsEnabled = True
        
        self.waveLengthTimer = 0
        self.enemyIntervalTimer = 0
        self.waveGapTimer = 10
        
        self.waveActive = False
        
        self.onNormalTimeScale = True
        
        
    def Update(self):
        self.normalTimeScale = 1 + app.difficultyManager.coeff/4
        self.teleporterTimeScale = self.normalTimeScale * 4
        self.timeScale = self.normalTimeScale if (self.onNormalTimeScale) else self.teleporterTimeScale
        if (not self.spawnsEnabled or len(app.enemyList) >= 50):
            return
        if (self.waveActive):
            self.waveLengthTimer -= Time.deltaTime * self.timeScale
            self.enemyIntervalTimer -= Time.deltaTime * self.timeScale
            if (self.enemyIntervalTimer <= 0):
                self.SpawnEnemy()
            if (self.waveLengthTimer <= 0):
                self.waveGapTimer = random.uniform(self.waveGapRange.x, self.waveGapRange.y)
                self.waveActive = False
        else:
            self.waveGapTimer -= Time.deltaTime * self.timeScale
            if (self.waveGapTimer <= 0):
                self.StartWave()
            self.randomEnemyChanceTimer -= Time.deltaTime * self.timeScale
            if (self.randomEnemyChanceTimer <= 0):
                num = random.randint(1, self.randomEnemyChance)
                if (num == 1):
                    self.SpawnEnemy()
                self.randomEnemyChanceTimer = 1
            
    
    
    def StartWave(self):
        self.waveActive = True
        self.waveLengthTimer = random.uniform(self.waveLengthRange.x, self.waveLengthRange.y)
        self.SpawnEnemy()
        
    def SpawnEnemy(self):
        self.enemyIntervalTimer = random.uniform(self.enemyIntervalRange.x, self.enemyIntervalRange.y)
        enemyType = random.choice(self.enemyTypeList)
        posX = 0
        while (posX >= -125 and posX <= 125):
            posX = random.randint(-210, 210)
        posY = 0
        while (posY >= -125 and posY <= 125):
            posY = random.randint(-210, 210)
        position = Vector2(app.player.transform.position.x + posX, app.player.transform.position.y + posY)
        enemy = Enemy.Spawn(position, enemyType.value, fromTeleporter=not self.onNormalTimeScale)
        
        
class GameManager(GameObject):
    def Awake(self):
        self.stage = 1
        self.cutscenePlaying = False
        self.teleporterCharging = False
        
        self.fullscreenShapeVisible = False
        
        self.isLoading = False
        self.loadStageBuffer = 3
        self.loadStageTimer = self.loadStageBuffer
        
        self.loadScreen = Rect(0,0, 400, 400, opacity=0, visible=False)
        
        class LoadScreenAnimation(Animation):
            def Keyframes(self):
                return [
                    Keyframe('opacity', 0, 0),
                    Keyframe('opacity', 100, 1, Easing.QUAD_IN_OUT),
                    Keyframe('opacity', 100, 3),
                    Keyframe('opacity', 0, 4, Easing.QUAD_IN_OUT),
                    ]
            def Keys(self):
                app.gameManager.loadScreen.opacity = self.SetKey('opacity')
        self.loadScreenAnimation = LoadScreenAnimation()
        
        @event_handler(self.loadScreenAnimation.OnAnimationEnd)
        def OnLoadScreenAnimationEnd(sender, e):
            self.loadScreen.visible = False
            self.fullscreenShapeVisible = False
        
    def Update(self):
        if (self.isLoading):
            self.loadStageTimer -= Time.deltaTime
            if (self.loadStageTimer <= self.loadStageBuffer - 1):
                DeleteStage()
            if (self.loadStageTimer <= 0):
                self.stage += 1
                app.difficultyManager.stageLabel.value = f"Stage {self.stage}"
                app.difficultyManager.stageLabelShadow.value = f"Stage {self.stage}"
                app.difficultyManager.StageCompleted()
                app.player.Heal(99999)
                app.player.money = 0
                app.playerHUD.UpdateMoney()
                if (self.stage == 4):
                    StartCommencement()
                else:
                    StartStage()
                    app.enemyManager.spawnsEnabled = True
                    app.enemyManager.onNormalTimeScale = True
                self.loadScreen.toFront()
                self.isLoading = False
                self.loadStageTimer = self.loadStageBuffer
                
    def LoadNextStage(self):
        self.isLoading = True
        self.loadScreen.visible = True
        self.loadScreen.toFront()
        self.loadScreenAnimation.Play(restart=True)
        self.fullscreenShapeVisible = True
        
class DifficultyType:
        def __init__(self, name, size, r, g, b):
            self.name = name
            self.r = r
            self.g = g
            self.b = b
            self.color = rgb(r, g, b)
            self.border = rgb(r-20, g-20, b-20)
            self.size = size
        
class Difficulty:
    EASY = DifficultyType("Easy", 13, 73, 167, 47)
    MEDIUM = DifficultyType("Medium", 12.5, 177, 141, 41)
    HARD = DifficultyType("Hard", 14, 170, 93, 59)
    VERY_HARD = DifficultyType("Very Hard", 13, 183, 67, 45)
    INSANE = DifficultyType("Insane", 13, 159, 72, 72)
    IMPOSSIBLE = DifficultyType("Impossible", 12, 118, 62, 87)
    I_SEE_YOU = DifficultyType("I SEE YOU", 12, 98, 53, 76)
    IM_COMING_FOR_YOU = DifficultyType("I'M COMING FOR YOU", 10, 55, 21, 43)
    HAHAHAHA = DifficultyType("HAHAHAHAHAHAHAHA", 10, 214, 61, 85)
        
class DifficultyManager(GameObject):
    def Awake(self):
        self.clockDisplayHand = Group(
            Rect(295, 25, 10, 1.3, align='left'),
            Rect(295, 25, 10, 1.3, align='right', opacity=0),
            )
        self.clockDisplay = Group(
            Circle(295, 25, 13, fill='white', border='black', borderWidth=1.2),
            self.clockDisplayHand,
            )
            
        class TickingAnimation(Animation):
            def Keyframes(self):
                return [
                    Keyframe('rotateAngle', -90, 0),
                    Keyframe('rotateAngle', -90, 0.75),
                    Keyframe('rotateAngle', -45, 1, Easing.BACK_OUT),
                    Keyframe('rotateAngle', -45, 1.75),
                    Keyframe('rotateAngle', 0, 2, Easing.BACK_OUT),
                    Keyframe('rotateAngle', 0, 2.75),
                    Keyframe('rotateAngle', 45, 3, Easing.BACK_OUT),
                    Keyframe('rotateAngle', 45, 3.75),
                    Keyframe('rotateAngle', 90, 4, Easing.BACK_OUT),
                    Keyframe('rotateAngle', 90, 4.75),
                    Keyframe('rotateAngle', 135, 5, Easing.BACK_OUT),
                    Keyframe('rotateAngle', 135, 5.75),
                    Keyframe('rotateAngle', 180, 6, Easing.BACK_OUT),
                    Keyframe('rotateAngle', 180, 6.75),
                    Keyframe('rotateAngle', 235, 7, Easing.BACK_OUT),
                    Keyframe('rotateAngle', 235, 7.75),
                    Keyframe('rotateAngle', 270, 8, Easing.BACK_OUT),
                    ]
                    
            def Keys(self):
                app.difficultyManager.clockDisplayHand.rotateAngle = self.SetKey('rotateAngle')
            
        self.tickingAnimation = TickingAnimation()
        self.tickingAnimation.Play()
        self.tickingAnimation.looping = True
        
        self.timerBackground = Rect(395, 5, 120, 40, fill='dimGray', border='black', align='top-right', opacity=13)
        self.timerLabel = Label("00:00", 385, 25, size=22, fill='white', font='monospace', bold=True, align='right')
        self.timerLabelShadow = Label(self.timerLabel.value, self.timerLabel.centerX + 2, self.timerLabel.centerY + 2, size=self.timerLabel.size, fill='black', bold=True, font=self.timerLabel.font, opacity=20)
        self.timerLabel.toFront()
        
        self.timer = 0
        
        self.difficultyBar = Rect(275, 50, 120, 30, fill='green', border='black')
        self.difficultyLines = Group(
            Line(355, 50 + self.difficultyBar.borderWidth, 355, 80 - self.difficultyBar.borderWidth),
            Line(315, 50 + self.difficultyBar.borderWidth, 315, 80 - self.difficultyBar.borderWidth),
            )
        self.difficultyArrow = Polygon(275, 54, 282, 47, 268, 47, fill='white', border='black', borderWidth=1)
        self.difficultyLabel = Label("", 335, 65, size=10, fill='white', bold=True)
        
        self.stageLabel = Label("Stage 1", 275, 90, size=14, fill='white', bold=True, align='left')
        self.stageLabelShadow = Label(self.stageLabel.value, self.stageLabel.centerX + 1.5, self.stageLabel.centerY + 1.5, size=14, fill='black', bold=True, opacity=20)
        self.stageLabel.toFront()
        
        self.levelLabel = Label("Lv. 1", 388, 90, size=14, fill='white', bold=True, align='right')
        self.levelLabelShadow = Label(self.levelLabel.value, self.levelLabel.centerX + 1.5, self.levelLabel.centerY + 1.5, size=14, fill='black', bold=True, opacity=20)
        self.levelLabel.toFront()
        
        
        self.timeFactor = .25 #.25 (0.1012 real game)
        self.stageFactor = 1
        self.coeff = self.CalculateCoeff()
        self.enemyLevel = self.CalculateEnemyLevel()
        
        self.group = Group(
            self.timerBackground,
            self.clockDisplay,
            self.clockDisplayHand,
            self.timerLabelShadow,
            self.timerLabel,
            self.difficultyBar,
            self.difficultyLines,
            self.difficultyArrow,
            self.difficultyLabel,
            self.stageLabelShadow,
            self.stageLabel,
            self.levelLabelShadow,
            self.levelLabel,
            )
        
        
    def CalculateCoeff(self):
        return (1 + self.timeFactor * (self.timer/60)) * self.stageFactor
        
    def CalculateEnemyLevel(self):
        return Clamp(int(1 + (self.coeff - 1) * 3), max=99)
        
    def StageCompleted(self):
        self.stageFactor = 1.15 ** (app.gameManager.stage - 1)
        self.coeff *= 1.25
            
        
    def DestroySelf(self):
        self.group.visible = False
        self.tickingAnimation.DestroySelf()
        super().DestroySelf()
        
    
    def Update(self):
        if (not app.gameManager.fullscreenShapeVisible):
            self.group.toFront()
        
        self.timer += Time.deltaTime
        rawTimer = str(datetime.timedelta(seconds=int(self.timer)))
        if (self.timer >= 3600):
            self.timerLabel.value = rawTimer
            self.timerLabel.size = 16.5
        else:
            self.timerLabel.value = rawTimer[slice(2, len(rawTimer))]
        self.timerLabelShadow.value = self.timerLabel.value
            
        self.coeff = self.CalculateCoeff()
        
        self.oldEnemyLevel = self.enemyLevel
        self.enemyLevel = self.CalculateEnemyLevel()
        if (self.oldEnemyLevel != self.enemyLevel):
            self.levelLabel.value = f"Lv. {self.enemyLevel}"
            self.levelLabelShadow.value = self.levelLabel.value
            
        
        difficulty = None
        
        if (self.coeff > 9):
            difficulty = Difficulty.HAHAHAHA
        elif (self.coeff > 8):
            difficulty = Difficulty.IM_COMING_FOR_YOU
        elif (self.coeff > 7):
            difficulty = Difficulty.I_SEE_YOU
        elif (self.coeff > 6):
            difficulty = Difficulty.IMPOSSIBLE
        elif (self.coeff > 5):
            difficulty = Difficulty.INSANE
        elif (self.coeff > 4):
            difficulty = Difficulty.VERY_HARD
        elif (self.coeff > 3):
            difficulty = Difficulty.HARD
        elif (self.coeff > 2):
            difficulty = Difficulty.MEDIUM
        else:
            difficulty = Difficulty.EASY
        
        if (difficulty == Difficulty.HAHAHAHA):
            if (self.difficultyLines.visible):
                self.difficultyLines.visible = False
                self.difficultyArrow.visible = False
            self.difficultyBar.fill = gradient(difficulty.color, 'black', start='left')
            self.difficultyBar.border = gradient('black', difficulty.border, start='left')
            self.difficultyLabel.value = difficulty.name
            self.difficultyLabel.size = difficulty.size
            return
        
        self.difficultyArrow.centerX = Lerp(0, self.difficultyBar.width, self.coeff - int(self.coeff)) + self.difficultyBar.left

        self.difficultyLabel.value = difficulty.name
        self.difficultyLabel.size = difficulty.size
        self.difficultyBar.fill = difficulty.color
        self.difficultyBar.border = 'black'
        self.difficultyLines.fill = difficulty.border
        


class PlayerHUD(GameObject):
    def Awake(self):
        self.e = Label("E  ", 250, 300, fill='yellow', bold=True, size=11)
        self.prompt = Label("", self.e.right, self.e.centerY, size=10, fill='white', bold=True, align='left')
        self.background = Rect(self.e.left-2, self.e.top-3, self.prompt.right-self.e.left+5, self.prompt.bottom-self.e.top+6, fill=gradient('black', 'gray', start='left'), opacity=20)
        self.interactGroup = Group(
            self.background,
            self.e,
            self.prompt
            )
        
        self.moneyBackground = Rect(10, 10, 80, 25, fill=gradient('black', rgb(245, 220, 178), start='left'), border='black', borderWidth=2, opacity=30)
        self.moneySignShadow = Label('$', 19, 22.5, size=16, fill='black', bold=True, opacity=75)
        self.moneySign = Label('$', 18, 21.5, size=16, fill=rgb(254, 251, 196), bold=True)
        self.moneyLabelShadow = Label(0, 85, 22.5, size=16, fill='black', bold=True, align='right', opacity=75)
        self.moneyLabel = Label(0, 84, 21.5, size=16, fill=rgb(245, 220, 178), bold=True, align='right')
        
        self.visualMoney = 0
        self.moneyAnimationPlaying = False
        
        self.healthBarBackground = Rect(10, 390, 164, 19, align='bottom-left')
        self.healthBar = Rect(12, 388, 160, 15, align='bottom-left', fill=rgb(98, 145, 56))
        self.healthLabelShadow = Label(f"{app.player.health} / {app.player.maxHealth}", 93, 381.5, size=13, bold=True)
        self.healthLabel = Label(f"{app.player.health} / {app.player.maxHealth}", 92, 380.5, fill='white', size=13, bold=True)
        
        self.group = Group(
            self.interactGroup,
            self.moneyBackground,
            self.moneySignShadow,
            self.moneySign,
            self.moneyLabelShadow,
            self.moneyLabel,
            self.healthBarBackground,
            self.healthBar,
            self.healthLabelShadow,
            self.healthLabel
            )
        
        self.HideInteract()
        
    def Update(self):
        if (not app.gameManager.fullscreenShapeVisible):
            self.group.toFront()
        if (self.moneyAnimationPlaying):
            self.visualMoney = Lerp(self.visualMoney, app.player.money + 1, 1.75 * Time.deltaTime)
            if (int(self.visualMoney) >= app.player.money):
                self.visualMoney = app.player.money
                self.moneyAnimationPlaying = False
            self.moneyLabel.value = int(self.visualMoney)
            self.moneyLabel.right = 84
            self.moneyLabelShadow.value = self.moneyLabel.value
            self.moneyLabelShadow.right = 85
        
    def ShowInteract(self):
        self.interactGroup.visible = True
        
    def HideInteract(self):
        self.interactGroup.visible = False
        
    def SetPrompt(self, text):
        self.prompt.value = text
        self.prompt.left = self.e.right
        self.background.width = self.prompt.right-self.e.left+5
        self.background.height = self.prompt.bottom-self.e.top+6
        self.ShowInteract()
        
    def UpdateMoney(self):
        self.moneyAnimationPlaying = True
        
    def UpdateHealth(self):
        self.healthLabel.value = f"{app.player.health} / {app.player.maxHealth}"
        self.healthLabelShadow.value = self.healthLabel.value
        healthPercent = Remap01(app.player.health, 0, app.player.maxHealth)
        self.healthBar.width = Clamp((self.healthBarBackground.width-4) * healthPercent, min=0.01)
        self.healthBar.left = self.healthBarBackground.left + 2
        
        
class Minimap(GameObject):
    def Awake(self):
        self.background = Rect(10, 40, 80, 80, fill='dimGray', border='black', opacity=25)
        self.playerDot = Circle(0, 0, 2.25, fill='white', border='black', borderWidth=0.75)
        
    def Update(self):
        if (not app.gameManager.fullscreenShapeVisible):
            self.background.toFront()
            self.playerDot.toFront()
        unmappedPosition = app.player.transform.position.copy()
        unmappedPosition.x /= 64
        unmappedPosition.y /= 64
        mappedPosition = Vector2(Clamp(unmappedPosition.x + self.background.left + self.background.width/2, min=self.background.left, max=self.background.right), Clamp(unmappedPosition.y + self.background.top + self.background.height/2, min=self.background.top, max=self.background.bottom))
        self.playerDot.centerX = mappedPosition.x
        self.playerDot.centerY = mappedPosition.y
    
    def DestroySelf(self):
        self.background.visible = False
        self.playerDot.visible = False
        super().DestroySelf()
        

class TutorialScreen(GameObject):
    def Awake(self):
        self.text = Group(
            Label("PETRICHOR V", 200, 45, size=38, fill='peachPuff', bold=True, borderWidth=.3, border='gray'),
            Label("-- Alien Planet --", 200, 75, size=20, fill=rgb(245, 202, 174), bold=True, italic=True, borderWidth=.23, border='gray'),
            Label("You are equipped with:", 200, 240, fill='gainsboro', bold=True, size=20),
            Label("Your blaster (LMB)", 200, 265, fill='oldLace', size=14, bold=True),
            Label("Many, many grenades (RMB / G)", 200, 285, fill='honeydew', size=14, bold=True),
            Label("A snappy dash (Space)", 200, 305, fill='aliceBlue', size=14, bold=True),
            Label("The ability to interact (E)", 200, 325, fill='oldLace', size=14, bold=True),
            Label("* For the best experience, turn on sound!", 200, 353, fill='whiteSmoke', size=12, italic=True),
            Label("Press SPACE to continue... (or press L for Low Detail Mode)", 200, 385, size=14.5, italic=True, fill='white')
            )
        self.loading = False
        
        paragraph = Group (
            Label("You were tasked with landing here to look for survivors. After touchdown,",0,0),
            Label("though, you attracted some unwanted attention from the local inhabitants.",0,0),
            Label("Now, you must escape by locating and using Teleporters, mysterious altars",0,0),
            Label("crafted out of alien material. Unfortunately, you aren't quite sure where",0,0),
            Label("they are. Search around the map to find these powerful structures. But",0,0),
            Label("first, scavenge the area for any useful items. Some say that loot crates",0,0),
            Label("had fallen off of the main ship. Don't take too long! The creatures here",0,0),
            Label("seem to become more agitated the longer you spend on their planet.",0,0),
            )
            
        for i in range(len(paragraph.children)):
            text = paragraph.children[i]
            text.centerY = 106 + i*15
            text.size = 11.75
            text.left = 8
            text.fill='white'
            shadow = Label(text.value, text.centerX+.5, text.centerY+.5, size=text.size, opacity=50)
            self.text.add(shadow)
        self.text.add(paragraph)
        
    def Update(self):
        if (self.loading):
            self.Hide()
            return
        if (Input.GetKeyDown('l')):
            app.LDM = True
        if (Input.GetKeyDown('space') or Input.GetKeyDown('l')):
            self.text.visible = False
            self.text = Group(
                Rect(0,0, 400,400),
                Label("LOADING...", 20, 380, fill='white', size=32, bold=True, align='bottom-left')
                )
            if app.LDM:
                self.text.add(Label("LOW DETAIL MODE", 20, 345, fill='white', size=15, bold=True, align='bottom-left'))
            self.loading = True
            
    def Hide(self):
        Start()
        self.text.visible = False
        self.DestroySelf()
        
        
def DeleteStage():
    app.stage.DestroySelf()
    app.teleporter.DestroySelf()
    for gameObject in app.gameObjectList:
        if (isinstance(gameObject, Chest)):
            gameObject.DestroySelf()
    enemyList = app.enemyList.copy()
    for enemy in enemyList:
        enemy.DestroySelf()
    del enemyList
    
def StartStage():
    app.player.transform.position = Vector2(0, 0)
    
    app.stage = Stage()

    app.teleporter = Teleporter()
    posX = 0
    posY = 0
    while (posX >= -600 and posX <= 600):
        posX = random.randint(int(-app.stage.visual.width/2+200), int(app.stage.visual.width/2-200))
    while (posY >= -600 and posY <= 600):
        posY = random.randint(int(-app.stage.visual.height/2+200), int(app.stage.visual.height/2-200))
    app.teleporter.transform.position = Vector2(posX, posY)
    
    chestSpawnAmount = app.stage.chests
    
    for i in range(chestSpawnAmount):
        positionX = random.randint(int(-app.stage.visual.width/2), int(app.stage.visual.width/2))
        positionY = random.randint(int(-app.stage.visual.height/2), int(app.stage.visual.height/2))
        Chest.Spawn(Vector2(positionX, positionY))
        
    app.player.gunVisual.toFront()
    app.player.visual.toFront()
    
    
    
def StartCommencement():
    app.stage = Stage()
    app.player.transform.position = Vector2(-7500, 15000)
    app.enemyManager.DestroySelf()
    app.minimap.DestroySelf()

def Start():
    app.player = Player()
    
    app.difficultyManager = DifficultyManager()
    
    app.gameManager = GameManager()
    
    app.upgradePopup = UpgradePopup()
    
    app.enemyManager = EnemyManager()
    
    app.playerHUD = PlayerHUD()
    
    app.minimap = Minimap()
    
    StartStage()
    
app.LDM = False
TutorialScreen()


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
        if (not button.enabled): return
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
        if (not button.enabled): return
        if (button.visual.hits(x, y)):
            button.OnHoveredVisual()
        else:
            button.OnUnhoveredVisual()
        
def onMouseDrag(x, y):
    Input.lastMouse = Vector2(Input.mouse.x, Input.mouse.y)
    Input.mouse = Vector2(x, y)
    
    for button in app.buttonList:
        if (not button.enabled): return
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
        if (not button.enabled): return
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
        if (not button.enabled): return
        if (button in app.heldButtonList):
            app.heldButtonList.remove(button)
            button.OnReleasedVisual()
            if (button.visual.hits(x, y)):
                button.OnReleased()
                
                
                
                
                