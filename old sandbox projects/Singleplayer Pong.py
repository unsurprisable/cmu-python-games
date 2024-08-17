import random
import math

class Vector2:
    def __init__(self, x, y):
        self._magnitude = 0
        self._x = 0
        self._y = 0
        
        self.x = x
        self.y = y
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, newX):
        self._x = newX
        self._magnitude = distance(self._x, 0, 0, self._y)
        
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, newY):
        self._y = newY
        self._magnitude = distance(self._x, 0, 0, self._y)
        
    @property
    def magnitude(self):
        return self._magnitude
    @magnitude.setter
    def magnitude(self, newMagnitude):
        multiplier = newMagnitude/self._magnitude

        self._magnitude = newMagnitude
        
        self._x *= multiplier
        self._y *= multiplier
        
    def Normalize(self):
        self._x /= self.magnitude
        self.y /= self.magnitude
        return self.magnitude
    
        
        
        
##### START #####
app.background = 'black'

player = Rect(100, 350, 200, 10, fill='white')

player.hitSizeMultiplier = 0.95

ball = Circle(200, 200, 6, fill='white')
ball.velocity = Vector2(random.randrange(-5, 5), random.randrange(2, 7))

ball.speed = 3
ball.hitSpeedMultiplier = 1.1

ball.velocity.magnitude = (ball.velocity.Normalize() * ball.speed)


print(ball.velocity.magnitude)

app.counter = 0
##### START #####


def onMouseMove(msX, msY):
    player.centerX = msX


app.stepsPerSecond = 60
def onStep():
    ### Ball
    
    ball.centerX += ball.velocity.x
    ball.centerY -= ball.velocity.y
    
    # Walls
    if (ball.top <= 0):
        ball.top = 0
        ball.velocity.y = -(ball.velocity.y)
    elif (ball.bottom >= 400):
        ball.bottom = 400
        ball.velocity.y = -(ball.velocity.y)
    if (ball.left <= 0):
        ball.left = 0
        ball.velocity.x = -(ball.velocity.x)
    elif (ball.right >= 400):
        ball.right = 400
        ball.velocity.x = -(ball.velocity.x)
        
    # Player
    if (ball.bottom >= player.top and ball.left >= player.left and ball.right <= player.right and ball.top <= player.top):
        ball.bottom = player.top
        ball.velocity.magnitude *= ball.hitSpeedMultiplier
        ball.velocity.y = -(ball.velocity.y)
        player.width *= player.hitSizeMultiplier
        
        
        

