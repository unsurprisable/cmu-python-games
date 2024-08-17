# May 2024

from time import time
from enum import Enum
import math
import random


##### background stuff #####

app.stepsPerSecond = 240
class Time:
    deltaTime = 0
    lastTime = -1
    timeScale = 1
    def Update():
        if (Time.lastTime != -1):
            Time.deltaTime = (time() - Time.lastTime) * Time.timeScale
        Time.lastTime = time()



class Vec:
    down = lambda: Vec(0, -1)
    up = lambda: Vec(0, 1)
    left = lambda: Vec(-1, 0)
    right = lambda: Vec(1, 0)
    one = lambda: Vec(1, 1)
    zero = lambda: Vec(0, 0)
    
    magnitude = lambda self: math.sqrt(self.x**2 + self.y**2)
    tuple = lambda self: (self.x, self.y)
    normalized = lambda self: Vec(self.x/self.magnitude(), self.y/self.magnitude()) if (self.magnitude() != 0) else Vec.zero()
    
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def mul(self, val):
        return Vec(self.x*val, self.y*val)
    def div(self, val):
        return Vec(self.x/val, self.y/val)
    def add(self, other):
        return Vec(self.x+other.x, self.y+other.y)
    def sub(self, other):
        return Vec(self.x-other.x, self.y-other.y)
    def __eq__(self, other):
        if (not isinstance(other, Vec)):
            raise TypeError(f"Unsupported operand '==': Vec and {type(other)}")
        return self.x == other.x and self.y == other.y
        
    def copy(self):
        return Vec(self.x, self.y)
    def getSigns(self):
        xSign = 1 if (self.x >= 0) else -1
        ySign = 1 if (self.y >= 0) else -1
        return Vec(xSign, ySign)
    def randint(self):
        return random.randint(self.min, self.max)
        
    @property
    def min(self):
        return self.x
    @min.setter
    def min(self, val):
        self.x = val
    @property
    def max(self):
        return self.y
    @max.setter
    def max(self, val):
        self.y = val
    
    @staticmethod
    def Dist(origin, other):
        return math.dist(origin.tuple(), other.tuple())
    @staticmethod
    def AngleTo(origin, other):
        difference = other.sub(origin)
        return difference.normalized()
    @staticmethod
    def VecTo(origin, other):
        return other.sub(origin)



class Input:
    lastMouse = Vec.zero()
    mouse = Vec.zero()

    kDown = set()
    kUp = set()
    kHeld = set()

    empty = [False, False, False]
    mDown = empty.copy()
    mUp = empty.copy()
    mHeld = empty.copy()

    def GetKeyDown(key):
        return key in Input.kDown

    def GetKeyUp(key):
        return key in Input.kUp

    def GetKey(key):
        return key in Input.kHeld

    def GetMouseDown(button):
        return Input.mDown[button]

    def GetMouseUp(button):
        return Input.mUp[button]

    def GetMouse(button):
        return Input.mHeld[button]
        
    def Update():
        Input.kDown.clear()
        Input.kUp.clear()
        Input.kHeld.clear()
        Input.mDown = Input.empty.copy()
        Input.mUp = Input.empty.copy()
        

            
def Lerp(start, end, t):
    t = max(0, min(1, t))
    return start + (end - start) * t
    
def randDir():
    return 1 if (random.randint(0, 1) == 1) else -1

##### background stuff #####


# app.speed = Label(0, 200, 175, fill='white', border='black', size=14, borderWidth=0.25, bold=True)

app.deathScreen = Group(
    Rect(0,0,400,400, opacity=75),
    Label("welp, you died.", 200,175, size=42, fill='white', bold=True),
    Label("but you can unpause to continue", 200,215, size=20, fill='white', bold=False),
    )
app.deathScreen.visible = False

class Player:
    width, height = (6.3, 11.2)
    def __init__(self, pos):
        self.physicalHitbox = Rect(200,200, Player.width, Player.height, fill='blue', border='black', opacity=0, align='center')
        self.triggerHitbox = Rect(200,200, Player.width*.75, Player.height*.75, fill='red', border='black', opacity=0, align='center')
        self.face = Group(Circle(201.5, 200-3.5, 1))
        self.visual = Group(
            Rect(200, 200, Player.width, Player.height, fill='dodgerBlue', border='blue', align='center', borderWidth=1),
            self.face,
            self.physicalHitbox,
            self.triggerHitbox,
            )
        self.visual.centerX, self.visual.centerY = pos.x, 400 - pos.y
        
        self.footOffset = Player.height/2 # how far below the center of the player the player's feet are
        self.position = pos
        self.lastPosition = pos
        
        self.maxHealth = 400
        self.health = 400
        self.healthLabel = Label("Health: 400", 395, 5, size=18, fill='white', align='top-right')
        self.immunityTime = 0.45
        self.immunityTimeLeft = 0
        
        self.gravity = -700
        self.velocity = Vec(0, 400)
        self.vertSpeedLim = Vec(-300, 475)
        
        self.flightTime = 3.5
        self.flightTimeLeft = self.flightTime
        self.wingAccel = 950
        self.downWingAccel = 2000
        self.glideVel = -80
        self.jumpVel = 85
        
        self.groundAccel = 722
        self.dragFactor = 3.75 # has an avg max velocity of 192
        self.velKillPoint = 15 # at what point velocity should just be set to 0 on the ground
        self.airAccel = 635
        self.airDragFactor = 2.75 # has an avg max velocity of 231
        
        self.dashCooldown = 1.25 # before using it again
        self.dashCooldownLeft = 0
        self.dashBuffer = 0.3 # time to double-press a direction
        self.dashBufferLeft = self.dashBuffer
        self.dashLength = 0.175 # time where the player is considered to be "dashing" (immunity time)
        self.dashLengthLeft = 0
        self.lastDashInput = 0
        self.dashVel = 300
        
        self.isGrounded = False
        self.isFlying = False
        self.isDashing = False
        self.isGrappled = False
        
        self.platform = None
        
        self.camera = Camera(self)
        self.hook = Hook(self)
        self.weapon = Weapon(self)
        
        
        
    def Damage(self, damage, name, ignoreImmunity=False):
        if (((self.immunityTimeLeft != 0 or self.isDashing) or self.health == -1) and not ignoreImmunity): return
        self.health = max(0, self.health - damage)
        
        if (self.health == 0):
            app.deathScreen.visible = True
            app.deathScreen.children[2].value = f"You were killed by: {name}"
            app.deathScreen.children[2].centerX = 200
            app.deathScreen.toFront()
            Time.timeScale = 0
            app.paused = True
            self.health = -1
            
        self.healthLabel.value = f"Health: {self.health}"
        if (not ignoreImmunity): self.immunityTimeLeft = self.immunityTime
        
        
    def HandleMovement(self):
        # givens
        t = Time.deltaTime
        a = Vec.zero()
        vi = self.velocity
        lim_vy = self.vertSpeedLim
        displacement = Vec.zero()
        
        a.y = self.gravity
        
        if (self.isGrappled): # grappling hook overrides other movement
            if (self.hook.HasEnded(self.position.y, self.lastPosition.y)):
                vi = Vec.zero()
                displacement.y = self.footOffset
                self.hook.EndHook()
            else:
                vi = self.hook.GetPullVelocity()
            
        else:
            # account for flight acceleration 
            if (self.isGrounded and Input.GetKeyDown('space')): # speed boost from "jumping"
                vi.y = self.jumpVel
                self.isGrounded = False
                
            if (not self.isGrounded and Input.GetKey('space')): # flying/gliding
                self.isFlying = self.flightTimeLeft > 0
                if (self.isFlying):
                    if (vi.y < 0):
                        a.y += self.downWingAccel
                    else:
                        a.y += self.wingAccel
                    self.flightTimeLeft -= Time.deltaTime
                    if (self.flightTimeLeft <= 0):
                        self.isFlying = False
                elif (vi.y <= self.glideVel):
                    a.y = 0
                    vi.y = self.glideVel
                    
            # stop vertical movement when grounded
            if (self.isGrounded):
                a.y = 0
                vi.y = 0
                
            # handle horizontal movement inputs
            inputDir = 0
            if (Input.GetKey('a')):
                inputDir -= 1
            if (Input.GetKey('d')):
                inputDir += 1
            accel = self.groundAccel if (self.isGrounded) else self.airAccel
            a.x += accel * inputDir
            # drag = 1 + self.dragFactor*t if (self.isGrounded) else 1 + self.airDragFactor*t
            # vi.x /= drag
            
            if (inputDir != 0):
                self.face.centerX = 200 + 1.5 * inputDir
                
            # if (inputDir == 0 and abs(vi.x) < self.velKillPoint):
            #     vi.x = 0
            
            # dashing "tap" inputs
            tapDir = 0
            if (Input.GetKeyDown('a')):
                tapDir -= 1
            if (Input.GetKeyDown('d')):
                tapDir += 1
            
            # dashing logic
            self.dashCooldownLeft = max(0, self.dashCooldownLeft - Time.deltaTime)
            self.dashBufferLeft = max(0, self.dashBufferLeft - Time.deltaTime)
            self.dashLengthLeft = max(0, self.dashBufferLeft - Time.deltaTime)
            
            if (self.dashBufferLeft == 0):
                self.lastDashInput = 0
            if (self.dashLengthLeft == 0):
                self.isDashing = False
            
            if (tapDir != 0):
                if (tapDir == self.lastDashInput and self.dashCooldownLeft == 0):
                    vi.x = self.dashVel * tapDir
                    self.dashCooldownLeft = self.dashCooldown
                    self.dashLengthTimer = self.dashLength
                    self.isDashing = True
                self.lastDashInput = tapDir
                self.dashBufferLeft = self.dashBuffer
            
        ### kinematics for displacement and new velocity ###
        
        
        # vf = vi + a*t
        vf = vi.add(a.mul(t))
        vf.y = max(lim_vy.min, min(lim_vy.max, vf.y)) # terminal velocity
        drag = 1 + self.dragFactor*t if (self.isGrounded) else 1 + self.airDragFactor*t
        vf.x /= drag
        
        # d = vi*t + .5*a*t**2
        displacement = displacement.add(vf.mul(t))
        
        # if player glitches under the map, tp them back up
        if (self.position.y < app.bottomBorder):
            displacement.y += (app.bottomBorder - self.position.y) + 10
            self.isGrounded = False
        
        
        # update the player's kinematics based on the calculations
        self.velocity = vf
        self.lastPosition = self.position
        self.position = self.position.add(displacement)
        
        # check if the player is colliding with a platform; if so, move their feet to the top of it and tell them they're grounded
        if (not self.isGrounded):
            plat = Platform.GetCollision(self.position.y-self.footOffset, self.lastPosition.y-self.footOffset, -1)
            if (plat is not None):
                self.position.y = plat.posY + self.footOffset
                self.velocity.y = 0
                if (not (self.isFlying and Input.GetKey('space'))): # to avoid the player getting stuck on the ground while trying to fly
                    self.isGrounded = True
                    self.flightTimeLeft = self.flightTime
                    self.platform = plat
        
        # make the player no longer grounded, which causes them to be affected by gravity and fall through the platform they're on
        if (Input.GetKey('s') and self.isGrounded and self.platform.canPass):
            self.isGrounded = False
        
        self.camera.UpdateScreen()
        # app.speed.value = f"({self.velocity.x:.0f}, {self.velocity.y:.0f})"
        
        
    def Update(self):
        self.weapon.Update()
        
        self.HandleMovement()
        
        self.hook.Update()
        
        self.immunityTimeLeft = max(0, self.immunityTimeLeft - Time.deltaTime)
        
        
        
        
class Camera:
    def __init__(self, player):
        self.player = player
        self.deltaPos = Vec()
    
    # DEFINE ALL THE OBJECTS THAT SHOULD BE MOVED INSIDE HERE
    def UpdateScreen(self):
        delta = Vec.VecTo(self.player.position, self.player.lastPosition)
        self.deltaPos = delta
        
        for plat in Platform.platformDict.values():
            plat.visual.centerY -= delta.y
        
        self.player.visual.toFront()
            
            
### todo: at shallow angles, the hook can glitch you under platforms, meaning the player can get under the bottom platform using the hook
class Hook:
    def __init__(self, player):
        self.player = player
        self.hookVelocity = 425
        self.pullVelocity = 340
        self.reelVelocity = 515
        self.distance = None
        self.maxDistance = 225
        
        self.position = None
        self.targetPlatform = None
        self.hookDirection = None
        self.pullDirection = None
        
        self.visual = None
        self.isActive = False
        self.isPulling = False
        self.isReeling = False
        
    def Fire(self):
        self.position = self.player.position.copy()
        self.hookDirection = Vec.AngleTo(Vec(200, 200), Input.mouse)
        self.hookDirection.y *= -1
        
        self.visual = Line(200, 200, 200, 200, fill='dimGray', lineWidth=2)
        
        self.isActive = True
        self.isPulling = False
        self.isReeling = False
    
    def Update(self):
        if (not self.isActive and Input.GetKeyDown('e')):
            self.Fire()
        if (self.isPulling and Input.GetKeyDown('space')):
            self.EndHook()
        
        if (not self.isActive): return
    
        self.distance = Vec.VecTo(self.player.position, self.position)
    
        if (self.isReeling):
            signs = self.distance.getSigns()
            
            dir = self.distance.normalized().mul(-1)
            displacement = dir.mul(self.reelVelocity * Time.deltaTime)
            lastPosition = self.position
            self.position = self.position.add(displacement)
            
            newDistance = Vec.VecTo(self.player.position, self.position)
            newSigns = newDistance.getSigns()
            
            # the hook has gone to the other side of the player on one of the axes, meaning it has passed through the player and it should end
            if (signs.x != newSigns.x or signs.y != newSigns.y):
                self.EndHook()
                return
            
            
        elif (not self.isPulling):
            displacement = self.hookDirection.mul(self.hookVelocity * Time.deltaTime)
            lastPosition = self.position
            self.position = self.position.add(displacement)
            
            plat = Platform.GetCollision(self.position.y, lastPosition.y, 1)
            if (plat is None):
                plat = Platform.GetCollision(self.position.y, lastPosition.y, -1)
                
            dist = self.distance.magnitude()
            
            if (plat is not None): # hook has collided with a platform
                target = Vec()
                angle = math.asin(self.distance.y / dist) if (dist != 0) else 0
                dy = plat.posY - self.player.position.y
                
                if (angle == 0): # no y-component, meaning the player grappled the platform point-blank
                    target = self.player.position.copy()
                else:
                    # find the x-position of the collision using dy and theta; 
                    # we can't just use the x-component of the hook's position for this because it could have gone past the collision point between frames
                    dir = 1 if (self.distance.x > 0) else -1
                    target.x = dir * dy / math.tan(angle) + self.player.position.x
                    target.y = plat.posY

                if (Vec.Dist(self.player.position, target) <= self.maxDistance):
                    self.Grapple(target, plat)
                    
            if (not self.isPulling and dist > self.maxDistance):
                self.ReelHook()
                return
            
        self.UpdateVisual()
        
    def UpdateVisual(self):
        if (not self.isActive): return
        line = self.visual
        line.x2, line.y2 = 200 + self.distance.x, 200 - self.distance.y
        
    def HasEnded(self, posY, lastPosY):
        hookY = self.position.y
        return (lastPosY < hookY and posY >= hookY) or (lastPosY > hookY and posY <= hookY)
        
    def GetPullVelocity(self):
        return self.pullDirection.mul(self.pullVelocity)
        
    def Grapple(self, target, plat):
        self.position = target
        self.targetPlatform = plat
        self.isPulling = True
        self.player.isGrappled = True
        self.player.isGrounded = False
        self.player.flightTimeLeft = self.player.flightTime
        self.pullDirection = self.distance.normalized()
        
    
    def ReelHook(self):
        self.isReeling = True
        
    def EndHook(self):
        self.isActive = False
        self.isPulling = False
        self.player.isGrappled = False
        self.visual.visible = False
        del self.visual
            
    
# last prism
class Weapon:
    def __init__(self, player):
        self.player = player
        self.startAngle = 37.5
        self.lowFreq = 0.25
        self.highFreq = 0.95
        self.lowOpacity = 15
        self.highOpacity = 90
        self.timeToCharge = 3.4 # 3.4, 0.075
        self.timeLeftBuffer = 0.075
        
        self.range = 300
        self.beamCount = 7 # 1-9
        self.offsetRand = 0.6
        self.beamWidth = 3.5
        self.chargedWidth = 10.5
        self.rotateSpeed = 200 # 4 for lerping
        
        self.timeSinceStart = 0
        
        self.damage = 110
        self.damageIncRate = 125 / self.timeToCharge
        self.chargedDamage = 330
        self.randDamageCoeff = 0.5
        self.damageDelay = 0.1
        self.damageDelayLeft = 0
        self.critChance = 35
        self.critMult = 3
        
        self.isFiring = False
        self.isCharged = False
        
        self.colors = [
            rgb(255,0,0), rgb(255,155,0), rgb(255,0,255), 
            rgb(0,255,0), rgb(0,100,200), rgb(0,155,255), 
            rgb(0,0,255), rgb(155,0,255), rgb(255,0,155)
                       ]
        
    
    def Fire(self):
        self.visual = Group()
        self.collider = Arc(200,200, self.range*2, self.range*2, 180-self.startAngle, self.startAngle*2, fill='white', opacity=0)
        self.beams = []
        self.offsets = [i * math.tau/self.beamCount + random.uniform(-self.offsetRand, self.offsetRand) for i in range(self.beamCount)]
        
        topColors = self.colors.copy()
        bottomColors = self.colors.copy()
        for i in range(self.beamCount):
            top = topColors.pop(random.randrange(len(topColors)))
            bottom = bottomColors.pop(random.randrange(len(bottomColors)))
            grad = gradient(top, 'white', bottom, start='top')
            beam = Group(Line(200,200, 200+self.range,200, fill=grad, lineWidth=self.beamWidth, opacity=0), Line(200,200, 200-self.range,200, lineWidth=self.beamWidth, opacity=0))
            self.beams.append(beam)
            self.visual.add(beam)
            
        self.timeSinceStart = 0
        self.rotateAngle = angleTo(200, 200, Input.mouse.x, Input.mouse.y) - 90
        
        self.isFiring = True
        self.isCharged = False
        
        
    def Update(self):
        if (not self.isFiring and (Input.GetMouseDown(0) or Input.GetKeyDown('f'))):
            self.Fire()
            
        if (not self.isFiring): return
    
        if (Input.GetMouseUp(0) or Input.GetKeyUp('f')):
            self.StopFiring()
            return
        
        targetAngle = angleTo(200, 200, Input.mouse.x, Input.mouse.y) - 90
        currentAngle = self.rotateAngle
        delta = (targetAngle - currentAngle + 180) % 360 - 180
        # angleToMove = Lerp(0, delta, self.rotateSpeed * Time.deltaTime)
        dir = -1 if (delta < 0) else 1
        angleToMove = min(abs(delta), self.rotateSpeed * Time.deltaTime)
        angle = (currentAngle + angleToMove * dir) % 360
        self.rotateAngle = angle
        
    
        ## PRISM IS CHARGING
        if (not self.isCharged):
            a = self.startAngle
            l = self.timeToCharge
            t = min(l, self.timeSinceStart)
            f = self.lowFreq + (self.highFreq - self.lowFreq)/l * t
            
            amplitude = a - a/l * t
            theta = f * math.tau * t
            
            for i in range(self.beamCount):
                beam = self.beams[i]
                offset = self.offsets[i]
                beam.children[0].opacity = self.lowOpacity + (self.highOpacity - self.lowOpacity)/l * t
                lastAngle = beam.rotateAngle
                beam.rotateAngle = amplitude * math.sin(theta + offset) + self.rotateAngle
            
            # added constants to make it go a little more outwards, since the beams were passing the edge before
            self.collider.startAngle = 180-amplitude - 1.5
            self.collider.sweepAngle = amplitude * 2 + 2.5
            self.collider.rotateAngle = self.rotateAngle - 90
            
            if (t >= self.timeToCharge - self.timeLeftBuffer):
                self.FireCharged()
            
            self.timeSinceStart += Time.deltaTime
            
        ## PRISM IS CHARGED
        else:
            colors = self.colors.copy()
            top = colors.pop(random.randrange(len(colors)))
            bottom = colors.pop(random.randrange(len(colors)))
            grad = gradient(*2*(top,), *5*('white',), *2*(bottom,), start='top')
            
            rotateAngle = self.rotateAngle + random.uniform(-.33, .33)
            
            self.visual.fill = grad
            self.visual.rotateAngle = rotateAngle
             
            theta = rotateAngle * math.pi/180
            
            self.collider.x2 = 200 + self.range*math.cos(theta)
            self.collider.y2 = 200 + self.range*math.sin(theta)
            
            
        ## PRISM IS IN ANY ACTIVE STATE
        if (self.damageDelayLeft == 0):
            damage = 0
            if (not self.isCharged):
                damage = self.damage + self.damageIncRate * t
                damage += random.randint(int(-self.damage*self.randDamageCoeff), int(self.damage*self.randDamageCoeff))
            else:
                damage = self.chargedDamage
                damage += random.randint(-self.chargedDamage*self.randDamageCoeff, self.chargedDamage*self.randDamageCoeff)
            if (random.randint(1, 100) <= self.critChance): damage *= self.critMult
            for enemy in Game.enemies.copy():
                if (enemy.hitbox.hitsShape(self.collider)):
                    enemy.Damage(damage)
                    self.damageDelayLeft = self.damageDelay
        self.damageDelayLeft = max(0, self.damageDelayLeft - Time.deltaTime)
        
            
            
    def FireCharged(self):
        self.isCharged = True
        self.visual.visible = False
        self.collider.visible = False
        self.collider = Line(200,200, 200+self.range,200, opacity=0, lineWidth=self.chargedWidth)
        self.beams.clear()
    
        opacity = 95
        self.visual = Group(Line(200,200, 200+self.range, 200, lineWidth=self.chargedWidth, opacity=opacity), Line(200,200, 200-self.range, 200, lineWidth=self.chargedWidth, opacity=0))
        self.visual.rotateAngle = self.rotateAngle
            
    def StopFiring(self):
        self.isFiring = False
        self.visual.visible = False
        self.collider.visible = False
        self.beams.clear()





# PROJECTILE
class LaserProjectile:
    activeLasers = set()
    
    length, width = (45, 3)
    startOpacity = 90
    velocity = 775
    maxDistance = 300
    
    damage = Vec(32, 40)
    
    @classmethod
    def Update(this):
        t = Time.deltaTime
        for laser in this.activeLasers.copy():
            vecToPlayer = Vec.VecTo(laser.position, app.player.position)
            if (vecToPlayer.magnitude() > this.maxDistance):
                laser.Destroy()
                continue
            
            displacement = laser.angleVec.mul(this.velocity * t)
            
            lastPosition = laser.position.copy()
            laser.position = laser.position.add(displacement)
            
            laser.group.centerX += displacement.x + app.player.camera.deltaPos.x
            laser.group.centerY -= displacement.y + app.player.camera.deltaPos.y
            
            lastDirFromPlayer = Vec.VecTo(app.player.position, lastPosition)
            dirFromPlayer = Vec.VecTo(app.player.position, laser.position)
            hitbox = Line(200+lastDirFromPlayer.x, 200-lastDirFromPlayer.y, 200+dirFromPlayer.x+laser.angleVec.x*this.length, 200-dirFromPlayer.y-laser.angleVec.y*this.length, fill='white', lineWidth=this.width)
            if (hitbox.hitsShape(app.player.triggerHitbox)):
                app.player.Damage(this.damage.randint(), "Laser Beam")
            hitbox.visible = False


    def __init__(self, pos, angleVec):
        this = LaserProjectile
        dirFromPlayer = Vec.VecTo(app.player.position, pos)
        canvasPos = Vec(200 + dirFromPlayer.x, 200 - dirFromPlayer.y)
        edgePos = canvasPos.add(Vec(angleVec.x, -angleVec.y).mul(this.length))
        
        this.activeLasers.add(self)
        
        self.position = pos.copy()
        self.angleVec = angleVec
        
        self.visual = Line(canvasPos.x, canvasPos.y, edgePos.x, edgePos.y, fill='red', opacity=this.startOpacity, lineWidth=this.width)
        self.group = Group( self.visual )
        self.group.toBack()
        
        
    def Destroy(self):
        self.group.visible = False
        LaserProjectile.activeLasers.remove(self)



class Retinazer:
    class State:
        class ABOVE:
            maxTime = 11
            timeLeft = 7
            cooldown = 1.25
            cooldownLeft = 2
            accel = 2000
            maxVel = 280
            offset = Vec(0, 140)
        class SIDE:
            maxTime = 5
            timeLeft = maxTime
            cooldown = 0.6
            cooldownLeft = 0
            accel = 1350
            maxVel = 280
            offset = Vec(120, 0)
        class LASER:
            # https://www.desmos.com/calculator/hl2nmuwywb
            getRadius = lambda x, te, ts, re, rs:  re*math.sin(math.pi/te/2*x) if (0 <= x <= te)   else   0.5*(re-rs)*math.cos(math.pi/ts*(x-te))+rs+0.5*(re-rs) if (te < x <= te+ts)   else   rs
            radiusTimeRange = Vec(0.5, 1.75)
            radiusRange = Vec(600, 320)
            getAngle = lambda x, a, tc, tf:  a/tc*x**2 if (0 < x and x<= tc)   else   2*a*x-a*tc if (tc < x and x <= tc+tf)   else   0
            angleTimeRange = Vec(3, 7.5)
            angleAmp = 60
            timeSinceStart = 0
            timeToLaserCircleEnd = radiusTimeRange.x + radiusTimeRange.y
            timeToLaserDespawn = timeToLaserCircleEnd/2 + angleTimeRange.x + angleTimeRange.y
            laserSpawnDelay = 0.25
            laserSpawnRate = 30
            laserSmallOpacity = 55
            laserOpacity = 85
            direction = None
            startAngle = None
            zapDamage = 2
            zapBuffer = 0.75
            zapCooldown = 0.1
            zapCooldownLeft = 0
        
        
        
    radius = 25
    laserThickness = 15
    laserRange = 800
    
    def __init__(self, pos):
        this = Retinazer
        self.hitbox = Circle(200,200, this.radius, fill=rgb(165, 110, 110), border='black')
        self.laserCircle = Circle(200, 200, 1, fill=None, border='red', borderWidth=5)
        self.laser = Line(200, 200, 200, 200-this.laserRange, fill=gradient(*3*('crimson',), *3*(rgb(255, 240, 240),), *3*('crimson',), start='left'), lineWidth=this.laserThickness, opacity=75)
        self.laserHint = Line(200, 200, 200, 200-this.laserRange, fill='red', lineWidth=this.laserThickness/3, dashes=(12, 9))
        counterLaser = Line(200, 200, 200, 200+this.laserRange, lineWidth=this.laserThickness, opacity=0)
        self.group = Group( self.laserHint, self.laser, counterLaser, self.hitbox, self.laserCircle )
        self.laserCircle.opacity = 0
        self.laser.opacity = 0
        self.laserHint.opacity = 0
        counterLaser.opacity = 0
        
        Game.enemies.add(self)
        
        self.position = pos
        self.target = None
        self.group.centerX, self.group.centerY = pos.tuple()
        
        self.health = 150000
        self.contactDamage = Vec(15, 22)
        self.state = this.State.ABOVE
        
        self.laserDamage = Vec(65, 78)
        
        self.velocity = Vec.zero()
        
        
    def Update(self):
        State = Retinazer.State
        s = self.state
        t = Time.deltaTime
        a = Vec.zero()
        vi = self.velocity
        vf = Vec.zero()
        displacement = Vec.zero()
        
        if (s is State.ABOVE or s is State.SIDE):
            s.cooldownLeft = max(0, s.cooldownLeft - Time.deltaTime)
            if (s.cooldownLeft == 0):
                angleToPlayer = Vec.AngleTo(self.position, app.player.position)
                LaserProjectile(self.position.add(angleToPlayer.mul(Retinazer.radius * 0.75)), angleToPlayer)
                s.cooldownLeft = s.cooldown
            
            self.target = app.player.position.add(Vec(s.offset.x, s.offset.y)) if (self.position.x > app.player.position.x) else app.player.position.add(Vec(-s.offset.x, s.offset.y))
            
            vecToTarget = Vec.VecTo(self.position, self.target)
            dirToMove = vecToTarget.normalized()
            distance = vecToTarget.magnitude()
            
            a = a.add(dirToMove.mul(s.accel))
            
            if (vi.magnitude()-1 > s.maxVel):
                vi = vi.normalized().mul(s.maxVel)
                a = Vec.zero()
                
            damping = math.exp(-distance / 150)
                
            vf = vi.add(a.mul(t)).sub(vi.mul(damping / 25))
            
            s.timeLeft = max(0, s.timeLeft - Time.deltaTime)
            if (s.timeLeft == 0):
                s.timeLeft = s.maxTime
                s.cooldownLeft = s.cooldown
                self.state = State.SIDE if (s is State.ABOVE) else State.LASER
                if (self.state is State.LASER):
                    self.laserCircle.opacity = 90
                    self.laserHint.opacity = 60
                    self.state.direction = randDir()
                    # self.state.startAngle = random.randint(0, 359)
                
        elif (s is State.LASER):
            s.timeSinceStart += Time.deltaTime
            dt = s.timeSinceStart
            
            if (dt < s.timeToLaserCircleEnd):
                radius = s.getRadius(dt, s.radiusTimeRange.x, s.radiusTimeRange.y, s.radiusRange.x, s.radiusRange.y) + 0.01
                self.laserCircle.radius = radius
            else:
                s.zapCooldownLeft = max(0, s.zapCooldownLeft - Time.deltaTime)
                distance = Vec.Dist(self.position, app.player.position)
                if (distance > self.laserCircle.radius):
                    if (s.zapCooldownLeft == 0):
                        app.player.Damage(s.zapDamage, 'Loneliness (too far away)', True)
                        s.zapCooldownLeft = s.zapCooldown
                else:
                    s.zapCooldownLeft = s.zapBuffer
            
            
            if (dt >= s.timeToLaserCircleEnd/2):
                lastAngle = self.group.rotateAngle
                angle = s.direction * s.getAngle(dt - s.timeToLaserCircleEnd/2, s.angleAmp, s.angleTimeRange.x, s.angleTimeRange.y)
                self.group.rotateAngle = angle #+ s.startAngle
                
                if (self.laser.opacity != s.laserOpacity and dt >= s.timeToLaserCircleEnd/2 + s.laserSpawnDelay):
                    self.laser.opacity = min(s.laserSmallOpacity, self.laser.opacity + s.laserSpawnRate * Time.deltaTime)
                    if (self.laser.opacity == s.laserSmallOpacity):
                        self.laser.opacity = s.laserOpacity
                        self.laserHint.opacity = 0

                if (dt > s.timeToLaserDespawn):
                    self.laserCircle.opacity = 0
                    self.laserCircle.radius = 0.1
                    self.laser.opacity = 0
                    self.state = State.ABOVE
                    s.timeSinceStart = 0

                if (self.laser.opacity == s.laserOpacity):
                    hitboxes = [self.laser]
                    arcHitbox = None
                    sweepAngle = min(360, max(-360, math.floor(angle - lastAngle)))
                    if (sweepAngle != 0):
                        arcHitbox = Arc(self.group.centerX, self.group.centerY, Retinazer.laserRange, Retinazer.laserRange, lastAngle, abs(sweepAngle), fill='white', opacity=25)
                        if (sweepAngle < 0):
                            arcHitbox.rotateAngle = sweepAngle
                        hitboxes.append(arcHitbox)
                    for hitbox in hitboxes:
                        if (hitbox.hitsShape(app.player.triggerHitbox)):
                            app.player.Damage(self.laserDamage.randint(), 'Death Ray')
                    if (arcHitbox): arcHitbox.visible = False
                    

            
        displacement = displacement.add(vf.mul(t))
        
        self.velocity = vf
        self.position = self.position.add(displacement)
        
        self.group.centerX += displacement.x + app.player.camera.deltaPos.x
        self.group.centerY -= displacement.y + app.player.camera.deltaPos.y
        
        
    def Damage(self, damage):
        self.health = max(0, self.health - damage)
        app.boss.UpdateBar()
        if (self.health == 0):
            self.hitbox.fill = rgb(125,125,125)
        
        
        
# PROJECTILE
class Breath:
    activeBreaths = set()
    
    length, width = (90, 15)
    startOpacity = 75
    minOpacity = 15
    lifespan = 0.35
    opacityRate = startOpacity/lifespan
    
    damage = Vec(21, 27)
    
    @classmethod
    def Update(this):
        for breath in this.activeBreaths.copy():
            opacity = breath.visual.opacity
            opacity -= this.opacityRate * Time.deltaTime
            
            if (opacity <= 0):
                breath.group.visible = False
                this.activeBreaths.remove(breath)
                del breath
                continue
            
            breath.visual.opacity = opacity
            breath.group.centerX += app.player.camera.deltaPos.x
            breath.group.centerY -= app.player.camera.deltaPos.y
            
            if (opacity >= this.minOpacity  and  breath.visual.hitsShape(app.player.triggerHitbox)):
                app.player.Damage(this.damage.randint(), 'Fire Breath')
            
    def __init__(self, pos, angleVec):
        dirFromPlayer = Vec.VecTo(app.player.position, pos)
        canvasPos = Vec(200 + dirFromPlayer.x, 200 - dirFromPlayer.y)
        angleVec.y = -angleVec.y
        edgePos = canvasPos.add(angleVec.mul(Breath.length))
        
        Breath.activeBreaths.add(self)
        
        self.visual = Line(canvasPos.x, canvasPos.y, edgePos.x, edgePos.y, fill='lime', opacity=Breath.startOpacity, lineWidth=Breath.width)
        self.group = Group( self.visual )
        self.group.toBack()
        
        

class Spazmatism:
    class State:
        class BREATHING:
            maxTime = 8
            timeLeft = maxTime
            cooldown = 0.15
            cooldownLeft = 0
            accel = 1250
            maxVel = 160
            sideOffset = 65
            
        class DASHING:
            maxDashes = 7
            dashesLeft = maxDashes
            dashDuration = 0.35
            dashDurationLeft = dashDuration
            dashBuffer = 0.15
            dashBufferLeft = dashBuffer
            dashVel = 500
            dashDecel = -1250
            dashDir = None
            isDashing = False
        
    radius = 25
        
    def __init__(self, pos):
        this = Spazmatism
        self.hitbox = Circle(200,200, this.radius, fill=rgb(110, 165, 110), border='black')
        self.group = Group( self.hitbox )
        
        Game.enemies.add(self)
        
        
        self.position = pos
        self.target = None
        self.hitbox.centerX, self.hitbox.centerY = pos.tuple()
        
        self.health = 120000
        self.contactDamage = Vec(35, 45)
        self.state = this.State.BREATHING
        
        
        self.velocity = Vec.zero()

        
    def Update(self):
        State = Spazmatism.State
        s = self.state
        t = Time.deltaTime
        a = Vec.zero()
        vi = self.velocity
        vf = Vec.zero()
        displacement = Vec.zero()
        
        if (s is State.BREATHING):
            s.cooldownLeft = max(0, s.cooldownLeft - Time.deltaTime)
            if (s.cooldownLeft == 0):
                angleToPlayer = Vec.AngleTo(self.position, app.player.position)
                Breath(self.position.add(angleToPlayer.mul(Spazmatism.radius * 0.75)), angleToPlayer)
                s.cooldownLeft = s.cooldown
            
            self.target = app.player.position.add(Vec(s.sideOffset, 0)) if (self.position.x > app.player.position.x) else app.player.position.add(Vec(-s.sideOffset, 0))
            
            vecToTarget = Vec.VecTo(self.position, self.target)
            dirToMove = vecToTarget.normalized()
            distance = vecToTarget.magnitude()
            
            a = a.add(dirToMove.mul(s.accel))
            
            if (vi.magnitude()-1 > s.maxVel):
                vi = vi.normalized().mul(s.maxVel)
                a = Vec.zero()
                
            damping = math.exp(-distance / 20)
                
            vf = vi.add(a.mul(t)).sub(vi.mul(damping / 35))
            
            s.timeLeft = max(0, s.timeLeft - Time.deltaTime)
            if (s.timeLeft == 0):
                self.state = State.DASHING
                s.timeLeft = s.maxTime
                
        elif (s is State.DASHING):
            if (not s.isDashing):
                s.dashBufferLeft = max(0, s.dashBufferLeft - Time.deltaTime)
                if (s.dashBufferLeft == 0):
                    self.target = app.player.position
                    s.dashDir = Vec.AngleTo(self.position, self.target)
                    vf = s.dashDir.mul(s.dashVel)
                    
                    s.isDashing = True
                    s.dashesLeft -= 1
                    s.dashBufferLeft = s.dashBuffer
                    
            elif (s.isDashing):
                vf = vi
                s.dashDurationLeft = max(0, s.dashDurationLeft - Time.deltaTime)
                if (s.dashDurationLeft == 0):
                    a = s.dashDir.mul(s.dashDecel)
                    vf = vi.add(a.mul(t))
                
                    if (vi.getSigns() != vf.getSigns()): # boss has decelerated and is now going other direction, so it should stop
                        if (s.dashesLeft == 0):
                            self.state = State.BREATHING
                            s.dashesLeft = s.maxDashes
                            
                        vf = Vec.zero()
                        s.isDashing = False
                        s.dashDurationLeft = s.dashDuration
                    
                
                
        
        displacement = displacement.add(vf.mul(t))
        
        self.velocity = vf
        self.position = self.position.add(displacement)
        
        self.group.centerX += displacement.x + app.player.camera.deltaPos.x
        self.group.centerY -= displacement.y + app.player.camera.deltaPos.y
            
            
            
        
    def Damage(self, damage):
        self.health = max(0, self.health - damage)
        app.boss.UpdateBar()
        if (self.health == 0):
            self.hitbox.fill = rgb(125,125,125)
            
            


class Twins:
    def __init__(self, pos):
        self.spazmatism = Spazmatism(pos)
        self.retinazer = Retinazer(pos)
        
        self.health = self.spazmatism.health + self.retinazer.health
        self.bossbar = Bossbar(self.health)
        
        
    def UpdateBar(self):
        self.health = self.spazmatism.health + self.retinazer.health
        self.bossbar.UpdateHealth(self.health)
        if (self.health == 0):
            Rect(0,0,400,400,opacity=75)
            Label("nice you won", 200, 200, fill='white', size=64)
            app.player.visual.toBack()
            app.stop()
        
        
        
    def Update(self):
        self.retinazer.Update()
        self.spazmatism.Update()
        
        Breath.Update()
        LaserProjectile.Update()
        
        for boss in [self.retinazer, self.spazmatism]:
            if (boss.hitbox.hitsShape(app.player.triggerHitbox)):
                name = 'Retinazer' if (boss is self.retinazer) else 'Spazmatism'
                app.player.Damage(boss.contactDamage.randint(), name)
        
        self.bossbar.Update()
        
        
        
        
class Bossbar:
    def __init__(self, maxHealth):
        self.barBounds = Vec(75, 325)
        
        self.border = Rect(self.barBounds.min-3, 380, self.barBounds.max-self.barBounds.min+6, 18, fill='gray', border='dimGray', borderWidth=3, align='left')
        self.bar = Line(self.barBounds.min, 380, self.barBounds.max, 380, fill='crimson', lineWidth=12)
        self.lagBar = Line(self.bar.x1, self.bar.y1, self.bar.x2, self.bar.y2, fill='yellow', lineWidth=self.bar.lineWidth)
        self.group = Group(self.border, self.lagBar, self.bar)
        
        self.maxHealth = maxHealth
        self.health = maxHealth
        
        self.lagBar.speed = 5
        self.lagBar.maxSpeed = 20
        self.lagBar.buffer = 0.25
        self.lagBar.bufferLeft = self.lagBar.buffer
        self.lagBar.maxBuffer = 3
        self.lagBar.maxBufferLeft = self.lagBar.maxBuffer
        self.lagBar.closeDistance = 0.2
        self.lagBar.isMoving = False
        self.lagBar.movementTime = 0
        self.lagBar.maxMovementTime = 2
        
    def Update(self):
        point = self.health / self.maxHealth
        
        self.bar.x2 = Lerp(self.barBounds.min, self.barBounds.max, point)
        
        lag = self.lagBar
        if (lag.bufferLeft == 0 or lag.maxBufferLeft == 0):
            lag.isMoving = True
            speed = lag.speed if (lag.maxBufferLeft != 0) else lag.maxSpeed
            lag.x2 = Lerp(lag.x2, self.bar.x2, speed * Time.deltaTime)
            lag.movementTime += Time.deltaTime
            if (lag.x2 - lag.closeDistance <= self.bar.x2):
                lag.x2 = self.bar.x2
                lag.maxBufferLeft = lag.maxBuffer
                lag.isMoving = False
        if (lag.x2 != self.bar.x2 and lag.bufferLeft != 0):
            lag.maxBufferLeft = max(0, lag.maxBufferLeft - Time.deltaTime)
        lag.bufferLeft = max(0, lag.bufferLeft - Time.deltaTime)
        
        self.group.toFront()
        
    def UpdateHealth(self, health):
        self.health = health
        
        if (not self.lagBar.isMoving or self.lagBar.movementTime > self.lagBar.maxMovementTime):
            self.lagBar.isMoving = False
            self.lagBar.movementTime = 0
            if (self.lagBar.bufferLeft == 0):
                self.lagBar.maxBufferLeft = self.lagBar.maxBuffer
            self.lagBar.bufferLeft = self.lagBar.buffer
    



class Platform:
    platformDict = {}
    keyRange = Vec(9999, -9999)
    SPACING = 190
    
    def __init__(self, key, canPass):
        Platform.platformDict[key] = self
        Platform.keyRange.min = min(Platform.keyRange.min, key)
        Platform.keyRange.max = max(Platform.keyRange.max, key)
        self.posY = key * Platform.SPACING
        self.visual = Rect(-5, 400-self.posY, 410, 2.5, fill=gradient('burlyWood', 'sienna', start='top'), border='black', borderWidth=0.25)
        self.canPass = canPass
    
    @staticmethod # passDirection is the direction that the object is moving towards the platform for (-1 means falling through it, 1 means coming up from under)
    def GetCollision(posY, lastPosY, passDirection):
        if (passDirection != 1 and passDirection != -1):
            raise Exception(f"passDirection ({passDirection}) is not 1 or -1")
        
        key = math.floor(posY/Platform.SPACING)
        if (passDirection == -1): key += 1
        if (key < Platform.keyRange.min or key > Platform.keyRange.max): return None
        plat = Platform.platformDict[key]
        
        if (passDirection == -1):
            if (lastPosY > plat.posY and posY <= plat.posY):
                return plat
        elif (passDirection == 1):
            if (lastPosY < plat.posY and posY >= plat.posY):
                return plat
            




class Game:
    enemies = set()
    projectiles = set()
    


# app.background = gradient('lightSkyBlue', 'cornflowerBlue', start='top')
app.background = gradient('black', rgb(25, 0, 0), rgb(80, 0, 0), start='top')
        
app.player = None
app.boss = None

for i in range(-2, 7):
    canPass = i != -2
    plat = Platform(i, canPass)
    if (not canPass):
        app.bottomBorder = plat.posY
        
app.player = Player(Vec(200, 200))
app.boss = Twins(Vec(-25, 200))



# lol = Group()
# for i in range(10):
#     for j in range(6):
#         lol.add(Circle(i*200, 650 - j*200, 15, fill='white'))


def onStep():
    Time.Update()
    
    # death screen stuff
    # if (not app.paused): Time.timeScale = 1
    if (app.deathScreen.visible):
        app.deathScreen.visible = False
    

    if (Time.deltaTime == 0): return

    if (app.boss): app.boss.Update()
    if (app.player): app.player.Update()
    
    Input.Update()
    
    
    
    
def onKeyPress(key):
    Input.kDown.add(key.lower())
    
def onKeyRelease(key):
    Input.kUp.add(key.lower())
    
def onKeyHold(keys):
    Input.kHeld.update(key.lower() for key in keys)
        
def onMouseMove(x, y):
    Input.lastMouse = Vec(Input.mouse.x, Input.mouse.y)
    Input.mouse = Vec(x, y)
        
def onMouseDrag(x, y):
    Input.lastMouse = Vec(Input.mouse.x, Input.mouse.y)
    Input.mouse = Vec(x, y)
    
def onMousePress(x, y, button):
    Input.mDown[button] = True
    Input.mHeld[button] = True
    
def onMouseRelease(x, y, button):
    Input.mUp[button] = True
    Input.mHeld[button] = False



kwargs = {'fill':'white', 'size':13, 'align':'left'}
Label("ASD to move", 8, 10, **kwargs)
Label("x2 A/D to dash", 8, 25, **kwargs)
Label("SPACE to jump/fly or cancel grapple", 8, 40, **kwargs)
Label("E to grapple", 8, 55, **kwargs)
Label("LMB/F to shoot", 8, 70, **kwargs)
            
            
            
            
            
            