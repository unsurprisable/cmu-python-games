import random

app.background = gradient('mediumSlateBlue', 'cornflowerBlue', 'cornflowerBlue', 'deepSkyBlue',start='top')

app.pipeList = []


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y




def NewPipe(posX):
    pipeGroup = Group(
        Rect(168, 145, 64, 30, fill=gradient('limeGreen', 'lime', start='top'), border='forestGreen', borderWidth=4),
        Rect(168, 255, 64, 30, fill=gradient('limeGreen', 'lime', start='bottom'), border='forestGreen', borderWidth=4),
        Rect(179, -201, 42, 350, fill=gradient('limeGreen', 'forestGreen', start='bottom'), border='forestGreen', borderWidth=4),
        Rect(179, 281, 42, 350, fill=gradient('limeGreen', 'forestGreen', start='top'), border='forestGreen', borderWidth=4)
        )
    pipeGroup.centerX = posX
    pipeGroup.centerY = random.randrange(75, 325)
    
    pipeGroup.pastPlayer = False
        
    app.pipeList.append(pipeGroup)
    
    return pipeGroup
    
def DeletePipe(pipe):
    if (pipe in app.pipeList):
        app.pipeList.remove(pipe)
        pipe.visible = False
    else:
        print("ERROR: Could not find the referenced pipe in 'app.pipeList'")
        
def Jump():
    player.velocity.y = player.jumpSpeed
    
def AddScore(amount):
    app.score += amount
    app.scoreText.value = str(app.score)
    
def GameOver():
    Rect(0,0,400,400, opacity=75)
    Label("GAME OVER!", 200, 200, size=56, fill='white', font='monospace', bold=True)
    app.stop()




##### START #####

player = Group()

player.visual = Label(chr(0x2711), 100, 100, size=46, fill='yellow', font='symbols')
player.hitBox = Circle(100, 100, 10, opacity=0)

player.add(player.visual)
player.add(player.hitBox)

player.jumpSpeed = 5
player.velocity = Vector2(0, 5)
player.maxDownVelocity = -6

app.gravity = -0.3



NewPipe(350).toFront()
NewPipe(550).toFront()
NewPipe(750).toFront()



app.speed = 2
app.score = 0
app.scoreText = Label(str(app.score), 200, 35, size=50, font='monospace', fill='white', bold=True)

app.scoreText.toFront()


app.countdownTimer = 2
app.countdownVisual = Group()

app.countdownTimerText = Label(str(app.countdownTimer), 200, 200, size=152, fill='white', bold=True, italic=True)

app.countdownVisual.add(
    Rect(0,0,400,400, opacity=50),
    app.countdownTimerText
    )
    
app.gameStarted = False

##### START #####



### JUMP
def onKeyPress(keys):
    if ('w' or 'f' or 'up' or 'e' or 'space' in keys):
        Jump()
        
def onMousePress(msX, msY):
    Jump()

app.stepsPerSecond = 60
def onStep():
    
    ### Countdown
    if (rounded((app.countdownTimer-1/60)+0.499) < rounded(app.countdownTimer+0.499)):
        app.countdownTimerText.value = rounded((app.countdownTimer-1/60)+0.499)
    app.countdownTimer -= 1/60
    
    if (app.countdownTimer <= 0):
        app.gameStarted = True
        app.countdownVisual.visible = False
    
    if (not app.gameStarted):
        return
    
    ### Player
    
    if (player.centerY < 0 or player.centerY > 400):
        GameOver()
    
    if (player.velocity.y + app.gravity >= player.maxDownVelocity):
        player.velocity.y += app.gravity
    else:
        player.velocity.y = player.maxDownVelocity
    
    player.centerY -= player.velocity.y
    
    
    ### Gameplay
    
    # Pipe Updates
    for pipe in app.pipeList:
        if (pipe.hitsShape(player.hitBox)):
            GameOver()
        
        pipe.centerX -= app.speed
        if (pipe.centerX <= -150):
            DeletePipe(pipe)
            NewPipe(450).toFront()
            app.scoreText.toFront()
            
        if (not pipe.pastPlayer and player.centerX > pipe.centerX):
            pipe.pastPlayer = True
            AddScore(1)
        
    

