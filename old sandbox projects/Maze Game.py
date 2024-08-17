# August 2023

app.background = gradient(rgb(60, 75, 120), rgb(80, 110, 255), rgb(90, 180, 255), start='top-left')

app.currentLevel = 0

pathColor = 'black'
pathBorderColor = rgb(45, 45, 45)

finishColor = 'lightGreen'
finishBorderColor = 'limeGreen'
finishTextColor = 'green'

borderMultiplier = 0.075

app.gameIsActive = False
app.pathList = []

app.finishButton = Rect(0,0,1,1,visible=False)
app.finishButtonText = Label("",0,0)

    
def NewPath(posX, posY, width, height):
    finalBorderWidth = 0.0
    if (width == height or width < height):
        finalBorderWidth = width * borderMultiplier
    else:
        finalBorderWidth = height * borderMultiplier
        
    path = Rect(posX - width/2, posY - height/2, width, height, fill=pathColor, border=pathBorderColor, borderWidth=finalBorderWidth)
    app.pathList.append(path)
    
def NewFinish(posX, posY, width, height):
    finalBorderWidth = 0.0
    if (width == height or width < height):
        finalBorderWidth = width * borderMultiplier
    else:
        finalBorderWidth = height * borderMultiplier
        
    app.finishButton = Rect(posX - width/2, posY - height/2, width, height, fill=finishColor, border=finishBorderColor, borderWidth=finalBorderWidth)
    app.finishButtonText = Label("Finish", posX, posY, size=finalBorderWidth*4, fill=finishTextColor, bold=True, font='monospace')
    
    

def LoadLevel(level):
    if (len(app.pathList) > 0):
        for path in app.pathList:
            path.visible = False
        app.pathList.clear()
    app.finishButton.visible = False
    app.finishButtonText.visible = False

        
        
    if (level == 1):
        app.background = gradient(rgb(0, 15, 60), rgb(20, 50, 175), rgb(30, 120, 255), start='top-left')
        
        NewPath(200, 200, 90, 400)
        NewFinish(200, 30, 90.25, 60)
        
        app.currentLevel = 1
    elif (level == 2):
        app.background = gradient(rgb(0, 60, 15), rgb(20, 175, 50), rgb(30, 255, 120), start='bottom-right')
        
        NewPath(125, 30, 250, 60)
        
        app.currentLevel = 2
    elif (level == 3):
        
        
        app.currentLevel = 3
    elif (level == 4):
        
        
        app.currentLevel = 4
    else:
        print(f"Trying to load a level that doesn't exist!: 'Level {app.currentLevel}'")
    

def LoadNextLevel():
    LoadLevel(app.currentLevel + 1)
    



app.startButton = Rect(0,0,1,1,visible=False)

def StartGame():
    app.startButton.visible = False
    app.gameIsActive = True
    LoadLevel(1)

def GameOver():
    Rect(0, 0, 400, 400, opacity=85)
    Label("Game Over!", 200, 170, size=52, fill='white', bold=True, font='monospace')
    Label("You didn't follow the path!", 200, 215, size=20, fill=rgb(240, 240, 240), bold=True, font='monospace')
    app.stop()
    
    

    
    
##### START #####

startButton = Rect(155, 340, 90, 60, fill='lightGray', border='gray', borderWidth=4)
Label("START", 200, 370, size=22, fill='darkGray', font='monospace', bold=True)

##### START #####

    
    
def onMousePress(msX, msY):
    if (startButton.contains(msX, msY)):
        StartGame()
    if (app.finishButton.contains(msX, msY)):
        LoadNextLevel()
    
def onMouseMove(msX, msY):
    if (app.gameIsActive):
        totalHits = 0
        for path in app.pathList:
            if (path.contains(msX, msY)):
                totalHits += 1
        if (totalHits == 0):
            GameOver()
    
    