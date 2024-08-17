# April 2024

import random
colors = [rgb(255,0,0), rgb(255,151,0), rgb(255,255,0), rgb(0,220,0), rgb(0,151,255), rgb(0,0,255), rgb(151,0,255), rgb(255,0,151)]


disks, start, end, sleepTime = 4*(-1,)
while disks < 2 or disks > 8:
    disks = int(app.getTextInput("How many disks do you want? (2-8)"))
while start < 1 or start > 3:
    start = int(app.getTextInput("What peg do you want to start at? (1-3)"))
while end < 1 or end > 3 or end == start:
    end = int(app.getTextInput("What peg do you want to end at? (1-3)"))
while sleepTime < 0:
    sleepTime = int(app.getTextInput("How long between moves? (in milliseconds)"))/1000

class Disk:
    HEIGHT = 30
    def __init__(self, width):
        self.visual = Rect(0, 0, width, Disk.HEIGHT, fill=colors.pop(0), align='center')

class Peg:
    def __init__(self, posX):
        self.visual = Line(posX, 0, posX, 400, lineWidth=4)
        self.stack = []
        
    def removeDisk(self):
        return self.stack.pop()
        
    def addDisk(self, disk):
        self.stack.append(disk)
        disk.visual.centerX = self.visual.centerX
        disk.visual.centerY = 400 - (len(self.stack)-1) * Disk.HEIGHT - Disk.HEIGHT/2
        
pegs = [Peg(100), Peg(200), Peg(300)]

for i in range(1, disks+1):
    pegs[start-1].addDisk(Disk(75 - 8*i))
    
def moveDisk(start, end):
    sleep(sleepTime)
    pegs[end-1].addDisk(pegs[start-1].removeDisk())
    print(f"{start} to {end}")
    
    
def solveTower(n, start, end):
    if (n == 0):
        return
    
    other = 6 - start - end
    
    solveTower(n-1, start, other)
    moveDisk(start, end)
    solveTower(n-1, other, end)
    

solveTower(disks, start, end)

Rect(200, 50, 400, 75, fill='white', align='center', border='black')
Label("DONE!", 200, 50, size=64)
    