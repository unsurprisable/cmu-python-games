# September 2023

import math
import time
import random
from enum import Enum



#####
##### !!!
#####

### VARIABLES THAT HELP TO INCREASE 
### FPS ARE LABELED WITH A ***

#####
##### !!!
#####








##### CLASSES #####

### Vector2
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self._magnitude = 0.0
        self._x = x
        self.y = y
    

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

    def __sub__(self, other):
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
        
    @property
    def normalized(self):
        self.UpdateMagnitude()
        if (self._magnitude != 0):
            return Vector2(self.x / self._magnitude, self.y / self._magnitude)
        else:
            return Vector2(0, 0)
            
    @property
    def zero(self):
        return Vector2(0.0, 0.0)
    @property
    def one(self):
        return Vector2(1.0, 1.0)
        
        
    @property
    def randomDir(self):
        x = random.randrange(-100, 100)
        y = random.randrange(-100, 100)
        newVector = Vector2(x, y).normalized
        return newVector
        
        
    @staticmethod
    def angleTo(x1, y1, x2, y2):
        return Vector2(x2-x1, y2-y1).normalized


### Input
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
     
        
### Time
class Time:
    lastFrame = time.time()
    deltaTime = 0.0
    
    @staticmethod
    def Update():
        Time.deltaTime = time.time() - Time.lastFrame
        Time.lastFrame = time.time()
        
        
        
### AUDIO
class Audio:
    PLAYER_SHOOT = Sound('cmu://682887/23686433/ricochet_shot.ogg')
    PLAYER_BLANK = Sound('cmu://682887/23689566/bomb_explode.ogg')
    PLAYER_BLANK_HIT = [
        Sound('cmu://682887/23689603/fire_bullet_impact.ogg'),
        Sound('cmu://682887/23689603/fire_bullet_impact.ogg'),
        Sound('cmu://682887/23689603/fire_bullet_impact.ogg'),
        Sound('cmu://682887/23689603/fire_bullet_impact.ogg'),
        ]
    playerBlankHitCounter = 0
    
    BOSS_DAMAGE = Sound('cmu://682887/23686435/twig_break1.ogg')
    BOSS_DASH = Sound('cmu://682887/23689164/shield_launch.ogg')
    BOSS_CROSS_INITIATE = Sound('cmu://682887/23686686/bubble_pop1.ogg')
    BOSS_CROSS_FIRE = Sound('cmu://682887/23686687/shield_create.ogg')
        
##### CLASSES #####



##### HELPER FUNCTIONS #####
    
def Lerp(start, end, t):
    if (t == 0): return start
    elif (t < 0): t *= -1
    range = end - start
    increment = range * t
    value = start + increment
    return value
    
def RemoveTutorialIndex(index):
    app.tutorial[index].visible = False
    
def PlayerDeath():
    Rect(0,0,400,400,opacity=60)
    Label("YOU DIED!", 200, 200, size=50, fill='white')
    app.stop()
    
def PlayerWin():
    Rect(0,0,400,400,opacity=75)
    Label("YOU WON!", 200, 200, size=50, fill='white')
    app.paused = True

##### HELPER FUNCTIONS #####









##### PLAYER #####

class Player:
    
    ### START
    def __init__(self):
        self.visual = Circle(200, 200, 6, border='black', borderWidth=1)
        
        self.hitCollider = Circle(200, 200, 5, opacity=0)
        self.hitCollider.parent = self
        
        self.position = Vector2(200, 300)
        
        self.velocity = Vector2()
        
        self.color = rgb(20, 175, 175)
        self.visual.fill = self.color
        
        self.UpdateVisual()
        
        
        
        
        self.speed = 22
        
        self.friction = 0.875
        
        self.isDashing = False
        self.dashImpulseSpeed = 22
        self.dashSpeed = 1.625
        self.dashDuration = .5
        self.dashCooldown = 1
        self.dashDurationTimer = 0
        self.dashCooldownTimer = 0
        self.dashColor = rgb(47, 101, 94)
        
        self.trail = Group()
        self.trailLength = 75
        self.trailDensity = 50 # 0-100   ! *** !
        self.trailOpacity = 25
        self.trailSize = 6.75
        self.trailColor = rgb(200, 238, 255)
        self.trailRoundness = 10
        self.trail.enabled = True #      ! *** !
        self.trailTimer = 0
        
        self.lookDirection = Vector2()
        
        self.bulletSpeed = 1250
        self.shootCooldown = .1
        self.shootCooldownTimer = self.shootCooldown
        self.bulletDamage = 2
        self.recoil = .0#275
        self.shootSpeedReduction = 0.5
        self.isShooting = False
        
        self.blanksLeft = 2
        self.blank = None
        self.blankExpandRate = 500
        self.blankLifetime = .6
        self.blankOpacityRate = 150
        self.blankTimer = self.blankLifetime
        
        self.livesLeft = 3
        self.immunityLength = 2
        self.immunityTimer = self.immunityLength
        self.isImmune = False
        self.damageVignette = Rect(0, 0, 400, 400, fill=gradient('gray', 'crimson'), opacity=0)
        self.damageVignetteOpacityRate = 25
        
        self.timeSinceLastHit = 0
        
        self.playTime = 0
        self.bulletsHit = 0
        self.bulletsShot = 0
        self.bulletsAvoided = 0




    ### UPDATE
    def Update(self):
        
        self.UpdateVisual()
        
        self.playTime += Time.deltaTime
        
        # Shooting
        self.shootCooldownTimer -= Time.deltaTime
        
        if (Input.GetMouse(0)):
            self.isShooting = True
            if (self.shootCooldownTimer <= 0):
                self.bulletsShot += 1
                
                self.shootCooldownTimer = self.shootCooldown
                self.lookDirection = self.GetLookDirection()
                bullet = PlayerBullet.Spawn(Vector2(self.position.x, self.position.y), (self.lookDirection * self.bulletSpeed), self.bulletDamage)
                Audio.PLAYER_SHOOT.play(restart=True)
                
                self.velocity.x -= self.lookDirection.x * self.recoil
                self.velocity.y += self.lookDirection.y * self.recoil
        else:
            self.isShooting = False
            
        
        # Movement
        inputDir = Vector2(0, 0)
        
        if (Input.GetKey('w')):
            inputDir.y += 1
        if (Input.GetKey('a')):
            inputDir.x -= 1
        if (Input.GetKey('s')):
            inputDir.y -= 1
        if (Input.GetKey('d')):
            inputDir.x += 1
            
        moveDir = self.speed * inputDir.normalized
        
        if (self.isDashing):
            moveDir *= self.dashSpeed
        if (self.isShooting):
            moveDir *= self.shootSpeedReduction
            
        self.velocity += moveDir
        
        velocity = Vector2()
        velocity.x = self.velocity.x * Time.deltaTime
        velocity.y = self.velocity.y * Time.deltaTime
        
        if (self.position.x + velocity.x <= 400-self.hitCollider.radius and self.position.x + velocity.x >= 0+self.hitCollider.radius):
            self.position.x += velocity.x
        if (self.position.y - velocity.y <= 400-self.hitCollider.radius and self.position.y - velocity.y >= 0+self.hitCollider.radius):
            self.position.y -= velocity.y
        
        self.velocity *= self.friction
        
        if ((self.velocity.magnitude > 0 and self.velocity.magnitude - 0.001 < 0) or (self.velocity.magnitude < 0 and self.velocity.magnitude + 0.001 > 0)):
            self.velocity = Vector2()
            
            
            
        # Dash
        if (Input.GetKeyDown('space') and self.ReadyToDash()):
            self.velocity = moveDir * self.dashImpulseSpeed
            self.Dash()
    
        if (self.isDashing):
            self.dashDurationTimer -= Time.deltaTime
        else:
            self.dashCooldownTimer -= Time.deltaTime
            
        if (self.isDashing and self.dashDurationTimer <= 0):
            self.EndDash()
            
            
            
        # Trail
        if (self.trail.enabled):
            timerMax = .1 - (self.trailDensity/1000)
            self.trailTimer += Time.deltaTime
            if (self.IsMoving() and self.trailTimer >= timerMax):
                self.trailTimer = 0
                particle = Circle(self.position.x, self.position.y, self.trailSize, opacity=self.trailOpacity, fill=self.trailColor)
                self.trail.add(particle)
                
            self.UpdateTrail()
            
            
        
        # Blanks
        if (Input.GetMouseDown(1) and self.blanksLeft > 0 and self.blank == None):
            self.SpawnBlank()
            
        if (self.blank != None):
            self.blankTimer -= Time.deltaTime
                
            opacity = self.blank.opacity - (self.blankOpacityRate * Time.deltaTime)
            if (opacity < 0):
                opacity = 0
                
            self.blank.radius += self.blankExpandRate * Time.deltaTime
            self.blank.opacity = opacity
            self.blank.toBack()
            
            if (self.blankTimer <= 0):
                self.blank.visible = False
                self.blank = None
                
                self.blankTimer = self.blankLifetime
        
        self.UpdateVisual() # i know there are two of these... dunno if its placebo or not but it feels more responsive when there are two
        
        
        
        
        # Lives
        if (self.isImmune):
            self.immunityTimer -= Time.deltaTime
            
        if (self.immunityTimer <= 0):
            self.isImmune = False
            self.immunityTimer = self.immunityLength
            
        if (self.damageVignette.opacity > 0):
            opacity = self.damageVignette.opacity
            
            opacity -= self.damageVignetteOpacityRate * Time.deltaTime
            if (opacity < 0):
                opacity = 0
                
            self.damageVignette.opacity = opacity
            
            
            
            
        # Ability?
        self.timeSinceLastHit += Time.deltaTime
    
    
    
        
    ### COLLISION
    
    def OnCollision(self, other):
        if (self.hitCollider.hitsShape(other)):
            if (isinstance(other.parent, BossBullet) or isinstance(other.parent, BossHomingBullet) or isinstance(other.parent, Boss)):
                if (not self.isDashing and not self.isImmune):
                    self.PlayerDamage()
            return True
            
        return False
        
        

            
        
        
        
    
    ### OTHER
    
    def UpdateVisual(self):
        self.visual.centerX = self.position.x
        self.visual.centerY = self.position.y
        self.hitCollider.centerX = self.position.x
        self.hitCollider.centerY = self.position.y
        
    def SpawnBlank(self):
        self.blanksLeft -= 1
        self.blank = Circle(self.position.x, self.position.y, 5, fill=gradient(app.background, app.background, app.background, app.background, 'cyan'))
        self.blank.toBack
        
        Audio.PLAYER_BLANK.play(restart=True)
    
    def ReadyToDash(self):
        return (not self.isDashing and self.dashCooldownTimer <= 0)
    
    def Dash(self):
        self.dashDurationTimer = self.dashDuration
        self.isDashing = True
        
        self.visual.fill = self.dashColor
        
    def EndDash(self):
        self.isDashing = False
        self.dashCooldownTimer = self.dashCooldown
        
        self.visual.fill = self.color
        
    def IsMoving(self):
        return (self.velocity != Vector2(0.0,0.0))
        
    def UpdateTrail(self):
        self.trail.toBack()
        for particle in self.trail:
            reduction = self.trailLength * Time.deltaTime
            opacity = particle.opacity - reduction
            radius = particle.radius - (((reduction - 0) * (self.trailSize - self.trailRoundness*-.01)) / (self.trailOpacity - 0) + self.trailRoundness*-.01)
            
            if (opacity <= 0 or (radius)-0.0001 <= 0):
                particle.visible = False
            else:
                particle.opacity = opacity
                particle.radius = radius
                
    def GetLookDirection(self):
        angleVector = Vector2.angleTo(self.position.x, self.position.y, app.mouseX, app.mouseY)
        return angleVector
        
    def PlayerDamage(self):
        if (self.livesLeft == 1):
            PlayerDeath()
        
        else:
            self.livesLeft -= 1
            self.isImmune = True
            self.damageVignette.opacity = 50
            self.timeSinceLastHit = 0
            

##### PLAYER #####










##### BULLET #####

class Bullet:
    ### START
    def __init__(self, position, velocity, size):
        self.position = position
        self.velocity = velocity
        self.visual = Circle(self.position.x, self.position.y, size, fill='white', border='black', borderWidth=size/4)
        #self.visual.rotateAngle = angleTo(0, 0, self.velocity.x, self.velocity.y)
        
        self.hitCollider = Circle(self.position.x, self.position.y, size, opacity=0)
        self.hitCollider.parent = self
        
        self.visual.toBack()
        
        self.isFrozen = False
        
        self.despawnLimit = 25
        
        self.destroyed = False
        
        
        
    ### UPDATE
    def Update(self):
        
        if (not self.isFrozen):
            self.position.x += (self.velocity.x * Time.deltaTime)
            self.position.y += (self.velocity.y * Time.deltaTime)
            
            self.visual.centerX = self.position.x
            self.visual.centerY = self.position.y
            
            self.hitCollider.centerX = self.position.x
            self.hitCollider.centerY = self.position.y
        
        # Offscreen
        if ((self.position.x < -self.despawnLimit or self.position.x > 400 + self.despawnLimit) or (self.position.y < -self.despawnLimit or self.position.y > 400 + self.despawnLimit)):
            if (not isinstance(self, PlayerBullet)):
                player.bulletsAvoided += 1
            self.DestroySelf()
        
        # Blank Collisions
        if (player.blank != None and player.blank.hitsShape(self.hitCollider)):
            if (not isinstance(self, PlayerBullet)):
                self.DestroySelf()
                
                player.bulletsAvoided += 1
                
                Audio.PLAYER_BLANK_HIT[Audio.playerBlankHitCounter].play(restart=True)
                Audio.playerBlankHitCounter += 1
                Audio.playerBlankHitCounter %= len(Audio.PLAYER_BLANK_HIT)
                
        
        
        if (self.destroyed):
            self.visual.visible = False
            self.hitCollider.visible = False
            app.gameObjectList.remove(self)
            
        
    
    ### OTHER
    #@staticmethod
    #def Spawn(position = Vector2(200, 200), velocity = Vector2(0, 0), size = 5):
    #    bullet = Bullet(position, velocity, size)
    #    app.gameObjectList.append(bullet)
    #    return bullet
        
    def DestroySelf(self):
        self.destroyed = True
    

##### BULLET #####










##### PLAYER BULLET #####

class PlayerBullet(Bullet):
    
    ### START
    def __init__(self, position, velocity, damage):
        
        super().__init__(position, velocity, 5)
        
        self.visual.visible = False
        self.hitCollider.visible = False
        
        self.visual = Rect(self.position.x, self.position.y, 1.75, 40, fill=gradient('yellow', app.background, start='top'), align='center')
        self.visual.rotateAngle = angleTo(0, 0, self.velocity.x, self.velocity.y)
        self.hitCollider = Rect(self.position.x, self.position.y, 1.8, 45, opacity=0)
        self.hitCollider.parent = self
        
        self.damage = damage
        
        
        
    ### UPDATE
    def Update(self):
        
        # Hit Boss
        if (boss.OnCollision(self.hitCollider)):
            player.bulletsHit += 1
            self.DestroySelf()
            
            
        super().Update()
        
    
    ### OTHER
    @staticmethod
    def Spawn(position = Vector2(200, 200), velocity = Vector2(0, 0), damage = 2):
        bullet = PlayerBullet(position, velocity, damage)
        app.gameObjectList.append(bullet)
        return bullet

##### PLAYER BULLET #####



        
        
        
      
        
   
   
##### BOSS ##### 

class Attack(Enum):
    SPRAY = "SPRAY"
    DASH = "DASH"
    SPIN = "SPIN"
    STRAIGHT_SPIN = "STRAIGHT_SPIN"
    CROSS = "CROSS"
    ROTATING = "ROTATING"

class Boss:
    
    ### START
    def __init__(self):
        self.maxHealth = 700 #700
        self.health = self.maxHealth
        self.healthBar = BossHealthbarUI(self)
        
        self.position = Vector2(200, 200) # MOVE BACK TO (200, 75)
        
        self.velocity = Vector2()
        
        self.visual = Group(
            Circle(200, 200, 40, fill=rgb(255, 200, 50), border='black', borderWidth=2),
            Circle(185, 205, 5, fill='black'),
            Circle(215, 205, 5, fill='black'),
            #Oval(200, 200, 25, 10, fill=rgb(255, 0, 150), border='black'),
            Rect(200, 215, 47, 5, align='center'),
            )
        self.hitCollider = Circle(200, 200, 35, opacity=0)
        self.hitCollider.parent = self
        
        self.UpdateVisual()
        
        

        
        
        self.attackList = [Attack.SPRAY, Attack.DASH, Attack.SPIN, Attack.STRAIGHT_SPIN, Attack.CROSS] # no ROTATING
        
        self.attackLengthDictionary = {
            Attack.SPRAY: 5, # ANY (s)
            Attack.DASH: 3.5, # DASHES(dashCooldown + dashLength + dashBuffer) + (initialDashCooldown - dashCooldown)
            Attack.SPIN: 6, # ANY (s)
            Attack.STRAIGHT_SPIN: 7.25, # ANY (s)
            Attack.CROSS: 5.5, # 
            Attack.ROTATING: 999,
        }
        
        # Dash Attack Variables
        self.dashSpeed = 900
        self.initialDashCooldown = 1.1
        self.dashCooldown = .6
        self.dashBuffer = 0.4
        self.dashLength = .5
        self.isDashing = False
        self.isBuffering = False
        self.dashTimer = self.dashCooldown
        self.dashBulletSpeed = 250
        self.dashVisualLength = 500
        self.dashVisual = Rect(0, 0, self.dashVisualLength, 20, fill=gradient('orangeRed', 'gold', start='left'), dashes=True)
        self.dashVisual.toBack()
        self.dashVisual.visible = False
        
        # Spray Attack Variables
        self.moveSpeed = 35
        self.sprayBulletSpeed = 190
        self.shootCooldown = .07
        self.shootCooldownTimer = self.shootCooldown
        self.sprayAngle = 10
        
        # Spin Attack Variables
        self.spinBulletSpeed = 125
        self.spinShootCooldown = 0.065 # 0.06
        self.spinShootTimer = self.spinShootCooldown
        self.spinSpeed = 0.325 # 0.4
        self.spinDirection = Vector2(0.5, 0.5)
        
        # Straight Spin Attack Variables
        self.straightSpinBulletSpeed = 400
        self.straightSpinShootCooldown = 0.07
        self.straightSpinSpeed = 0.06
        self.inSpinPosition = False
        self.straightSpinWalkSpeed = 150
        #using spinDirection and spinShootTimer from above attack
        
        # Cross Attack Variables
        self.crossMoveSpeed = 60
        self.crossBulletSpeed = 1375
        self.crossCooldown = 0.85
        self.crossBuffer = 0.35
        self.isCrossBuffering = False
        self.crossSpawnDistance = 450
        self.crossTimer = self.crossCooldown
        self.crossBulletList = []
        self.crossTraceList = []
        
        self.duplicateAttack = False
        
        self.attackMode = None
        self.attackMode = self.GenerateNewAttack()
        self.attackTimerMax = self.attackLengthDictionary[self.attackMode]
        self.attackTimer = self.attackTimerMax
        
        self.ResetAttackVariables()
        
        
        self.deathAnimationPlaying = False
        self.deathOpacityRate = 10
        self.deathSpinRate = 600
        self.deathScaleRate = 25
        
        self.test = False
        
        
        
    ### UPDATE
    def Update(self):
        
        self.healthBar.Update()
        
        
        # DEATH
        if (self.health <= 0 and not self.deathAnimationPlaying):
            print("dead")
            self.deathAnimationPlaying = True
            
        if (self.deathAnimationPlaying):
            opacity = self.visual.opacity
            width = self.visual.width
            height = self.visual.height
            
            opacity -= self.deathOpacityRate * Time.deltaTime
            self.visual.rotateAngle += self.deathSpinRate * Time.deltaTime
            width -= self.deathScaleRate * Time.deltaTime
            height -= self.deathScaleRate * Time.deltaTime
            
            if (opacity < 0):
                opacity = 0
            if (width <= 0):
                width = 0.0001
            if (height <= 0):
                height = 0.0001
                
            self.visual.opacity = opacity
            self.visual.width = width
            self.visual.height = height
            
            self.dashVisual.visible = False
            for trace in self.crossTraceList:
                trace.visible = False
                
            if (self.visual.width <= 0.0001 or self.visual.opacity == 0):
                PlayerWin()
            
            return
    
        self.attackTimer -= Time.deltaTime
        if (self.attackTimer <= 0):
            self.attackMode = self.GenerateNewAttack()
    
        
        
        # SPRAY
        if (self.attackMode == Attack.SPRAY):
            # Move Towards Player
            inputDir = Vector2.angleTo(self.position.x, self.position.y, player.position.x, player.position.y)
            moveDir = inputDir * self.moveSpeed
            self.velocity = moveDir
            
            # Shoot Stuff
            self.shootCooldownTimer -= Time.deltaTime
            
            if (self.shootCooldownTimer <= 0):
                playerDirection = Vector2.angleTo(self.position.x, self.position.y, player.position.x, player.position.y)
                
                
                playerDirection.x += random.randrange(-self.sprayAngle, self.sprayAngle)/10
                playerDirection.y += random.randrange(-self.sprayAngle, self.sprayAngle)/10
                
                shootAngle = playerDirection.normalized
                shootDir = shootAngle * self.sprayBulletSpeed
                BossBullet.Spawn(Vector2(self.position.x, self.position.y), shootDir)
                
                self.shootCooldownTimer = self.shootCooldown
                
            #targetAngle = angleTo(0, 0, -self.velocity.x, -self.velocity.y)
            #self.visual.rotateAngle = Lerp(self.visual.rotateAngle, targetAngle, 0.075)
            
            self.SmoothlyRotate(Vector2(0, 0), Vector2(-self.velocity.x, -self.velocity.y), 0.035)
            

            
        # DASH
        elif (self.attackMode == Attack.DASH):
            if (not self.isDashing and not self.isBuffering):
                self.dashTimer -= Time.deltaTime
                self.SmoothlyRotate(Vector2(-self.position.x, -self.position.y), Vector2(-player.position.x, -player.position.y), 0.1)
                if (self.dashTimer <= 0):
                    self.isBuffering = True
                    self.dashTimer = self.dashBuffer
                    
                    inputDir = Vector2.angleTo(self.position.x, self.position.y, player.position.x, player.position.y)
                    moveDir = inputDir * self.dashSpeed
                    self.velocity = moveDir
                    
                    self.dashVisual.visible = True
                    
                    angleToPlayer = angleTo(self.position.x, self.position.y, player.position.x, player.position.y) - 90
                    #vectorToPlayer = Vector2.angleTo(self.position.x, self.position.y, player.position.x, player.position.y)
                    
                    self.dashVisual.rotateAngle = angleToPlayer
                    self.dashVisual.centerX = self.position.x + self.velocity.normalized.x*self.dashVisualLength/2
                    self.dashVisual.centerY = self.position.y + self.velocity.normalized.y*self.dashVisualLength/2
                    

                    
                    
            elif (not self.isDashing):
                self.dashTimer -= Time.deltaTime
                if (self.dashTimer <= 0):
                    self.isDashing = True
                    self.isBuffering = False
                    self.dashTimer = self.dashLength

                    Audio.BOSS_DASH.play(restart=True)
                    
                    BossHomingBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(-1, 0).normalized * self.dashBulletSpeed, 9.5)
                    BossHomingBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(-1, 1).normalized * self.dashBulletSpeed, 9.5)
                    BossHomingBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(0, 1).normalized * self.dashBulletSpeed, 9.5)
                    BossHomingBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(1, 1).normalized * self.dashBulletSpeed, 9.5)
                    BossHomingBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(1, 0).normalized * self.dashBulletSpeed, 9.5)
                    BossHomingBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(1, -1).normalized * self.dashBulletSpeed, 9.5)
                    BossHomingBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(0, -1).normalized * self.dashBulletSpeed, 9.5)
                    BossHomingBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(-1, -1).normalized * self.dashBulletSpeed, 9.5)
                    
                    
                    
            elif (self.isDashing):
                self.dashTimer -= Time.deltaTime
                
                if (self.velocity.normalized.magnitude != 0):
                    self.dashVisual.centerX = self.position.x + self.velocity.normalized.x*self.dashVisualLength/2
                    self.dashVisual.centerY = self.position.y + self.velocity.normalized.y*self.dashVisualLength/2
                if (self.dashTimer <= 0):
                    self.isDashing = False
                    self.dashTimer = self.dashCooldown
                    self.dashVisual.visible = False
                
                    
                    
        # SPIN
        elif (self.attackMode == Attack.SPIN):
            self.spinShootTimer -= Time.deltaTime
            
            if (self.spinShootTimer <= 0):
    
                BossBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(self.spinDirection.x, self.spinDirection.y).normalized * self.spinBulletSpeed, 23)
                #BossBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(self.spinDirection.y, -self.spinDirection.x).normalized * self.spinBulletSpeed, 23)
                BossBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(-self.spinDirection.x, -self.spinDirection.y).normalized * self.spinBulletSpeed, 23)
                #BossBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(-self.spinDirection.y, self.spinDirection.x).normalized * self.spinBulletSpeed, 23)
                
                self.spinDirection.x = (math.cos(self.spinSpeed) * self.spinDirection.x) - (math.sin(self.spinSpeed) * self.spinDirection.y)
                self.spinDirection.y = (math.sin(self.spinSpeed) * self.spinDirection.x) + (math.cos(self.spinSpeed) * self.spinDirection.y)
                
                self.spinShootTimer = self.spinShootCooldown

                
                    
        # STRAIGHT SPIN
        elif (self.attackMode == Attack.STRAIGHT_SPIN):
            
            if (not self.inSpinPosition):
                inputDir = Vector2.angleTo(self.position.x, self.position.y, 200, 200)
                moveDir = inputDir * self.straightSpinWalkSpeed
                self.velocity = moveDir
                
                self.SmoothlyRotate(Vector2(0, 0), Vector2(-self.velocity.x, -self.velocity.y), 0.08)
                
                if (((self.position.x >= 200 and self.position.x - 1 <= 200) or (self.position.x <= 200 and self.position.x + 1 >= 200)) and ((self.position.y >= 200 and self.position.y - 1 <= 200) or (self.position.y <= 200 and self.position.y + 1 >= 200))):
                    self.position.x = 200
                    self.position.y = 200
                    self.inSpinPosition = True
            
            else:
                self.velocity = Vector2(0, 0)
                
                self.SmoothlyRotate(Vector2(0, 0), Vector2(0, -1), 0.08)
                
                self.spinShootTimer -= Time.deltaTime
                
                if (self.spinShootTimer <= 0):
        
                    BossBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(self.spinDirection.x, self.spinDirection.y).normalized * self.straightSpinBulletSpeed, 18)
                    BossBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(self.spinDirection.y, -self.spinDirection.x).normalized * self.straightSpinBulletSpeed, 18)
                    BossBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(-self.spinDirection.x, -self.spinDirection.y).normalized * self.straightSpinBulletSpeed, 18)
                    BossBullet.Spawn(Vector2(self.position.x, self.position.y), Vector2(-self.spinDirection.y, self.spinDirection.x).normalized * self.straightSpinBulletSpeed, 18)
                    
                    self.spinDirection.x = (math.cos(self.straightSpinSpeed) * self.spinDirection.x) - (math.sin(self.straightSpinSpeed) * self.spinDirection.y)
                    self.spinDirection.y = (math.sin(self.straightSpinSpeed) * self.spinDirection.x) + (math.cos(self.straightSpinSpeed) * self.spinDirection.y)
                    
                    self.spinShootTimer = self.straightSpinShootCooldown
                
                
                
        # CROSS
        elif (self.attackMode == Attack.CROSS):
            
            if (not self.isCrossBuffering):
                self.crossTimer -= Time.deltaTime
                

                
                if (self.crossTimer <= 0):
                    
                    if (len(self.crossTraceList) != 0):
                        for line in self.crossTraceList:
                            line.visible = False
                        self.crossTraceList.clear()
                    
                    for i in range(6):
                        randomDir = Vector2(random.randrange(-100, 100), random.randrange(-100, 100)).normalized
                        spawnPos = randomDir * self.crossSpawnDistance
                        spawnPos.x += player.position.x
                        spawnPos.y += player.position.y
                        moveDir = Vector2.angleTo(spawnPos.x, spawnPos.y, player.position.x, player.position.y) * self.crossBulletSpeed
                        
                        bullet = BossBullet.Spawn(Vector2(spawnPos.x, spawnPos.y), moveDir, 8)
                        bullet.visual.toFront()
                        bullet.isFrozen = True
                        bullet.despawnLimit = 900
                        self.crossBulletList.append(bullet)
                        
                        traceLine = Rect(bullet.position.x, bullet.position.y, 1900, 3, fill='yellow', align='center')
                        traceLine.toBack()
                        
                        angleToPlayer = angleTo(bullet.position.x, bullet.position.y, player.position.x, player.position.y) - 90
                        
                        traceLine.rotateAngle = angleToPlayer
                        self.crossTraceList.append(traceLine)
                        
                        Audio.BOSS_CROSS_INITIATE.play(restart=True)
                        
                    self.crossTimer = self.crossBuffer
                    self.isCrossBuffering = True
                    
            elif (self.isCrossBuffering):
                self.crossTimer -= Time.deltaTime
                
                if (self.crossTimer <= 0):
                    for bullet in self.crossBulletList:
                        bullet.isFrozen = False
                    self.crossBulletList.clear()
                    
                    self.isCrossBuffering = False
                    self.crossTimer = self.crossCooldown
                    
                    Audio.BOSS_CROSS_FIRE.play(restart=True)
                
            self.velocity = Vector2.angleTo(self.position.x, self.position.y, player.position.x, player.position.y) * self.crossMoveSpeed
            self.SmoothlyRotate(Vector2(0, 0), Vector2(-self.velocity.x, -self.velocity.y), 0.075)
            
    
        
        # ROTATING    
        elif (self.attackMode == Attack.ROTATING):
            if (not self.test):
                angleToPlayer = Vector2.angleTo(self.position.x, self.position.y, player.position.x, player.position.y)
                BossRotatingBullet.Spawn(Vector2(self.position.x, self.position.y), angleToPlayer * 100, 10, 0.1)
                self.test = True
            
            
            
            
                    
        velocity = Vector2()
        velocity.x = self.velocity.x * Time.deltaTime
        velocity.y = self.velocity.y * Time.deltaTime
        
        if (self.attackMode == Attack.STRAIGHT_SPIN or self.attackMode == Attack.SPRAY or self.attackMode == Attack.CROSS or (self.attackMode == Attack.DASH and self.isDashing)):
            
            if (self.position.x + velocity.x <= 400-self.hitCollider.radius and self.position.x + velocity.x >= 0+self.hitCollider.radius):
                self.position.x += velocity.x
            elif (self.attackMode == Attack.DASH):
                self.velocity = Vector2()
            if (self.position.y + velocity.y <= 400-self.hitCollider.radius and self.position.y + velocity.y >= 0+self.hitCollider.radius):
                self.position.y += velocity.y
            elif (self.attackMode == Attack.DASH):
                self.velocity = Vector2()
        
        #vectorToPlayer = Vector2.angleTo(self.position.x, self.position.y, player.position.x, player.position.y)
        
        if (self.hitCollider.hitsShape(player.hitCollider)):
            player.OnCollision(self.hitCollider)

        
        self.UpdateVisual()
    
    
    
    
    ### OTHER
    def UpdateVisual(self):
        self.visual.centerX = self.position.x
        self.visual.centerY = self.position.y
        
        self.hitCollider.centerX = self.visual.centerX
        self.hitCollider.centerY = self.visual.centerY
        
    def SmoothlyRotate(self, startPos, targetPos, t):
        targetAngle = angleTo(startPos.x, startPos.y, targetPos.x, targetPos.y)
        currentAngle = self.visual.rotateAngle
        
        delta = (targetAngle - currentAngle + 180) % 360 - 180
        
        lerpedAngleDifference = Lerp(0, delta, t)
        
        lerpedAngle = (currentAngle + lerpedAngleDifference) % 360
        
        self.visual.rotateAngle = lerpedAngle
        
    def ResetAttackVariables(self):
        self.velocity = Vector2()
        
        self.duplicateAttack = False
        
        self.dashVisual.visible = False
        self.dashTimer = self.initialDashCooldown
        self.isDashing = False
        self.isBuffering = False
        
        self.spinDirection = Vector2(0.5, 0.5)
        self.spinShootTimer = self.spinShootCooldown
        
        self.inSpinPosition = False
        
        self.isCrossBuffering = False
        self.crossTimer = self.crossCooldown
        if (len(self.crossTraceList) != 0):
            for line in self.crossTraceList:
                line.visible = False
            self.crossTraceList.clear()
        if (len(self.crossBulletList) != 0):
            for bullet in self.crossBulletList:
                bullet.DestroySelf()
            
        
    def GenerateNewAttack(self, override = None):
        
        while True: 
            index = random.randrange(len(self.attackList))
            if (not self.duplicateAttack): 
                break
            elif (self.attackMode != self.attackList[index]):
                break
                
        self.ResetAttackVariables()
        
        self.attackTimerMax = self.attackLengthDictionary[self.attackList[index]]
        self.attackTimer = self.attackTimerMax
        
        if (self.attackMode == self.attackList[index]):
            self.duplicateAttack = True
            
        print(f"Generated attack mode: {self.attackList[index].value}")
        
        
        # Spin Initialize
        if (self.attackList[index] == Attack.SPIN):
            self.velocity = Vector2(0.5, 0.5)
        
        
        return self.attackList[index]
    
    def OnCollision(self, other):
        if (self.hitCollider.hitsShape(other)):
            if (isinstance(other.parent, PlayerBullet)):
                self.healthBar.ResetLagDelay()
                self.health -= other.parent.damage
                Audio.BOSS_DAMAGE.play(restart=True)
            return True
            
        return False
        

##### BOSS #####










##### BOSS BULLET #####

class BossBullet(Bullet):
    @staticmethod
    def Spawn(position = Vector2(200, 200), velocity = Vector2(0, 0), size = 5):
        bullet = BossBullet(position, velocity, size)
        app.gameObjectList.append(bullet)
        return bullet
        
    # UPDATE
    def Update(self):
        
        if (player.OnCollision(self.hitCollider)):
            if (not player.isDashing):
                self.DestroySelf()
        
        super().Update()

##### BOSS BULLET #####










##### BOSS HOMING BULLET #####

class BossHomingBullet(Bullet):
    
    ### START
    def __init__(self, position, velocity, size, homingStrength, maxLife):
        super().__init__(position, velocity, size)

        self.homingStrength = homingStrength
        
        self.maxLife = maxLife
        self.lifeTimer = 0
        
        
        
    ### UPDATE
    def Update(self):
        
        self.lifeTimer += Time.deltaTime
        
        
        playerDir = Vector2.angleTo(self.position.x, self.position.y, player.position.x, player.position.y)
        
        moveDir = playerDir * self.homingStrength
        
        self.velocity += moveDir

        if (self.lifeTimer >= self.maxLife):
            player.bulletsAvoided += 1
            
            self.DestroySelf()
            
            
        if (player.OnCollision(self.hitCollider)):
            if (not player.isDashing):
                self.DestroySelf()
        
        
        super().Update()
        
    
    ### OTHER
    @staticmethod
    def Spawn(position = Vector2(200, 200), velocity = Vector2(0, 0), size = 5, homingStrength = 10, maxLife = 1):
        bullet = BossHomingBullet(position, velocity, size, homingStrength, maxLife)
        app.gameObjectList.append(bullet)
        return bullet

##### BOSS HOMING BULLET #####










##### BOSS ROTATING BULLET #####

class BossRotatingBullet(Bullet):
    
    ### START
    def __init__(self, position, velocity, size, rotateSpeed):
        super().__init__(position, velocity, size)
        
        self.magnitude = self.velocity.magnitude / 10

        self.rotateSpeed = rotateSpeed
        
        
    ### UPDATE
    def Update(self):
        
        oldMagnitude = self.velocity.magnitude
        
        xRot = ((math.cos(self.rotateSpeed) * (self.velocity.x - boss.position.x) - math.sin(self.rotateSpeed) * (boss.position.y - self.velocity.y))) + boss.position.x
        yRot = boss.position.y - ((math.sin(self.rotateSpeed) * (self.velocity.x - boss.position.x) + math.cos(self.rotateSpeed) * (boss.position.y - self.velocity.y)))
        
        rotation = Vector2(xRot, yRot)
        
        self.position.x += rotation.x * Time.deltaTime
        self.position.y += rotation.y * Time.deltaTime
        
        #self.velocity.magnitude = oldMagnitude
        
        print(self.velocity)
        print(self.velocity.magnitude)
        print("")
        
        self.visual.toFront()
        
        if (player.OnCollision(self.hitCollider)):
            if (not player.isDashing):
                self.DestroySelf()
        
        super().Update()
        
        
    @staticmethod
    def Spawn(position = Vector2(200, 200), velocity = Vector2(0, 0), size = 5, rotateSpeed = 1):
        bullet = BossRotatingBullet(position, velocity, size, rotateSpeed)
        app.gameObjectList.append(bullet)
        return bullet

##### BOSS ROTATING BULLET #####










##### BOSS HEALTHBAR #####

class BossHealthbarUI:
    
    ### START
    def __init__(self, targetBoss):
        self.boss = targetBoss

        self.background = Rect(200, 20, 320, 18, align='center')
        
        self.leftAnchor = self.background.left + 3
        self.rightAnchor = self.background.right - 3
        self.width = 314
        
        self.fillLag = Rect(self.leftAnchor, self.background.top + 3, self.width, 12, fill=rgb(255, 240, 0))
        self.fill = Rect(self.leftAnchor, self.background.top + 3, self.width, 12, fill='red')
        
        self.visualGroup = Group()
        self.visualGroup.add(self.background, self.fillLag, self.fill)
        
        self.maxLagDelay = 0.5
        self.lagDelayTimer = 0
        
        self.lagBufferLimit = 5
        self.lagBufferTimer = 0
        
        self.lerpSpeed = 0.0875
        
        
        
    ### UPDATE    
    def Update(self):
        self.lagDelayTimer += Time.deltaTime
        if (self.lagDelayTimer < self.maxLagDelay):
            self.lagBufferTimer += Time.deltaTime
            
        if (self.fillLag.width - 3 <= self.fill.width):
            self.lagBufferTimer = 0
        
        newWidth = self.ConvertedWidth()
        
        if (newWidth <= 0):
            newWidth = 0.0001
            
        self.fill.width = newWidth
        self.fill.left = self.leftAnchor
        
        if (self.lagDelayTimer >= self.maxLagDelay or self.lagBufferTimer >= self.lagBufferLimit):
            newLagWidth = Lerp(self.fillLag.width, self.fill.width, self.lerpSpeed)
            if (self.lagBufferTimer < self.lagBufferLimit):
                self.lagBufferTimer = 0
            
            if (newLagWidth - 0.5 <= self.fill.width):
                newLagWidth = self.fill.width
            
            self.fillLag.width = newLagWidth
            self.fillLag.left = self.leftAnchor
            
        if (self.visualGroup.hitsShape(player.visual)):
            self.visualGroup.opacity = 25
            self.fillLag.fill = 'crimson'
        else:
            self.visualGroup.opacity = 100
            self.fillLag.fill = rgb(255, 240, 0)
            
        self.visualGroup.toFront()
        
        
        
        
    ### OTHER
    def ConvertedWidth(self):
        return (self.boss.health) * (self.rightAnchor - self.leftAnchor) / (self.boss.maxHealth)
        
    def ResetLagDelay(self):
        self.lagDelayTimer = 0
        
        
        
        

##### BOSS HEALTHBAR #####
   
   
   
   
   
   
   
   
   
   
##### AWAKE #####

app.background = rgb(100, 102, 105)

app.mouseX = 200
app.mouseY = 200

app.gameObjectList = [] # list to store all objects with (ONLY WITH) their own Update() methods

##### AWAKE #####



        
        
##### START #####

player = Player()

boss = Boss()
    
app.tutorial = [
        Label("'LMB' to fire", 200, 325, size=20, fill='white', opacity=25),
        Label("'Space' to dash", 200, 350, size=20, fill='white', opacity=25),
        Label("'RMB' to fire blank", 200, 375, size=20, fill='white', opacity=25),
    ]
    

##### START #####




   
##### UPDATE #####
        
app.stepsPerSecond = 60
app.timeFromStart = 0

def onStep():
    app.timeFromStart += Time.deltaTime
    
    player.Update()
    
    if (app.timeFromStart > 2):
        boss.Update()
        
    # Tutorial Clearing
    if (Input.GetKeyDown('space')):
        RemoveTutorialIndex(1)
    if (Input.GetMouseDown(0)):
        RemoveTutorialIndex(0)
    if (Input.GetMouseDown(1)):
        RemoveTutorialIndex(2)
    
    Input.Update()
    Time.Update()
    
    for gameObject in app.gameObjectList:
        gameObject.Update()
        
        

        
##### UPDATE #####





##### BUILT-IN FUNCTIONS #####

def onKeyPress(key):
    Input.keyDownList.append(key)
    
def onKeyRelease(key):
    Input.keyUpList.append(key)
    
def onKeyHold(keys):
    for key in keys:
        Input.keyHeldList.append(key)
        
def onMouseMove(x, y):
    app.mouseX = x
    app.mouseY = y
        
def onMouseDrag(x, y):
    app.mouseX = x
    app.mouseY = y
    
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
    

        


##### BUILT-IN FUNCTIONS #####
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        