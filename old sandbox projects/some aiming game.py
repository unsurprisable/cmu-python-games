# August 2023

import random


# Background
Rect(0, 0, 400, 400, fill=gradient('darkTurquoise', 'dodgerBlue'))

width = 50
height = 50
evilSizeMultiplier = 5.5
gameScore = 0


class ActiveSquare:
    def __init__(self):
        self.isEvil = False
        self.currentSquare = None
        
        self.finalWidth = width
        self.finalHeight = height
        
        self.fillColor = rgb(255, 0, 255)


    def DeleteSelf(self):
        self.currentSquare.visible = False
        self.currentSquare = None
        
        
    def GenerateNewSquare(self, addScore = True):
        self.finalWidth = width
        self.finalHeight = height
        
        if (random.randint(1, 5) == 1):
            self.isEvil = True
            self.fillColor = 'orangeRed'
            self.finalWidth = int(self.finalWidth * evilSizeMultiplier)
            self.finalHeight = int(self.finalHeight *evilSizeMultiplier)
        else:
            self.isEvil = False
            self.fillColor = 'limeGreen'
            
        if (self.finalWidth % 2 != 0):
            self.finalWidth+=1
        if (self.finalHeight % 2 != 0):
            self.finalHeight+=1
            
        positionX = random.randint(self.finalWidth/2, 400-self.finalWidth/2)
        positionY = random.randint(self.finalHeight/2, 400-self.finalHeight/2)
        
        if (self.currentSquare != None):
            self.DeleteSelf()
        
        
        finalBorderWidth = 9 if (self.isEvil == True) else 3
        self.currentSquare = Rect(positionX-self.finalWidth/2, positionY-self.finalHeight/2, self.finalWidth, self.finalHeight, fill=self.fillColor, border='black', borderWidth=finalBorderWidth)
      
        #gameScore += 1 if (addScore) else 0


activeSquare = ActiveSquare()

dim = Rect(0, 0, 400, 400, opacity=50)

label = Label("3", 200, 200, size=128, bold=True)
sleep(1)
label.visible = False
label = Label("2", 200, 200, size=128, bold=True)
sleep(1)
label.visible = False
label = Label("1", 200, 200, size=128, bold=True)
sleep(1)
label.visible = False
dim.visible = False

activeSquare.GenerateNewSquare()

scoreText = Label(gameScore, 200, 25, size=40, bold=True)


def onMousePress(mouseX, mouseY):
    if (not activeSquare.isEvil and activeSquare.currentSquare.contains(mouseX, mouseY)):
        activeSquare.GenerateNewSquare(True)
    elif (activeSquare.isEvil and not activeSquare.currentSquare.contains(mouseX, mouseY)):
        activeSquare.GenerateNewSquare(True)
    else:
        return
    
    scoreText.value = gameScore
