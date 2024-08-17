# April 2024

#####
"""
Made in 7 days.
Based on Balatro (developed by LocalThunk).
Audio pulled directly from Balatro.
Currently has 30 unique, fully functional Jokers from Balatro.
Also has 1 original Joker that is not in Balatro.

Has as much content as possible; constrained by the 100 KB filesize limit.
(My code structuring had to be completely destroyed just to save some space.)

"""
#####



import time
import math
import random
from enum import Enum


app.font = 'montserrat'

audioWarning = Group(Rect(0,0, 400,400),Label("Loading Audio...", 200, 340, font=app.font, size=42, fill='white', bold=True),
Label("(refresh the page if there's an error)", 200, 375, font=app.font, size=19, fill='white')
)

sleep(0.01)

class Audio:
    MAIN_THEME = Sound('cmu://682887/29279892/Balatro+Main+Theme.mp3')
    BUTTON_CLICK = Sound('cmu://682887/29279953/ButtonClick.mp3')
    ANTE_UP = Sound('cmu://682887/29279955/RoundStart.mp3')
    CARD_HOVER_1 = Sound('cmu://682887/29279957/CardHover1.mp3')
    CARD_HOVER_2 = Sound('cmu://682887/29279959/CardHover2.mp3')
    CARD_HOVER_3 = Sound('cmu://682887/29279960/CardHover3.mp3')
    CARD_SELECT = Sound('cmu://682887/29279962/CardSelect.mp3')
    CARD_DESELECT = Sound('cmu://682887/29279963/CardDeselect.mp3')
    CHIPS_ADDED = Sound('cmu://682887/29279975/ChipsAdded.mp3')
    MULT_ADDED = Sound('cmu://682887/29315210/MultAdded.mp3')
    MULT_MULTIPLIED = Sound('cmu://682887/29316175/MultMultiplied.mp3')
    CHIPS_CALCULATED = Sound('cmu://682887/29279976/ChipsCalculated.mp3')
    TOTAL_CHIPS_ADDED = Sound('cmu://682887/29279977/TotalChipsAdded.mp3')

audioWarning.visible = False

Audio.MAIN_THEME.play(loop=True)



class GameSpeed:
    SLOW = 2
    NORMAL = 1
    SUPER_FAST = 0.5
    options = [ SLOW, NORMAL, SUPER_FAST ]
app.gameSpeed = GameSpeed.NORMAL



class Time:
    lastTime = 0
    deltaTime = 0
    def Update():
        if (Time.lastTime != 0):
            Time.deltaTime = time.time() - Time.lastTime
        Time.lastTime = time.time()



class CoroutineStage:
    def __init__(self):
        self.indexes = []

# ima be honest i have no idea how i got this to work but it works
# (from the future) luckily i didn't end up needing to modify this :D
class Coroutine:
    activeCoroutines = []
    endedCoroutines = []
    Instance = None
    def __init__(self):
        self.timeLeft = 0
        self.args = None
    def setStage(self, index):
        self.stageIndex = index
        self.stage = self.stages[self.stageIndex]
    def nextStage(self):
        self.stageIndex += 1
        if (self.stageIndex > len(self.stages)-1):
            self.end()
            return
        self.stage = self.stages[self.stageIndex]
    def nextStep(self, step):
        pass
    def runNextStep(self):
        if (self.args is not None):
            self.timeLeft = self.nextStep(self.stage, *self.args)
        else:
            self.timeLeft = self.nextStep(self.stage)

    def resetBaseVars(self):
        self.stageIndex = 0
        self.stage = self.stages[self.stageIndex]
        self.timeLeft = 0
        self.hasEnded = False
    def resetVars(self):
        pass
    def start(self, stages, args=None):
        self.stages = stages
        self.resetBaseVars()
        self.resetVars()
        self.args = args
        Coroutine.activeCoroutines.append(self)
    def end(self):
        Coroutine.endedCoroutines.append(self)

    def HandleCoroutines():
        for coroutine in Coroutine.activeCoroutines:
            if (coroutine.timeLeft <= 0):
                coroutine.runNextStep()
            if (coroutine.timeLeft is not None):
                coroutine.timeLeft -= Time.deltaTime
            
        for endedCoroutine in Coroutine.endedCoroutines:
            Coroutine.activeCoroutines.remove(endedCoroutine)
        Coroutine.endedCoroutines.clear()

class SuitI:
    def __eq__(self, other):
        return type(self) == type(other)

class Suit:
    class SPADES(SuitI):
        name = 'Spades'
        symbolCode = chr(0x2660)
        color = rgb(38, 42, 81)

    class HEARTS(SuitI):
        name = 'Hearts'
        symbolCode = chr(0x2665)
        color = rgb(222, 27, 77)

    class CLUBS(SuitI):
        name = 'Clubs'
        symbolCode = chr(0x2663)
        color = rgb(14, 70, 65)

    class DIAMONDS(SuitI):
        name = 'Diamonds'
        symbolCode = chr(0x2bc1)
        color = rgb(235, 88, 42)
    
    options = [ SPADES, HEARTS, CLUBS, DIAMONDS ]
    def GetSuitFromIndex(index):
        return Suit.options[index]


class PokerHandI:
    level = 1
    def __eq__(self, other):
        return type(self) == type(other)

class PokerHand:
    def Upgrade(hand):
        hand.chips += hand.cinc
        hand.mult += hand.minc
        hand.level += 1
        Sidebar.HandInfo.UpdateInfo(hand)

    def GetUniqueRanks(selectedCards):
        uniqueRanks = {}
        for card in selectedCards:
            if (not card.GetEffectiveRank() in uniqueRanks):
                uniqueRanks[card.GetEffectiveRank()] = [ card ]
            else:
                uniqueRanks[card.GetEffectiveRank()].append(card)
        return uniqueRanks

    def GetUniqueSuits(selectedCards):
        uniqueSuits = {}
        for card in selectedCards:
            if (not card.GetSuit() in uniqueSuits):
                uniqueSuits[card.GetSuit()] = [ card ]
            else:
                uniqueSuits[card.GetSuit()].append(card)
        return uniqueSuits
    
    
    class FLUSH_FIVE(PokerHandI):
        name = "Flush Five"
        offsetX, fontSize = 1, 10
        mult, minc, chips, cinc = 16, 3, 200, 40

        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            args = (handSize, uniqueRanks, uniqueSuits)
            if (PokerHand.FIVE_OF_A_KIND.IsPlayed(*args) and PokerHand.FLUSH.IsPlayed(*args)):
                return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            return cards
    
    class FIVE_OF_A_KIND(PokerHandI):
        name = "Five of a Kind"
        offsetX, fontSize = .25, 7.75
        mult, minc, chips, cinc = 12, 3, 120, 35

        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            if (len(uniqueRanks) == 1):
                return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            return cards

    class FLUSH_HOUSE(PokerHandI):
        name = "Flush House"
        offsetX, fontSize = 1.5, 9.5
        mult, minc, chips, cinc = 14, 3, 140, 40

        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            args = (handSize, uniqueRanks, uniqueSuits)
            if (PokerHand.FULL_HOUSE.IsPlayed(*args) and PokerHand.FLUSH.IsPlayed(*args)):
                return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            return cards

    class STRAIGHT_FLUSH(PokerHandI):
        name = "Straight Flush"
        offsetX, fontSize = 1.5, 8
        mult, minc, chips, cinc = 8, 3, 100, 40
        
        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            args = (handSize, uniqueRanks, uniqueSuits)
            if (PokerHand.STRAIGHT.IsPlayed(*args) and PokerHand.FLUSH.IsPlayed(*args)):
                return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            return cards

    class FOUR_OF_A_KIND(PokerHandI):
        name = "Four of a Kind"
        offsetX, fontSize = 0.25, 7.75
        mult, minc, chips, cinc = 7, 3, 60, 30
        
        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            if (len(uniqueRanks) > 2):
                return False
            for rank in uniqueRanks:
                if (len(uniqueRanks[rank]) == 4):
                    return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            cards = []
            for rank in uniqueRanks:
                if (len(uniqueRanks[rank]) == 4):
                    cards += uniqueRanks[rank]
                    break
            return cards


    class FULL_HOUSE(PokerHandI):
        name = "Full House"
        offsetX, fontSize = 1, 10
        mult, minc, chips, cinc = 4, 2, 40, 25
        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            if (len(uniqueRanks) == 2):
                for rank in uniqueRanks:
                    if (len(uniqueRanks[rank]) == 3):
                        return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            return cards

    class FLUSH(PokerHandI):
        name = "Flush"
        offsetX, fontSize = -8.5, 13
        mult, minc, chips, cinc = 4, 2, 35, 15
        
        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            if (len(uniqueSuits) == 1):
                return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            return cards

    class STRAIGHT(PokerHandI):
        name = "Straight"
        offsetX, fontSize = -4, 10.5
        mult, minc, chips, cinc = 4, 2, 30, 30
        
        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            if (len(uniqueRanks) != 5):
                return False
            uniqueRanks = list(uniqueRanks.keys())
            uniqueRanks.sort()
            lowestRank = uniqueRanks[0]
            passed = True
            for i in range(5):
                if (lowestRank + i != uniqueRanks[i]):
                    passed = False
                    break
            if (not passed):
                if (uniqueRanks[4] != 14): 
                    return False
                uniqueRanks.insert(0, 1)
                uniqueRanks.remove(14)
                lowestRank = uniqueRanks[0]
                for i in range(5):
                    if (lowestRank + i != uniqueRanks[i]):
                        return False
            return True
        def GetEffectiveCards(uniqueRanks, cards):
            return cards

    class THREE_OF_A_KIND(PokerHandI):
        name = "Three of a Kind"
        offsetX, fontSize = 1.7, 7.5
        mult, minc, chips, cinc = 3, 2, 30, 20

        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            for rank in uniqueRanks:
                if (len(uniqueRanks[rank]) == 3):
                    return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            cards = []
            for rank in uniqueRanks:
                if (len(uniqueRanks[rank]) == 3):
                    cards += uniqueRanks[rank]
                    break
            return cards

    class TWO_PAIR(PokerHandI):
        name = "Two Pair"
        offsetX, fontSize = -1, 11
        mult, minc, chips, cinc = 2, 1, 20, 20
        
        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            if (len(uniqueRanks) == handSize-2):
                return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            cards = []
            for rank in uniqueRanks:
                if (len(uniqueRanks[rank]) == 2):
                    cards += uniqueRanks[rank]
            return cards

    class PAIR(PokerHandI):
        name = "Pair"
        offsetX, fontSize = -12, 13
        mult, minc, chips, cinc = 2, 1, 10, 15
        
        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            if (len(uniqueRanks) == handSize-1):
                return True
            return False
        def GetEffectiveCards(uniqueRanks, cards):
            cards = []
            for rank in uniqueRanks:
                if (len(uniqueRanks[rank]) == 2):
                    cards += uniqueRanks[rank]
                    break
            return cards

    class HIGH_CARD(PokerHandI):
        name = "High Card"
        offsetX, fontSize = 0, 10.5
        mult, minc, chips, cinc = 1, 1, 5, 10
        
        def IsPlayed(handSize, uniqueRanks, uniqueSuits):
            return True
        def GetEffectiveCards(uniqueRanks, cards):
            highestRank = 0
            for rank in uniqueRanks:
                if (rank > highestRank):
                    highestRank = rank
            cards = [ uniqueRanks[highestRank][0] ]
            return cards

    class NONE(PokerHandI):
        name = ""
        offsetX = 0
        fontSize = 1
        chips = 0
        mult = 0


class BlindI:
    def __init__(self, name, reward, color, baseScoreMult):
        self.name = name
        self.desc = ""
        self.reward = reward
        self.color = color
        self.baseScoreMult = baseScoreMult

class BossBlindI:
    def __init__(self, color, darkColor, name="Boss Blind", desc="", reward=5, baseScoreMult=2):
        self.color = color
        self.darkColor = darkColor
        self.name = name
        self.desc = desc
        self.reward = reward
        self.baseScoreMult = baseScoreMult
        Blind.options.append(self)
    def __eq__(self, other):
        return (self is other) or (other is BossBlind)


class Blind:
    options = []

    Small = BlindI("Small Blind", 3, rgb(1, 107, 164), 1)
    Big = BlindI("Big Blind", 4, rgb(167, 108, 0), 1.5)

    def GetRandomBossBlind():
        return random.choice(Blind.options)

class BossBlind:
    TheClub = BossBlindI(rgb(177, 196, 132), rgb(57, 72, 58))
    TheHead = BossBlindI(rgb(161, 145, 171), rgb(49, 60, 66))
    TheGoad = BossBlindI(rgb(178, 71, 139), rgb(60, 48, 62))
    TheManacle = BossBlindI(rgb(65, 65, 65), rgb(36, 45, 45))
    TheWheel = BossBlindI(rgb(56, 181, 104), rgb(37, 71, 59))
    TheHook = BossBlindI(rgb(156, 39, 7), rgb(54, 41, 34))
    TheWall = BossBlindI(rgb(124, 68, 154), rgb(45, 46, 65))
    TheOx = BossBlindI(rgb(175, 70, 0), rgb(57, 45, 28))
    TheNeedle = BossBlindI(rgb(71, 91, 22), rgb(38, 50, 40))
    TheArm = BossBlindI(rgb(82, 81, 241), rgb(40, 48, 80))



class RarityI:
    def __init__(self, name, color, priceRange):
        self.name = name
        self.color = color
        self.priceRange = priceRange

class EventI:
    def __init__(self):
        self.activeJokers = []
    def GetSize(self):
        return len(self.activeJokers)
    def call(self, event, args):
        for joker in self.activeJokers:
            if (joker.run(joker, event, *args) == True):
                joker.visual.activateAnimation.Start()
                Audio.CARD_DESELECT.play(restart=True)
                return True
    def callSingle(self, event, index, args):
        joker = self.activeJokers[index]
        if (joker.run(joker, event, *args) == True):
            joker.visual.activateAnimation.Start()
            Audio.CARD_DESELECT.play(restart=True)
            return True

class Joker:
    activeJokerVisuals = []
    
    jokerAnimations = []
    disabledJokerAnimations = []
    
    def HandleAnimations():
        for disabledAnimation in Joker.disabledJokerAnimations:
            if (disabledAnimation in Joker.jokerAnimations):
                Joker.jokerAnimations.remove(disabledAnimation)
        Joker.disabledJokerAnimations.clear()
        for animation in Joker.jokerAnimations:
            animation()


    def __init__(self, name, desc, rarity, events, runFunc, activeJokerList):
        self.name = name
        self.desc = desc
        self.rarity = rarity
        if (type(events) is not list): events = [events]
        self.events = events
        self.visual = type(self).Visual(self)
        self.run = runFunc
        activeJokerList.append(self)
        self.price = random.choice(self.rarity.priceRange)
        self.sellValue = int(self.price/2)
        self.isActive = False

    def activate(self, silent=False):
        for event in self.events:
            Event.assign(event, self)
        if (not silent):
            self.isActive = True
    def deactivate(self):
        for event in self.events:
            Event.unassign(event, self)
        self.isActive = False
    def __repr__(self):
        return f"'{self.name}'"
        
    def IsActive(self):
        return self.isActive



    @staticmethod
    def HandleHovers(mx, my):
        for jokerVisual in Joker.activeJokerVisuals:
            if (not jokerVisual.isHovered and jokerVisual.group.hits(mx, my)):
                jokerVisual.OnHovered(audio=True)
            elif (jokerVisual.isHovered and not jokerVisual.group.hits(mx, my)):
                jokerVisual.OnUnhovered()


    class Visual:
        def __init__(self, joker):
            self.joker = joker
            self.group = None
            self.infoBox = None
            self.isHovered = False
            self.UpdateDescription()
            self.activateAnimation = None
            self.moveAnimation = None

        def IsActive(self):
            return self.group != None

        def UpdateDescription(self):
            self.description = self.GenerateDescription(self.joker.desc)

        def GenerateDescription(self, rawDesc):
            description = []
            while True:
                if ('\n' in rawDesc):
                    index = rawDesc.index('\n')
                    description.append(rawDesc[:index])
                    rawDesc = rawDesc[index+1:]
                else:
                    description.append(rawDesc)
                    break
            return description



        def CreateVisual(self, posX, posY):
            self.group = Group(Rect(-Card.width/2, -Card.height/2, Card.width, Card.height, fill=self.joker.rarity.color, border='white'),Label("JOKER", 0, -Card.height/8, font=app.font, size=8, fill=self.joker.rarity.color.darker().darker().darker(), bold=True),Label(self.joker.name, 0, Card.height/2-8, font=app.font, size=4, fill=self.joker.rarity.color.darker().darker().darker(), bold=True))
            self.group.centerX, self.group.centerY = posX, posY
            if self.activateAnimation==None:
                self.activateAnimation = Joker.Visual.ActivateAnimation(self)
            self.activateAnimation.SetGroup(self.group)
            if self.moveAnimation==None:
                self.moveAnimation = Effects.MoveAnimation(Joker.jokerAnimations, Joker.disabledJokerAnimations)
            self.moveAnimation.SetGroup(self.group)
            if (not self in Joker.activeJokerVisuals): 
                Joker.activeJokerVisuals.append(self)

        def DeleteVisual(self):
            if (self.infoBox is not None): self.DeleteInfoBox()
            if (self.group is not None): self.group.visible = False
            self.group = None
            self.activateAnimation.SetGroup(None)
            self.moveAnimation.SetGroup(None)
            if (self in Joker.activeJokerVisuals):
                Joker.activeJokerVisuals.remove(self)

        def MoveVisual(self, posX=None, posY=None, animate=False, timeToMove=app.gameSpeed):
            if posX==None: posX = self.group.centerX
            if posY==None: posY = self.group.centerY
            if (animate): self.moveAnimation.Start(posX, posY, timeToMove)
            else: self.group.centerX, self.group.centerY = posX, posY

        def IsHovered(self):
            return self.isHovered

        def OnHovered(self, audio=False):
            if (self.activateAnimation.isActive):
                return
            self.isHovered = True
            self.Resize(Card.width*1.1, Card.height*1.1)
            self.DrawInfoBox()
            if (audio): random.choice([ Audio.CARD_HOVER_1, Audio.CARD_HOVER_2, Audio.CARD_HOVER_3 ]).play(restart=True)

        def OnUnhovered(self):
            self.isHovered = False
            self.Resize(Card.width, Card.height)
            self.DeleteInfoBox()

        def Resize(self, width, height, includeText=True):
            oldX, oldY = self.group.centerX, self.group.centerY
            if (includeText):
                self.group.children[1].centerY += (self.group.children[0].height - height)/4
                self.group.children[2].centerY -= (self.group.children[0].height - height)/4
            self.group.children[0].width = width
            self.group.children[0].height = height
            self.group.children[0].centerX, self.group.children[0].centerY = oldX, oldY
            self.group.centerX, self.group.centerY = oldX, oldY

        def DrawInfoBox(self):
            if (not self.IsActive):
                return
            self.infoBox = Group(Rect(0,1.5, 60, 56, border=rgb(245,245,245).darker().darker()),Rect(0,0, 60, 56, border=rgb(245,245,245)),Rect(1.5,1.5, 57, 53, fill=rgb(43, 57, 58)),Rect(4,12.25, 52, 22, fill=rgb(255,255,255).darker().darker()),Rect(4,11, 52, 22, fill=rgb(255,255,255)),Rect(12,37.75, 36, 8, fill=self.joker.rarity.color.darker().darker().darker()),Rect(12,36.5, 36, 8, fill=self.joker.rarity.color),Label(self.joker.name, 30, 6, font=app.font, size=6.5, fill='white', bold=True),Label(self.joker.rarity.name, 30, 40.5, font=app.font, size=5.25, fill='white', bold=True),)
            if (self.joker.IsActive() and (Game.state is GameState.SHOPPING or self.joker is Game.jokersDeck.jokersList[len(Game.jokersDeck.jokersList)-1])):
                self.infoBox.add(Label(f"(Click to sell ${self.joker.sellValue})", 30, 49.25, font=app.font, size=4.5, fill=rgb(255,255,255).darker()))
            elif (not self.joker.IsActive() and Game.state is GameState.SHOPPING):
                self.infoBox.add(Label(f"(Click to buy ${self.joker.price})", 30, 49.25, font=app.font, size=4.5, fill=rgb(255,255,255).darker()))
            else:
                self.infoBox.add(Label("(Click to move)", 30, 49.25, font=app.font, size=4.5, fill=rgb(255,255,255).darker()))
            for i, line in enumerate(self.description):
                self.infoBox.add( Label(line, 30, 14.5 + i*5, font=app.font, size=4.5, fill=rgb(43, 57, 58), bold=True) )
            self.infoBox.centerX = self.group.centerX
            self.infoBox.top = self.group.bottom + 3

        def DeleteInfoBox(self):
            if (self.infoBox is None):
                return
            self.infoBox.visible = False
            self.infoBox = None

        class ActivateAnimation:
            def __init__(self, visual):
                self.visual = visual
                self.group = None
                self.isActive = False

            def SetGroup(self, group):
                self.group = group
                if group is None:
                    self.Stop(forceStop=True)

            def Start(self):
                if (self.group is None):
                    return
                self.visual.OnUnhovered()
                self.isActive = True
                self.endWidth = self.group.width
                self.endHeight = self.group.height
                self.startWidth = self.endWidth * 1.3
                self.startHeight = self.endHeight * 1.3
                self.maxRot = 10
                self.animSpeed = 3 / app.gameSpeed
                self.animPosition = 0
                if (not self.Step in Joker.jokerAnimations):
                    Joker.jokerAnimations.append(self.Step)

            def Stop(self, forceStop=False):
                self.isActive = False
                if (forceStop and self.Step in Joker.jokerAnimations):
                    Joker.jokerAnimations.remove(self.Step)
                    return
                if (not self.Step in Joker.disabledJokerAnimations):
                    Joker.disabledJokerAnimations.append(self.Step)

            def Step(self):
                if (self.group is None):
                    return
                t = self.animPosition
                if (t == 1):
                    self.Stop()
                    self.visual.Resize(self.endWidth, self.endHeight)
                    self.group.rotateAngle = 0
                    return
                animPos = math.sin((math.pi * t) / 2)
                width = (1 - animPos) * self.startWidth + animPos * self.endWidth
                height = (1 - animPos) * self.startHeight + animPos * self.endHeight
                if (t < 0.3333):
                    animPos = math.sin(3*math.pi * t)
                elif (t < 0.52):
                    animPos = -0.5*math.sin(4*math.pi * t + 2.09419)
                else:
                    animPos = 0.318*(2*(t - 1.039807))**3
                rot = animPos * self.maxRot
                self.animPosition = max(0, min(1, t + self.animSpeed * Time.deltaTime))
                self.visual.Resize(width, height, includeText=False)
                self.group.rotateAngle = -rot


class Rarity:
    COMMON = RarityI("Common", rgb(7, 145, 254), [2,2, 3,3,3,3, 4,4, 5])
    UNCOMMON = RarityI("Uncommon", rgb(63, 183, 129), [5,5,5,5, 6,6,6, 7])
    RARE = RarityI("Rare", rgb(253, 69, 61), [6, 7,7,7,7, 8,8,8, 9,9])

class Event:
    ON_HAND_PLAY = EventI()
    ON_HAND_END = EventI()
    ON_CARD_SCORED = EventI()
    ON_ROUND_START = EventI()
    ON_ROUND_END = EventI()
    ON_DISCARD = EventI()
    ON_JOKER_DECK_CHANGED = EventI()

    def Call(event, args=(None,)):
        event.call(event, args)
    def CallSingle(event, index, args=(None,)):
        return event.callSingle(event, index, args)

    def assign(event, joker):
        if (joker not in event.activeJokers):
            event.activeJokers.append(joker)
    def unassign(event, joker):
        if (joker in event.activeJokers):
            event.activeJokers.remove(joker)


class JManager:
    availableJokers = {Rarity.COMMON: [], Rarity.UNCOMMON: [], Rarity.RARE: []}

    def GetJokersOfRarity(rarity):
        return JManager.availableJokers[rarity]

    def New(name, desc, rarity, events, runFunc):
        availableJokersList = JManager.availableJokers[rarity]
        return Joker(name, desc, rarity, events, runFunc, availableJokersList)

    def Activate(joker, silent=False):
        JManager.availableJokers[joker.rarity].remove(joker)
        if (not silent):
            joker.activate(silent=silent)
            Event.Call(Event.ON_JOKER_DECK_CHANGED)
    def Deactivate(joker, silent=False):
        JManager.availableJokers[joker.rarity].append(joker)
        if (not silent):
            joker.deactivate()
            Event.Call(Event.ON_JOKER_DECK_CHANGED)

    # Joker Helper Functions
    def AddChips(chips, origin, dir):
        scoreCycle = Game.PlayHand_CR.Instance
        scoreCycle.chips += chips
        RoundInfo.Update(chips=scoreCycle.chips)
        Effects.AddChipsEffect(chips, origin.centerX, origin.centerY + (origin.height/2 * dir) + (15 * dir), dir)
    def AddMult(mult, origin, dir):
        scoreCycle = Game.PlayHand_CR.Instance
        scoreCycle.mult += mult
        RoundInfo.Update(mult=scoreCycle.mult)
        Effects.AddMultEffect(mult, origin.centerX, origin.centerY + (origin.height/2 * dir) + (15 * dir), dir)
    def TimesMult(factor, origin, dir):
        scoreCycle = Game.PlayHand_CR.Instance
        scoreCycle.mult *= factor
        RoundInfo.Update(mult=scoreCycle.mult)
        Effects.TimesMultEffect(factor, origin.centerX, origin.centerY + (origin.height/2 * dir) + (15 * dir), dir)
    def CustomPopup(text, origin, dir, color, startSize, textSize):
        Effects.InfoPopup(text, origin.centerX, origin.centerY + (origin.height/2 * dir) + (10 * dir), dir, color, startSize, textSize)

class JokerType:
    def run(self, event, a, selectedCards, c):
        if (len(selectedCards) <= 3):
            JManager.AddMult(20, self.visual.group, 1)
            return True
    HalfJoker = JManager.New(
        "Half Joker",
        "+20 Mult if played\nhand contains 3\nor fewer cards",
        Rarity.COMMON,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, a, b=0, c=0):
        self.multMultiplier = Game.jokersDeck.maxJokers - (Game.jokersDeck.GetSize()-1)
        if (event is Event.ON_HAND_END):
            JManager.TimesMult(self.multMultiplier, self.visual.group, 1)
            return True
        elif (event is Event.ON_JOKER_DECK_CHANGED):
            self.desc = f"X1 Mult for each\nempty Joker slot,\nthis Joker's included\n(Currently X{self.multMultiplier})"
            self.visual.UpdateDescription()
    JokerStencil = JManager.New(
        "Joker Stencil",
        "",
        Rarity.UNCOMMON,
        [Event.ON_HAND_END, Event.ON_JOKER_DECK_CHANGED],
        run
        )

    def run(self, event, a, b, c):
        if (Game.activeHand.GetSize() != 0):
            lowestRank = min(card.GetChips() for card in Game.activeHand.GetCardList())
            JManager.AddMult(lowestRank * 2, self.visual.group, 1)
            return True
    RaisedFist = JManager.New(
        "Raised Fist",
        "Adds double the\nrank of lowest card\nheld in hand to Mult",
        Rarity.COMMON,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, card):
        if (card.GetEffectiveRank() in [2,3,5,8,14]):
            JManager.AddMult(8, card.visual.group, -1)
            return True
    Fibonacci = JManager.New(
        "Fibonacci",
        "Each played\nAce, 2, 3, 5, or 8\ngives +8 Mult\nwhen scored",
        Rarity.UNCOMMON,
        Event.ON_CARD_SCORED,
        run
        )

    def run(self, event, a, b, c):
        foundKing = False
        for card in Game.activeHand.GetCardList():
            if (card.GetRank() == 13):
                foundKing = True
                JManager.TimesMult(1.5, card.visual.group, -1)
        return foundKing
    Baron = JManager.New(
        "Baron",
        "Each King held\nin hand gives\nX1.5 Mult",
        Rarity.RARE,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, card):
        if (card.GetRank() in [11,12,13]):
            JManager.AddChips(30, card.visual.group, -1)
            return True
    ScaryFace = JManager.New(
        "Scary Face",
        "Played face cards\ngive +30 Chips\nwhen scored",
        Rarity.COMMON,
        Event.ON_CARD_SCORED,
        run
        )

    def run(self, event, card):
        if (card.GetRank() in [11,12,13]):
            JManager.AddMult(4, card.visual.group, -1)
            return True
    SmileyFace = JManager.New(
        "Smiley Face",
        "Played face cards\ngive +4 Mult\nwhen scored",
        Rarity.COMMON,
        Event.ON_CARD_SCORED,
        run
        )

    def run(self, event, a, b, c):
        self.multMultiplier = 3 * Game.jokersDeck.GetSize()
        JManager.AddMult(self.multMultiplier, self.visual.group, 1)
        return True
    AbstractJoker = JManager.New(
        "Abstract Joker",
        "+3 Mult for each\nactive Joker card",
        Rarity.COMMON,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, a):
        self.sellValue += 3
        JManager.CustomPopup("+$3", self.visual.group, 1, rgb(252, 181, 67), 6.5, 8)
        return True
    EternalEgg = JManager.New(
        "Eternal Egg",
        "Gains $3 of sell value\nat end of round\n(never resets)",
        Rarity.COMMON,
        Event.ON_ROUND_END,
        run
        )

    def run(self, event, a=0, b=0, c=0):
        chips = 2 * Game.roundDeck.GetSize()
        if (event is Event.ON_HAND_END):
            JManager.AddChips(chips, self.visual.group, 1)
        self.desc = f"+2 Chips for each\nremaining card\nin deck\n(Currently +{chips})"
        self.visual.UpdateDescription()
        return True
    BlueJoker = JManager.New(
        "Blue Joker",
        "+2 Chips for each\nremaining card\nin deck\n(Currently +104)",
        Rarity.COMMON,
        [Event.ON_HAND_END, Event.ON_ROUND_END, Event.ON_HAND_PLAY],
        run
        )

    def run(self, event, a, b, c):
        chips = 2 * Game.money
        JManager.AddChips(chips, self.visual.group, 1)
        return True
    Bull = JManager.New(
        "Bull",
        "+2 Chips for each\ndollar you have",
        Rarity.UNCOMMON,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, a, b, c):
        if (Game.hands == 0):
            JManager.TimesMult(3, self.visual.group, 1)
            return True
    Acrobat = JManager.New(
        "Acrobat",
        "X3 Mult on final\nhand of round",
        Rarity.UNCOMMON,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, card):
        if (event is Event.ON_ROUND_END):
            self.suit = Suit.GetSuitFromIndex(random.randint(0,3))
            self.desc = f"Played {self.suit.name} suit\ncards give X1.5\nMult, suit changes\nend of round"
            self.visual.UpdateDescription()
            return True
        if (event is Event.ON_CARD_SCORED):
            if (card.GetSuit() == self.suit):
                JManager.TimesMult(1.5, card.visual.group, -1)
                return True
    AncientJoker = JManager.New(
        "Ancient Joker",
        "",
        Rarity.RARE,
        [Event.ON_CARD_SCORED, Event.ON_ROUND_END],
        run
        )
    run(AncientJoker, Event.ON_ROUND_END, None)

    def run(self, event, a):
        money = int(Game.money/7)
        Game.money += money
        JManager.CustomPopup(f"+${money}", self.visual.group, 1, rgb(252, 181, 67), 6.5, 8)
        return money != 0
    ToTheMoon = JManager.New(
        "To the Moon",
        "Earn $1 of interest\nfor every $7 you\nhave at end of round",
        Rarity.UNCOMMON,
        Event.ON_ROUND_END,
        run
        )

    def run(self, event, a, b, c):
        mult = 2 * int(Game.money/5)
        JManager.AddMult(mult, self.visual.group, 1)
        return True
    Bootstraps = JManager.New(
        "Bootstraps",
        "+2 Mult for every\n$5 you have",
        Rarity.UNCOMMON,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, pokerHand, b, c):
        if (random.randint(0, 2) == 0):
            PokerHand.Upgrade(pokerHand)
            JManager.CustomPopup("+1 lvl.", self.visual.group, 1, rgb(255, 153, 0), 6, 7)
            return True
    SpaceJoker = JManager.New(
        "Space Joker",
        "1 in 3 chance to\nupgrade level of\nplayed poker hand",
        Rarity.RARE,
        Event.ON_HAND_PLAY,
        run
        )

    def run(self, event, pokerHand, a):
        if (Game.discards == Game.maxDiscards):
            PokerHand.Upgrade(pokerHand)
            JManager.CustomPopup("+1 lvl.", self.visual.group, 1, rgb(255, 153, 0), 6, 7)
            return True
    BurntJoker = JManager.New(
        "Burnt Joker",
        "Upgrade the level of\nthe first discarded\npoker hand each\nround",
        Rarity.UNCOMMON,
        Event.ON_DISCARD,
        run
        )

    def run(self, event, a):
        ran = False
        for _ in range(min(2, Game.jokersDeck.maxJokers-Game.jokersDeck.GetSize())):
            Game.jokersDeck.AddJoker(random.choice(JManager.GetJokersOfRarity(Rarity.COMMON)))
            ran = True
        Game.jokersDeck.DisplayJokers()
        return ran
    RiffRaff = JManager.New(
    "Riff-Raff",
    "When new round\nstarts, create 2\nCommon Jokers\n(Must have room)",
    Rarity.COMMON,
    Event.ON_ROUND_START,
    run
    )

    def run(self, event, a, selectedCards):
        if (Game.discards == Game.maxDiscards and len(selectedCards) == 1):
            card = selectedCards[0]
            Game.fullDeck.RemoveCard(card)
            Game.money += 3
            JManager.CustomPopup("+$3", self.visual.group, 1, rgb(252, 181, 67), 6.5, 8)
            RoundInfo.Update(money=Game.money)
            return True
    TradingCard = JManager.New(
        "Trading Card",
        "If first discard of\nround has only 1\ncard, destroy it\nforever and earn $3",
        Rarity.UNCOMMON,
        Event.ON_DISCARD,
        run
        )

    def run(self, event, a, selectedCards, c):
        if (Game.hands == Game.maxHands-1 and len(selectedCards) == 1):
            card = selectedCards[0]
            newCard = Card(card.rank, card.suit)
            Game.fullDeck.AddCard(newCard)
            Game.activeHand.AddCard(newCard)
            Game.activeHand.DisplayCards()
            JManager.CustomPopup("+1 Card", self.visual.group, 1, rgb(63, 183, 129), 8.5, 6)
            return True
    DNA = JManager.New(
        "DNA",
        "If first hand has\nonly 1 card, create a\ncopy in deck and\ndraw it to hand",
        Rarity.RARE,
        Event.ON_HAND_PLAY,
        run
        )

    def run(self, event, a, selectedCards, c):
        if (event is Event.ON_HAND_PLAY):
            if (len(selectedCards) == 4):
                self.chips += 4
                JManager.CustomPopup(f"+{self.chips}", self.visual.group, 1, rgb(255, 153, 0), 9, 8.5)
                self.desc = f"Gains +4 Chips if\nplayed hand has\nexactly 4 cards\n(Currently +{self.chips})"
                self.visual.UpdateDescription()
                return True
        else:
            JManager.AddChips(self.chips, self.visual.group, 1)
            return True
    SquareJoker = JManager.New(
        "Square Joker",
        "Gains +4 Chips if\nplayed hand has\nexactly 4 cards\n(Currently +16)",
        Rarity.COMMON,
        [Event.ON_HAND_PLAY, Event.ON_HAND_END],
        run
        )
    SquareJoker.chips = 16
    
    def run(self, event, hand, b, c):
        if (event is Event.ON_HAND_PLAY):
            if (hand is PokerHand.STRAIGHT or hand is PokerHand.STRAIGHT_FLUSH):
                self.chips += 10
                JManager.CustomPopup(f"+{self.chips}", self.visual.group, 1, rgb(255, 153, 0), 9, 8.5)
                self.desc = f"Gains +10 Chips\nif played hand\ncontains a Straight\n(Currently +{self.chips})"
                self.visual.UpdateDescription()
                return True
        else:
            JManager.AddChips(self.chips, self.visual.group, 1)
            return True
    Runner = JManager.New(
        "Runner",
        "Gains +10 Chips\nif played hand\ncontains a Straight\n(Currently +20)",
        Rarity.COMMON,
        [Event.ON_HAND_PLAY, Event.ON_HAND_END],
        run
        )
    Runner.chips = 20

    def run(self, event, hand, b, c):
        if (event is Event.ON_HAND_PLAY):
            if (hand is PokerHand.TWO_PAIR or hand is PokerHand.FULL_HOUSE or hand is PokerHand.FLUSH_HOUSE):
                self.mult += 2
                JManager.CustomPopup(f"+{self.mult}", self.visual.group, 1, rgb(255, 153, 0), 9, 8.5)
                self.desc = f"Gains +2 Mult\nif played hand\ncontains a Two Pair\n(Currently +{self.mult})"
                self.visual.UpdateDescription()
                return True
        else:
            JManager.AddMult(self.mult, self.visual.group, 1)
            return True
    SpareTrousers = JManager.New(
        "Spare Trousers",
        "Gains +2 Mult\nif played hand\ncontains a Two Pair\n(Currently +4)",
        Rarity.UNCOMMON,
        [Event.ON_HAND_PLAY, Event.ON_HAND_END],
        run
        )
    SpareTrousers.mult = 4

    def run(self, event, hand, cards, c):
        if (hand is PokerHand.STRAIGHT):
            suit = cards[0].GetSuit()
            for card in cards:
                card.suit = suit
                oldX, oldY = card.visual.group.centerX, card.visual.group.centerY
                card.visual.DeleteVisual()
                card.visual.CreateVisual(card.rank, card.suit, oldX, oldY)
            JManager.CustomPopup(f"{random.choice(['Boom!','Bang!','Pow!'])}", self.visual.group, 1, rgb(63, 183, 129), 11, 6)
            return True
    Uniform = JManager.New(
        "Uniform",
        "If played hand\nis a Straight, convert\nentire hand into\nthe leftmost suit",
        Rarity.RARE,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, a, cards=0, c=0):
        def updatedesc():
            self.desc = f"Gains +3 Chips per\n{self.suit.name} discard, suit\nchanges each round\n(Currently +{self.chips})"
            self.visual.UpdateDescription()
        if (event is Event.ON_ROUND_END):
            self.suit = Suit.GetSuitFromIndex(random.randint(0,3))
            updatedesc()
            return True
        elif (event is Event.ON_DISCARD):
            matched = False
            for card in cards:
                if (card.GetSuit() is self.suit):
                    self.chips += 3
                    matched = True
            if (matched):
                JManager.CustomPopup(f"+{self.chips}", self.visual.group, 1, rgb(255, 153, 0), 9, 8.5)
                updatedesc()
                return True
        else:
            JManager.AddChips(self.chips, self.visual.group, 1)
            return True
    Castle = JManager.New(
        "Castle",
        "",
        Rarity.UNCOMMON,
        [Event.ON_ROUND_END, Event.ON_DISCARD, Event.ON_HAND_END],
        run
        )
    Castle.chips = 0
    run(Castle, Event.ON_ROUND_END, 0,0,0)

    def run(self, event, a, cards=0, c=0):
        def updatedesc():
            self.desc = f"Gains X0.5 Mult\nper discarded Jack\nthis round\n(Currently X{self.timesMult})"
            self.visual.UpdateDescription()
        if (event is Event.ON_ROUND_END):
            self.timesMult = 1.0
            updatedesc()
            return True
        elif (event is Event.ON_DISCARD):
            matched = False
            for card in cards:
                if (card.GetRank() == 11):
                    self.timesMult += 0.5
                    matched = True
            if (matched):
                JManager.CustomPopup(f"X{self.timesMult}", self.visual.group, 1, rgb(255, 153, 0), 9, 8.5)
                updatedesc()
                return True
        else:
            JManager.TimesMult(self.timesMult, self.visual.group, 1)
            return True
    HitTheRoad = JManager.New(
        "Hit the Road",
        "",
        Rarity.RARE,
        [Event.ON_HAND_END, Event.ON_DISCARD, Event.ON_ROUND_END],
        run
        )
    run(HitTheRoad, Event.ON_ROUND_END, 0,0,0)

    def run(self, event, a,b,c):
        matched = False
        for card in Game.activeHand.GetAllCards():
            if (card.GetRank() == 12):
                JManager.AddMult(13, card.visual.group, -1)
                matched = True
        if (matched):
            return True
    ShootTheMoon = JManager.New(
        "Shoot the Moon",
        "+13 Mult for\neach Queen\nheld in hand",
        Rarity.COMMON,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, card, b=0,c=0):
        if (event is Event.ON_HAND_END):
            self.hasRun = False
        else:
            if (not self.hasRun and card.GetRank() in [11, 12, 13]):
                self.hasRun = True
                JManager.TimesMult(2, card.visual.group, -1)
                return True
    Photograph = JManager.New(
        "Photograph",
        "First played face\ncard gives X2 Mult\nwhen scored",
        Rarity.COMMON,
        [Event.ON_CARD_SCORED, Event.ON_HAND_END],
        run
        )
    Photograph.hasRun = False

    def run(self, event, a,b,c):
        JManager.AddMult(random.randint(0,23), self.visual.group, 1)
        return True
    Misprint = JManager.New(
        "Misprint",
        "Randomly adds\n0 to 23 Mult",
        Rarity.COMMON,
        Event.ON_HAND_END,
        run
        )
    
    def run(self, event, a,b,c):
        chips = 40 * Game.discards
        JManager.AddChips(chips, self.visual.group, 1)
        return True
    Banner = JManager.New(
        "Banner",
        "+40 Chips for\neach remaining\ndiscard",
        Rarity.COMMON,
        Event.ON_HAND_END,
        run
        )

    def run(self, event, a,b,c):
        JManager.AddMult(4, self.visual.group, 1)
        return True
    BasicJoker = JManager.New(
        "Joker",
        "+4 Mult",
        Rarity.COMMON,
        Event.ON_HAND_END,
        run
        )
        
    def run(self, event, a,b,c):
        if (Game.discards == 0):
            JManager.AddMult(15, self.visual.group, 1)
            return True
    MysticSummit = JManager.New(
        "Mystic Summit",
        "+15 Mult when\n0 discards\nremaining",
        Rarity.COMMON,
        Event.ON_HAND_END,
        run
        )


    




class Card:
    width = 40
    height = 56
    cardAnimations = []
    disabledCardAnimations = []

    def HandleAnimations():
        for disabledAnimation in Card.disabledCardAnimations:
            if (disabledAnimation in Card.cardAnimations):
                Card.cardAnimations.remove(disabledAnimation)
        Card.disabledCardAnimations.clear()
        for animation in Card.cardAnimations:
            animation()

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.visual = Card.Visual()

    def GetRank(self):
        return self.rank

    def GetEffectiveRank(self):
        rank = self.rank
        if (rank == 1): rank = 14
        return rank

    def GetSuit(self):
        return self.suit

    def GetReadableRank(rank):
        match rank:
            case 1: return 'A'
            case 11: return 'J'
            case 12: return 'Q'
            case 13: return 'K'
        return str(rank)

    def GetChips(self):
        chips = min(10, self.GetRank())
        if (chips == 1): chips = 11
        return chips


    def __repr__(self):
        return f"{Card.GetReadableRank(self.rank)} of {self.suit.name}"


    class Visual:
        def __init__(self):
            self.group = None
            self.active = False
            self.idleAnimation = Card.Visual.IdleAnimation()
            self.moveAnimation = Effects.MoveAnimation(Card.cardAnimations, Card.disabledCardAnimations)
            self.isHovered = False

        def CreateVisual(self, rank, suit, posX=None, posY=None):
            visualRank = Card.GetReadableRank(rank)
            color = suit.color
            self.group = Group (
                Rect(0,0, Card.width, Card.height, fill='white', border='gray', borderWidth=0.4),
                Label(visualRank, 7, 7, font=app.font, size=10.5, fill=color, bold=True),
                Label(suit.symbolCode, 7, 16.5, font='symbols', size=8.5, fill=color),
                Label(visualRank, Card.width-7, Card.height-7, font=app.font, size=10.5, fill=color, bold=True, rotateAngle=180),
                Label(suit.symbolCode, Card.width-7, Card.height-16.5, font='symbols', size=8.5, fill=color, rotateAngle=180),
            )
            if posX!=None:
                self.group.centerX = posX
            if posY!=None:
                self.group.centerY = posY
            self.active = True
            self.idleAnimation.SetGroup(self.group)
            self.idleAnimation.Start()
            self.moveAnimation.SetGroup(self.group)


        def MoveVisual(self, inputX=None, inputY=None, animate=False, timeToMove=app.gameSpeed):
            posX, posY = self.group.centerX, self.group.centerY
            if inputX!=None: posX = inputX
            if inputY!=None: posY = inputY 
            if (animate): 
                self.moveAnimation.Start(posX, posY, timeToMove)
            else:
                self.group.centerX = posX
                self.group.centerY = posY

        def DeleteVisual(self):
            self.idleAnimation.SetGroup(None)
            self.moveAnimation.SetGroup(None)
            self.group.visible = False
            self.group = None
            self.active = False
            self.isHovered = False

        def IsActive(self):
            return self.active

        def IsHovered(self):
            return self.isHovered

        def IsTouchingMouse(self, mx, my):
            return self.group.hits(mx, my)

        def Select(self, audio=False):
            self.unselectedPosY = self.group.centerY
            self.MoveVisual(self.group.centerX, self.unselectedPosY-12)
            if (audio): Audio.CARD_SELECT.play(restart=True)

        def Deselect(self, audio=False):
            self.MoveVisual(self.group.centerX, self.unselectedPosY)
            if (audio): Audio.CARD_DESELECT.play(restart=True)

        def Hover(self, audio=False):
            self.isHovered = True
            self.Resize(Card.width*1.1, Card.height*1.1)
            if (audio): random.choice([ Audio.CARD_HOVER_1, Audio.CARD_HOVER_2, Audio.CARD_HOVER_3 ]).play(restart=True)
            
        def Unhover(self):
            self.isHovered = False
            self.Resize(Card.width, Card.height)
        
        def Resize(self, width, height):
            oldCenterX, oldCenterY = self.group.centerX, self.group.centerY
            oldRotateAngle = self.group.rotateAngle
            self.group.rotateAngle = 0
            widthRatio = width/self.group.width
            heightRatio = height/self.group.height
            cardBg = self.group.children[0]

            labels = []
            for i in range(1, 5):
                labels.append(self.group.children[i])
            offsetX = labels[0].centerX - cardBg.left
            numberOffsetY = labels[0].centerY - cardBg.top
            symbolOffsetY = labels[1].centerY - cardBg.top

            cardBg.width, cardBg.height = width, height
            for label in labels:
                label.size *= widthRatio
            labels[0].centerX = cardBg.left + offsetX * widthRatio
            labels[0].centerY = cardBg.top + numberOffsetY * heightRatio
            labels[2].centerX = cardBg.right - offsetX * widthRatio
            labels[2].centerY = cardBg.bottom - numberOffsetY * heightRatio

            labels[1].centerX = cardBg.left + offsetX * widthRatio
            labels[1].centerY = cardBg.top + symbolOffsetY * heightRatio
            labels[3].centerX = cardBg.right - offsetX * widthRatio
            labels[3].centerY = cardBg.bottom - symbolOffsetY * heightRatio

            self.group.centerX, self.group.centerY = oldCenterX, oldCenterY
            self.group.rotateAngle = oldRotateAngle

        class IdleAnimation:
            def __init__(self):
                self.minAngle = -3.5
                self.maxAngle = 3.5
                self.baseSpeed = 0.4
                self.minSpeed = self.baseSpeed - (self.baseSpeed/8)
                self.maxSpeed = self.baseSpeed + (self.baseSpeed/4)
                self.animSpeed = random.uniform(self.minSpeed, self.maxSpeed)
                self.animPosition = random.uniform(0, 1)
                self.rotateDir = 1 if (bool(random.getrandbits(1))) else -1

            def IsActive(self):
                return self.Step in Card.activeAnimations

            def SetGroup(self, group):
                self.cardGroup = group
                if group is None:
                    self.Stop(forceStop=True)

            def Start(self):
                self.initialRotateDir = self.cardGroup.rotateAngle
                self.animSpeed = random.uniform(self.minSpeed, self.maxSpeed)
                self.animPosition = random.uniform(0, 1)
                self.rotateDir = 1 if (bool(random.getrandbits(1))) else -1
                if (not self.Step in Card.cardAnimations):
                    Card.cardAnimations.append(self.Step)

            def Stop(self, forceStop=False):
                if (forceStop and self.Step in Card.cardAnimations):
                    Card.cardAnimations.remove(self.Step)
                    return
                else:
                    Card.disabledCardAnimations.append(self.Step)
                if (self.cardGroup is not None):
                    self.cardGroup.rotateAngle = self.initialRotateDir

            def Step(self):
                if (self.cardGroup is None): return
                t = self.animPosition
                animPos = (-math.cos(math.pi * t)+1) / 2
                angle = (1 - animPos) * self.minAngle + animPos * self.maxAngle 
                self.animPosition = max(0, min(1, t + self.animSpeed * self.rotateDir * Time.deltaTime))
                if (t == 1):
                    self.rotateDir = -1
                elif (t == 0):
                    self.rotateDir = 1
                self.cardGroup.rotateAngle = angle
        
class Deck:
    def __init__(self): self.cardList = []

    def GetSize(self): return len(self.cardList)

    def GetCardList(self): return self.cardList

    def GetAllCards(self): return self.cardList.copy()
        
    def AddCard(self, card): self.cardList.append(card)

    def GetCard(self, index):
        index = max(0, min(self.GetSize()-1, index))
        return self.cardList[index]

    def RemoveCard(self, card):
        if (card in self.cardList):
            self.cardList.remove(card)

    def SetCard(self, card, index):
        index = max(0, min(self.GetSize()-1, index))
        self.cardList[index] = card

class FullDeck(Deck):
    def __init__(self):
        super().__init__()
        for suitIndex in range(4):
            for rank in range(1, 14):
                card = Card(rank, Suit.GetSuitFromIndex(suitIndex))
                self.cardList.append(card)

class EffectiveDeck(Deck):
    def __init__(self, fullDeck):
        super().__init__()
        self.fullDeck = fullDeck
        self.cardList = fullDeck.GetAllCards()

class Hand(Deck):
    def __init__(self, maxCards, sourceDeck, startingHand=[]):
        super().__init__()
        self.maxCards = maxCards
        self.sourceDeck = sourceDeck
        for card in startingHand:
            self.AddCard(card)
        self.sortMode = 'rank'
        self.FillHand(self.sourceDeck)
        self.selectedCards = []
        self.canSelectCards = True

    def FillHand(self, sourceDeck):
        neededCards = self.maxCards - self.GetSize()
        while (neededCards > 0):
            if (sourceDeck.GetSize() == 0):
                break
            card = sourceDeck.cardList[random.randint(0, sourceDeck.GetSize()-1)]
            self.AddCard(card)
            sourceDeck.RemoveCard(card)
            neededCards -= 1
        self.DisplayCards()

    def SortHand(self, mode):
        originalHand = self.GetAllCards()
        def CardIsHigherRank(card, bestCard):
            return card.GetEffectiveRank() > bestCard.GetEffectiveRank()
        def CardIsSameRank(card, bestCard):
            return card.GetEffectiveRank() == bestCard.GetEffectiveRank()
        def CardIsHigherSuit(card, bestCard):
            suitIndex = 0
            highSuitIndex = 0
            for index in range(len(Suit.options)):
                if (card.GetSuit() == Suit.options[index]):
                    suitIndex = index
                if (bestCard.GetSuit() == Suit.options[index]):
                    highSuitIndex = index
            if (suitIndex < highSuitIndex):
                return True
            return False
        def CardIsSameSuit(card, bestCard):
            return card.GetSuit() == bestCard.GetSuit()

        for i in range(self.GetSize()):
            bestCard = None
            for card in originalHand:
                if (bestCard == None):
                    bestCard = card
                    continue
                if (mode == 'rank'):
                    if (CardIsHigherRank(card, bestCard)):
                        bestCard = card
                        continue
                    elif (CardIsSameRank(card, bestCard)):
                        if (CardIsHigherSuit(card, bestCard)):
                            bestCard = card
                            continue
                elif (mode == 'suit'):
                    if (CardIsHigherSuit(card, bestCard)):
                        bestCard = card
                        continue
                    elif (CardIsSameSuit(card, bestCard)):
                        if (CardIsHigherRank(card, bestCard)):
                            bestCard = card
                            continue
            originalHand.remove(bestCard)
            self.SetCard(bestCard, i)


    def SetSortMode(self, mode):
        if (self.sortMode != mode):
            self.sortMode = mode
            self.DisplayCards()

    def CheckForSelection(self, mx, my):
        for i in range(self.GetSize()):
            card = self.GetCardList()[self.GetSize()-1 - i]
            if (card.visual.IsTouchingMouse(mx, my)):
                if (card in self.selectedCards):
                    self.DeselectCard(card)
                elif (len(self.selectedCards) != 5):
                    self.SelectCard(card)
                return

    def CheckForHover(self, mx, my):
        foundCard = False
        for i in range(self.GetSize()):
            card = self.GetCardList()[self.GetSize()-1 - i]
            currentlyHovered = card.visual.IsTouchingMouse(mx, my)
            if (currentlyHovered and not foundCard):
                if (not card.visual.IsHovered()): 
                    card.visual.Hover(audio=True)
                foundCard = True
            elif (card.visual.IsHovered() and (foundCard or not currentlyHovered)):
                card.visual.Unhover()

    def SelectCard(self, card):
        if (not self.canSelectCards):
            return
        card.visual.Select(audio=True)
        self.selectedCards.append(card)
        self.OnSelectedCardsChanged()

    def DeselectCard(self, card, remove=True):
        card.visual.Deselect(audio=True)
        if (remove):
            self.selectedCards.remove(card)
        self.OnSelectedCardsChanged()

    def OnSelectedCardsChanged(self):
        if (self.HasCardsSelected()):
            Game.currentPokerHand = self.GetPokerHandType(self.selectedCards, len(self.selectedCards))
            Buttons.Enable(Buttons.PlayHand)
            if (Game.discards != 0):
                Buttons.Enable(Buttons.Discard)
        else:
            Game.currentPokerHand = PokerHand.NONE
            Buttons.Disable(Buttons.PlayHand)
            Buttons.Disable(Buttons.Discard)
        Sidebar.HandInfo.UpdateInfo(Game.currentPokerHand)
 
    def HasCardsSelected(self):
        return len(self.selectedCards) > 0

    def PlayHand(self, selectedCards, pokerHand):
        Game.PlayHand_CR.Instance.start(Game.PlayHand_Stages.stages, args=(selectedCards, pokerHand))

    def DiscardHand(self):
        Game.DiscardHand(self.selectedCards.copy())
        
    def GetPokerHandType(self, selectedCards, handSize):
        uniqueRanks = PokerHand.GetUniqueRanks(selectedCards)
        uniqueSuits = PokerHand.GetUniqueSuits(selectedCards)
        args = (handSize, uniqueRanks, uniqueSuits)

        sequence = []
        match handSize:
            case 1: sequence = [ PokerHand.HIGH_CARD ]
            case 2: sequence = [ PokerHand.PAIR, PokerHand.HIGH_CARD ]
            case 3: sequence = [ PokerHand.THREE_OF_A_KIND, PokerHand.PAIR, PokerHand.HIGH_CARD ]
            case 4: sequence = [ PokerHand.FOUR_OF_A_KIND, PokerHand.THREE_OF_A_KIND, PokerHand.TWO_PAIR, PokerHand.PAIR, PokerHand.HIGH_CARD ]
            case 5: sequence = [ PokerHand.FLUSH_FIVE, PokerHand.FLUSH_HOUSE, PokerHand.FIVE_OF_A_KIND, PokerHand.STRAIGHT_FLUSH, PokerHand.FOUR_OF_A_KIND, PokerHand.FULL_HOUSE, PokerHand.FLUSH, PokerHand.STRAIGHT, PokerHand.THREE_OF_A_KIND, PokerHand.TWO_PAIR, PokerHand.PAIR, PokerHand.HIGH_CARD ]
        for pokerHand in sequence:
            if (pokerHand.IsPlayed(*args)):
                return pokerHand

    def DisplayCards(self):
        handSize = self.GetSize()
        spreadDistance = 220
        spacing = spreadDistance/max(1, handSize-1)
        left = 255 - spreadDistance/2
        centerY = 280
        self.SortHand(self.sortMode)
        for i in range(handSize):
            card = self.GetCard(i)
            if (not card.visual.IsActive()):
                card.visual.CreateVisual(card.rank, card.suit, 255, centerY)
            card.visual.MoveVisual(left + i*spacing, None, animate=True, timeToMove=app.gameSpeed/6)
            card.visual.group.toFront()

class JokersDeck:
    def __init__(self, maxJokers):
        self.SetMaxJokers(maxJokers)
        self.jokersList = []
        self.canMoveJokers = True

    def GetSize(self):
        return len(self.jokersList)

    def SetMaxJokers(self, val):
        self.maxJokers = val

    def AddJoker(self, joker):
        self.jokersList.append(joker)
        JManager.Activate(joker)
        self.DisplayJokers()
        PlayingArea.jokersNumber.value = f"{self.GetSize()} / {self.maxJokers}"
        PlayingArea.jokersNumber.left = 127
    def RemoveJoker(self, joker):
        self.jokersList.remove(joker)
        JManager.Deactivate(joker)
        self.DisplayJokers()
        PlayingArea.jokersNumber.value = f"{self.GetSize()} / {self.maxJokers}"
        PlayingArea.jokersNumber.left = 127

    def DisplayJokers(self):
        spacing = 210 / max(1, len(self.jokersList)-1)
        left = 255 - 210 / 2
        centerY = 95

        for i in range(len(self.jokersList)):
            joker = self.jokersList[i]
            if (not joker.visual.IsActive()):
                joker.visual.CreateVisual(255, centerY)
            joker.visual.MoveVisual(left + i*spacing, centerY, animate=True, timeToMove=app.gameSpeed/6)
            joker.visual.group.toFront()

    def CheckForJokersClicked(self, mx, my):
        if (not self.canMoveJokers):
            return
        for joker in self.jokersList:
            if (not joker.visual.IsHovered()):
                continue
            if (joker.visual.group.hits(mx, my)):
                if (Game.state == GameState.SHOPPING or joker is self.jokersList[len(self.jokersList)-1]):
                    joker.visual.DeleteVisual()
                    Game.money += joker.sellValue
                    self.RemoveJoker(joker)
                    RoundInfo.Update(money=Game.money)
                    Audio.CARD_DESELECT.play(restart=True)
                else:
                    self.RemoveJoker(joker)
                    self.AddJoker(joker)
                    Audio.CARD_SELECT.play(restart=True)
                return

class Button:
    def OnClick(): pass
    def OnHover(): pass
    def OnUnhover(): pass
    def OnEnable(): pass
    def OnDisable(): pass



class UI:
    app.background = gradient(rgb(52, 111, 85).darker(), rgb(65, 133, 105), start='bottom-right')
    defaultColor = rgb(43, 57, 58)
    defaultDarkColor = rgb(18, 32, 34)
    blueColor = rgb(7, 145, 254)
    redColor = rgb(253, 69, 61)
    orangeColor = rgb(255, 153, 0)
    moneyColor = rgb(252, 181, 67)
    greenColor = rgb(63, 183, 129)

    def UpdateThemes(blind):
        Sidebar.UpdateThemes(blind)
        Bars.UpdateThemes(blind)
    def UpdateBossThemes(blind):
        Sidebar.UpdateBossThemes(blind)
        Bars.UpdateThemes(blind)

class Sidebar:
    background = Rect(10, -5, 100, 410, border='black', borderWidth=2.25)
    borders = Group(Rect(15, 80, 90, 20), Rect(15, 105, 90, 60, opacity=20))
    staticBorders = Group(Rect(45, 122.5, 57.5, 30), Rect(15, 200, 90, 50),)
    otherBorders = Group(Rect(15, 170, 90, 25),Rect(45, 255, 27.5, 22.5),Rect(77.5, 255, 27.5, 22.5),Rect(45, 282.5, 60, 22.5),Rect(45, 310, 27.5, 22.5),Rect(77.5, 310, 27.5, 22.5),)
    borderFills = Group(Rect(45, 172.5, 57.5, 20),Rect(48.75, 262.5, 20.25, 12.5),Rect(81.25, 262.5, 20.25, 12.5),Rect(48.75, 285, 52.5, 17.5),Rect(48.75, 317.5, 20.25, 12.5),Rect(81.25, 317.5, 20.25, 12.5),)
    kwargs = {'fill':'white', 'font':app.font, 'bold':True}
    staticText = Group(Label("Score at least", 73.75, 127, size=5.5, **kwargs),Label("Reward:", 63, 147, size=5.5, **kwargs),Label("Round", 30, 179, size=6.25, **kwargs),Label("score", 30, 187, size=6.75, **kwargs),Label("Hands", 58.75, 258.75, size=5, **kwargs),Label("Discards", 91, 258.75, size=5, **kwargs),Label("Ante", 58.75, 313.75, size=5, **kwargs),Label("Round", 91, 313.75, size=5, **kwargs),Label("/ 8", 63, 322.75, size=6, **kwargs))
    staticHandInfo = Group(Rect(20, 225, 32.5, 20),Rect(67.5, 225, 32.5, 20),Label("X", 60.5, 235, size=11, font=app.font, bold=True))
        
    class HandInfo:
        name = Label("", 77, 210, font=app.font, fill='white', size=10, bold=True, align='right')
        level = Label("", 80, 210.75, font=app.font, fill='white', size=7, bold=True, align='left')

        def UpdateInfo(hand):
            this = Sidebar.HandInfo
            this.name.value = hand.name
            this.name.size = hand.fontSize
            this.name.right = 77 + hand.offsetX
            if (hand is not PokerHand.NONE):
                this.level.value = f"lvl.{hand.level}"
                this.level.left = this.name.right + 5
            else:
                this.level.value = ""
            RoundInfo.Update(chips=hand.chips, mult=hand.mult)                

    def UpdateThemes(blind):
        this = Sidebar
        color = blind.color
        this.staticBorders.fill = UI.defaultDarkColor
        this.background.fill = UI.defaultColor
        this.background.border = color
        this.borders.fill = color
        this.borderFills.fill = UI.defaultColor
        this.otherBorders.fill = UI.defaultDarkColor
        handInfo = this.staticHandInfo.children
        handInfo[0].fill, handInfo[1].fill, handInfo[2].fill = (UI.blueColor, UI.redColor, UI.redColor)
    def UpdateBossThemes(blind):
        this = Sidebar
        color = blind.color
        darkColor = blind.darkColor
        this.background.fill = darkColor
        this.background.border = color
        this.borders.fill = color
        this.otherBorders.fill = color
        this.borderFills.fill = darkColor

class RoundInfo:
    kwargs = {'font':app.font, 'fill':'white', 'bold':True}
    kwargs2 = {'font':app.font, 'bold':True}

    blindName = Label("", 60, 90, size=12, **kwargs)
    blindDescription = Label("", 60, 110, size=6, **kwargs)
    blindDescription2 = Label("", 60, 117.5, size=6, **kwargs)
    scoreGoal = Label("0", 73.75, 137, size=11, **kwargs)
    roundScore = Label("0", 73.75, 182.5, size=14, **kwargs)
    reward = Label("", 77, 147, size=6.5, align='left', **kwargs)

    hands = Label(0, 58.875, 268.75, fill=rgb(7, 145, 254), size=11, **kwargs2)
    discards = Label(0, 91.375, 268.75, fill=rgb(253, 69, 61), size=11, **kwargs2)
    money = Label("$0", 75, 293, fill=rgb(252, 181, 67), size=12.5, **kwargs2)
    ante = Label(0, 54.25, 323.25, fill=rgb(255, 153 ,0), size=10, **kwargs2)
    round = Label(0, 91.375, 323.75, fill=rgb(255, 153 ,0), size=11, **kwargs2)

    chips = Label(0, 50, 235, size=12, align='right', **kwargs)
    mult = Label(0, 70, 235, size=12, align='left', **kwargs)
    handScore = Label("", 60.5, 210, size=14, **kwargs) 

    blindIcon = Group(Circle(30, 137, 12),Circle(30, 137, 12, fill=None, border=gradient('gray', 'black'), dashes=(4, 3), borderWidth=9, opacity=10),Circle(30, 137, 10, fill=None, border='white', dashes=(5, 4), borderWidth=2.2, opacity=90),Circle(30, 137, 12, fill='black', opacity=5))

    def GetScoreFontSize(score):
        if (score < 1_000): return 13
        elif (score < 10_000): return 12
        elif (score < 100_000): return 11.5
        elif (score < 1_000_000): return 10
        elif (score < 10_000_000): return 9
        elif (score < 100_000_000): return 8
        elif (score < 1_000_000_000): return 7.5
        elif (score >= 1_000_000_000): return 8.25

    def Update(blind=None, scoreGoal=None, roundScore=None, hands=None, discards=None, ante=None, round=None, money=None, chips=None, mult=None, handScore=None):
        this = RoundInfo
        if scoreGoal!=None: 
            this.scoreGoal.size = RoundInfo.GetScoreFontSize(scoreGoal)
            this.scoreGoal.value = f"© {scoreGoal:,}" if (scoreGoal < 1_000_000_000) else f"© {scoreGoal:.3e}"
            this.scoreGoal.fill = UI.redColor
        if roundScore!=None:
            this.roundScore.size = RoundInfo.GetScoreFontSize(roundScore)
            this.roundScore.value = f"© {roundScore:,}" if (roundScore < 1_000_000_000) else f"© {roundScore:.3e}"
        if blind!=None:
            this.blindName.value= blind.name
            this.blindIcon.children[0].fill = blind.color
            if (len(blind.desc) > 25):
                rightIndex = 26
                for i in range(0, rightIndex):
                    if (blind.desc[rightIndex-i] == ' '):
                        this.blindDescription.value = blind.desc[:rightIndex-i]
                        this.blindDescription2.value = blind.desc[rightIndex-i+1:]
                        break
            else:
                this.blindDescription.value = blind.desc
                this.blindDescription2.value = ""
            if (blind.reward <= 5):
                this.reward.value = blind.reward * "$"  
            else:
                this.reward.value = "$$$$$+"
            this.reward.left = 77
            this.reward.fill = UI.moneyColor
        if hands!=None:
            this.hands.value = hands
        if discards!=None:
            this.discards.value = discards
        if ante!=None:
            this.ante.value = ante
        if round!=None:
            this.round.value = round
        if money!=None:
            this.money.value = f"${money:,}"
        if chips!=None:
            this.chips.value = f"{chips:,}"
            this.chips.right = 50
        if mult!=None:
            this.mult.value = f"{mult:,}"
            this.mult.left = 70
        if handScore!=None:
            this.handScore.value = f"{handScore:,}"

class PlayingArea:
    handBackground = Rect(130, 255, 250, 50, opacity=10)
    jokersBackground  = Rect(125, 68, 260, 54, opacity=10)
    jokersNumber = Label("0 / 6", 127, 129, font=app.font, size=6.5, fill='white', bold=True, align='left')
    sortHandBorder = Group(Rect(230, 316, 50, 32, fill=None, border=rgb(245,245,245).darker().darker()),Rect(230, 314, 50, 32, fill=None, border=rgb(245,245,245)),Label("Sort Hand", 255, 322.5, font=app.font, size=6.5, fill='white', bold=True),)

class Bars:
    top = Rect(-200, -5, 800, 55, fill=gradient(rgb(25, 35, 33), 'black', start='bottom'), border=gradient(rgb(23, 37, 38), rgb(96, 78, 5), rgb(23, 37, 38), start='left'), borderWidth=5, align='top-left')
    bottom = Rect(-200, 405, 800, 55, fill=gradient(rgb(25, 35, 33), 'black', start='top'), border=gradient(rgb(23, 37, 38), rgb(96, 78, 5), rgb(23, 37, 38), start='left'), borderWidth=5, align='bottom-left')
    CRT = Line(200, 0, 200, 400, lineWidth=400, dashes=(1.25, 1.25), opacity=2) 
    group = Group( top, bottom, CRT )

    def UpdateThemes(blind):
        color = blind.color
        Bars.top.border = gradient(rgb(23, 37, 38), color, rgb(23, 37, 38), start='left')
        Bars.bottom.border = gradient(rgb(23, 37, 38), color, rgb(23, 37, 38), start='left')

class Buttons:
    activeButtons = []

    def Enable(button):
        if (not button in Buttons.activeButtons):
            Buttons.activeButtons.append(button)
        button.OnEnable()
    def Disable(button):
        if (button in Buttons.activeButtons):
            Buttons.activeButtons.remove(button)
        button.OnDisable()
    def HandleButtonsClick(mx, my):
        for button in Buttons.activeButtons:
            if (button.group.hits(mx, my)):
                button.OnClick()
    def HandleButtonsHover(mx, my):
        for button in Buttons.activeButtons:
            if (button.group.hits(mx, my)):
                button.OnHover()
            else:
                button.OnUnhover()

    class RunInfo:
        group = Group(Rect(18, 259, 24.5, 32.5, opacity=32),Rect(16.5, 257, 24.5, 32.5, fill=rgb(253, 69, 61)),Label("Run", 28.75, 269.75, font=app.font, fill='white', size=6.25, bold=True),Label("Info", 28.75, 276.75, font=app.font, fill='white', size=6, bold=True),)

    class Options:
        group = Group(Rect(18, 299, 24.5, 32.5, opacity=32),Rect(16.5, 297, 24.5, 32.5, fill=rgb(255, 153 ,0)),Label("Options", 28.75, 313.25, font=app.font, fill='white', size=5.5, bold=True),)
            
    class PlayHand(Button):
        group = Group(Rect(175, 318, 50, 28, opacity=32),Rect(175, 316, 50, 28, fill=rgb(43, 57, 58)),Label("Play Hand", 200, 327, font=app.font, size=7, fill=rgb(43, 57, 58).lighter(), bold=True))
        def OnEnable():
            this = Buttons.PlayHand
            child = this.group.children
            child[1].fill = rgb(7, 145, 254)
            child[2].fill = rgb(255,255,255)
        def OnDisable():
            this = Buttons.PlayHand
            child = this.group.children
            child[1].fill = rgb(43, 57, 58)
            child[2].fill = rgb(43, 57, 58).lighter()
        def OnHover():
            this = Buttons.PlayHand
            child = this.group.children
            child[1].fill = rgb(7, 145, 254).darker()
            child[2].fill = rgb(255,255,255).darker()
        def OnUnhover():
            this = Buttons.PlayHand
            this.OnEnable()
        def OnClick():
            Audio.BUTTON_CLICK.play(restart=True)
            app.playTut.visible = False
            app.scoreTut.visible = False
            Game.activeHand.PlayHand(Game.activeHand.selectedCards.copy(), Game.currentPokerHand)

    class Discard(Button):
        group = Group(Rect(285, 318, 50, 28, opacity=32),Rect(285, 316, 50, 28, fill=rgb(43, 57, 58)),Label("Discard", 310, 327, font=app.font, size=7, fill=rgb(43, 57, 58).lighter(), bold=True))
        def OnEnable():
            this = Buttons.Discard
            child = this.group.children
            child[1].fill = rgb(253, 69, 61)
            child[2].fill = rgb(255,255,255)
        def OnDisable():
            this = Buttons.Discard
            child = this.group.children
            child[1].fill = rgb(43, 57, 58)
            child[2].fill = rgb(43, 57, 58).lighter()
        def OnHover():
            this = Buttons.Discard
            child = this.group.children
            child[1].fill = rgb(253, 69, 61).darker()
            child[2].fill = rgb(255,255,255).darker()
        def OnUnhover():
            this = Buttons.Discard
            this.OnEnable()
        def OnClick():
            Audio.BUTTON_CLICK.play(restart=True)
            app.discardTut.visible = False
            Game.activeHand.DiscardHand()

    class SortRank(Button):
        group = Group(Rect(235, 329.25, 18, 13, opacity=32),Rect(235, 328, 18, 13, fill=rgb(43, 57, 58)),Label("Rank", 244, 334.5, font=app.font, size=5.5, fill=rgb(43, 57, 58).lighter(), bold=True))
        def OnEnable():
            this = Buttons.SortRank
            child = this.group.children
            child[1].fill = rgb(255, 153, 0)
            child[2].fill = rgb(255,255,255)
        def OnDisable():
            this = Buttons.SortRank
            child = this.group.children
            child[1].fill = rgb(43, 57, 58)
            child[2].fill = rgb(43, 57, 58).lighter()
        def OnHover():
            this = Buttons.SortRank
            child = this.group.children
            child[1].fill = rgb(255, 153, 0).darker()
            child[2].fill = rgb(255,255,255).darker()
        def OnUnhover():
            this = Buttons.SortRank
            this.OnEnable()
        def OnClick():
            Audio.BUTTON_CLICK.play(restart=True)
            Game.activeHand.SetSortMode('rank')

    class SortSuit(Button):
        group = Group(Rect(257, 329.25, 18, 13, opacity=32),Rect(257, 328, 18, 13, fill=rgb(43, 57, 58)),Label("Suit", 266, 334.5, font=app.font, size=5.5, fill=rgb(43, 57, 58).lighter(), bold=True))
        def OnEnable():
            this = Buttons.SortSuit
            child = this.group.children
            child[1].fill = rgb(255, 153, 0)
            child[2].fill = rgb(255,255,255)
        def OnDisable():
            this = Buttons.SortSuit
            child = this.group.children
            child[1].fill = rgb(43, 57, 58)
            child[2].fill = rgb(43, 57, 58).lighter()
        def OnHover():
            this = Buttons.SortSuit
            child = this.group.children
            child[1].fill = rgb(255, 153, 0).darker()
            child[2].fill = rgb(255,255,255).darker()
        def OnUnhover():
            this = Buttons.SortSuit
            this.OnEnable()
        def OnClick():
            Audio.BUTTON_CLICK.play(restart=True)
            Game.activeHand.SetSortMode('suit')

    class NextRound(Button):
        group = Group(Rect(141.5, 166.5, 56, 32, fill=rgb(253, 69, 61).darker().darker().darker()),Rect(140, 165, 56, 32, fill=rgb(253, 69, 61)),Label("Next", 168, 177, font=app.font, size=8, fill='white', bold=True),Label("Round", 168, 185, font=app.font, size=8, fill='white', bold=True),)
        def OnHover():
            this = Buttons.NextRound
            child = this.group.children
            child[0].fill = rgb(253, 69, 61).darker().darker().darker().darker()
            child[1].fill = rgb(253, 69, 61).darker().darker()
            child[2].fill, child[3].fill = 2*(rgb(255,255,255).darker(),)
        def OnUnhover():
            this = Buttons.NextRound
            child = this.group.children
            child[0].fill = rgb(253, 69, 61).darker().darker().darker()
            child[1].fill = rgb(253, 69, 61)
            child[2].fill, child[3].fill = 2*('white',)
        def OnClick():
            Game.NextRound()

    class RerollShop(Button):
        cost = Label("$5", 168, 221, font=app.font, size=11, fill='white', bold=True)
        group = Group(Rect(141.5, 202.5, 56, 32, fill=rgb(63, 183, 129).darker().darker().darker()),Rect(140, 201, 56, 32, fill=rgb(63, 183, 129)),Label("Reroll", 168, 211, font=app.font, size=8, fill='white', bold=True),cost)
        def OnHover():
            this = Buttons.RerollShop
            child = this.group.children
            child[0].fill = rgb(63, 183, 129).darker().darker().darker().darker()
            child[1].fill = rgb(63, 183, 129).darker().darker()
            child[2].fill, child[3].fill = 2*(rgb(255,255,255).darker(),)
        def OnUnhover():
            this = Buttons.RerollShop
            child = this.group.children
            child[0].fill = rgb(63, 183, 129).darker().darker().darker()
            child[1].fill = rgb(63, 183, 129)
            child[2].fill, child[3].fill = 2*('white',)
        def OnClick():
            Audio.BUTTON_CLICK.play(restart=True)
            Shop.Reroll()

class Effects:
    activeEffects = []
    deletedEffects = []

    def AddEffect(stepFunc):
        Effects.activeEffects.append(stepFunc)
    def RemoveEffect(stepFunc):
        Effects.deletedEffects.append(stepFunc)

    def HandleEffects():
        for deletedEffect in Effects.deletedEffects:
            if (deletedEffect in Effects.activeEffects):
                Effects.activeEffects.remove(deletedEffect)
        Effects.deletedEffects.clear()
        for effect in Effects.activeEffects:
            effect()

    class InfoPopup:
        def __init__(self, text, posX, posY, dir, color, startSize, textSize):
            self.minRotateAngle = -30
            self.maxRotateAngle = 30
            self.growSpeed = 32 / app.gameSpeed
            self.fadeSpeed = 350 / app.gameSpeed
            self.fadeBuffer = app.gameSpeed/4
            self.velY = 5 / app.gameSpeed * dir
            self.timer = 0
            self.square = Rect(-startSize/2, -startSize/2, startSize, startSize, fill=color, rotateAngle=random.uniform(self.minRotateAngle, self.maxRotateAngle))
            self.group = Group( self.square,Label(text, 0, 0, font=app.font, size=textSize, fill='white', bold=True), )
            self.group.centerX = posX
            self.group.centerY = posY
            Effects.AddEffect(self.Step)

        def Delete(self):
            Effects.RemoveEffect(self.Step)
            self.group.visible = False

        def Step(self):
            self.timer += Time.deltaTime
            self.group.centerY += self.velY * Time.deltaTime
            oldX, oldY = self.square.centerX, self.square.centerY
            self.square.width += self.growSpeed * Time.deltaTime
            self.square.height += self.growSpeed * Time.deltaTime
            self.square.centerX, self.square.centerY = oldX, oldY
            if (self.timer >= self.fadeBuffer):
                self.group.opacity = max(0, self.group.opacity - self.fadeSpeed * Time.deltaTime)
                if (self.group.opacity == 0):
                    self.Delete()

    def AddChipsEffect(chips, posX, posY, dir):
        effect = Effects.InfoPopup(f"+{chips}", posX, posY, dir, rgb(7, 145, 254), 7, 9.5)
        Audio.CHIPS_ADDED.play(restart=True)
    def AddMultEffect(mult, posX, posY, dir):
        effect = Effects.InfoPopup(f"+{mult} Mult", posX, posY, dir, rgb(253, 69, 61), 11, 6)
        Audio.MULT_ADDED.play(restart=True)
    def TimesMultEffect(timesMult, posX, posY, dir):
        effect = Effects.InfoPopup(f"X{timesMult} Mult", posX, posY, dir, rgb(253, 69, 61), 11, 6)
        Audio.MULT_MULTIPLIED.play(restart=True)

    class CountUpChipsToScore:
        def Start(handScore):
            this = Effects.CountUpChipsToScore
            Effects.AddEffect(this.Step)
            this.chips = handScore
            this.score = Game.roundScore
            this.animationTime = app.gameSpeed/2
            this.timer = 0
            this.rate = this.chips / this.animationTime

        def Stop():
            this = Effects.CountUpChipsToScore
            Effects.RemoveEffect(this.Step)

        def Step():
            this = Effects.CountUpChipsToScore
            this.timer += Time.deltaTime
            if (this.timer >= this.animationTime):
                RoundInfo.Update(handScore="", roundScore=Game.roundScore)
                this.Stop()
                return
            this.chips -= this.rate * Time.deltaTime
            this.score += this.rate * Time.deltaTime
            RoundInfo.Update(handScore=int(this.chips), roundScore=int(this.score))

    class OpeningFade:
        kwargs = {'font':app.font,'fill':'white'}
        screenCover = Group(
            Rect(0,0, 400,400),
            Rect(10,123, 380,130),
            Label("Based on BALATRO", 200, 148, size=35, bold=True, **kwargs),
            Label("original game developed by LocalThunk", 200, 175.5, size=17, **kwargs),
            Label("Filter through your deck to play poker hands for score!", 200, 208, size=12, italic=True, **kwargs),
            Label("Defeat different blinds by reaching their score requirement.", 200, 223, size=12, italic=True, **kwargs),
            Label("Unlock Jokers in the Shop for game-changing upgrades!", 200, 238, size=12, italic=True, **kwargs),
            )
        def Step():
            this = Effects.OpeningFade
            this.screenCover.opacity = max(0, Effects.OpeningFade.screenCover.opacity - 7 * Time.deltaTime)
            if (this.screenCover.opacity == 0):
                Effects.RemoveEffect(this.Step)
                this.screenCover.visible = False


    class MoveAnimation:
        def __init__(self, activeList, disabledList):
            self.startX, self.startY, self.targetX, self.targetY, self.timeToMove = 5*(0,)
            self.activeList = activeList
            self.disabledList = disabledList

        def SetGroup(self, group):
            self.group = group
            if group is None:
                self.Stop(forceStop=True)

        def Start(self, targetX, targetY, timeToMove):
            self.timeToMove = timeToMove
            self.startX, self.startY = self.group.centerX, self.group.centerY
            self.targetX, self.targetY = targetX, targetY
            self.velX = (self.targetX - self.startX) / self.timeToMove
            self.velY = (self.targetY - self.startY) / self.timeToMove
            if (not self.Step in self.activeList):
                self.activeList.append(self.Step)

        def Stop(self, forceStop=False):
            if (forceStop and self.Step in self.activeList):
                self.activeList.remove(self.Step)
                return
            else:
                self.disabledList.append(self.Step)
            if (self.group is not None):
                self.group.centerX = self.targetX
                self.group.centerY = self.targetY

        def Step(self):
            newX = self.group.centerX + self.velX * Time.deltaTime
            if ((self.velX > 0 and newX > self.targetX) or (self.velX < 0 and newX < self.targetX)):
                newX = self.targetX
            newY = self.group.centerY + self.velY * Time.deltaTime
            if ((self.velY > 0 and newY > self.targetY) or (self.velY < 0 and newY < self.targetY)):
                newY = self.targetY
            if (newX == self.targetX and newY == self.targetY):
                self.Stop()
                return
            self.group.centerX, self.group.centerY = newX, newY

class Shop:
    class BlindInfoBox:
        def __init__(self, posX, posY):
            kwargs = {'font':app.font, 'bold':True}
            self.group = Group(Rect(3,3, 60, 80),Rect(1.5,1.5, 60, 80),Rect(0,0, 60, 80),Label("", 31, 17, fill='black', size=8, **kwargs, opacity=35),Label("", 30, 16, fill='white', size=8, **kwargs),Rect(4, 31, 52, 34),Rect(7, 34, 49, 31),Label("", 32, 43.5, fill=rgb(245, 245, 245), **kwargs),Label("", 30, 57, fill=rgb(252, 181, 67), size=5.5, **kwargs),Label("Reward:", 33, 57, fill='white', size=5, align='right', **kwargs))
            self.group.left, self.group.top = posX, posY
        def UpdateInfo(self, baseScoreGoal, blind):
            child = self.group.children
            child[0].fill = blind.color.darker().darker()
            child[1].fill = blind.color.darker()
            child[2].fill = blind.color
            child[3].value, child[4].value = 2*(blind.name,)
            child[5].fill = blind.color.darker().darker()
            child[6].fill = blind.color.darker().darker().darker()
            child[7].size = 0.9 * RoundInfo.GetScoreFontSize(int(baseScoreGoal * blind.baseScoreMult))
            child[7].value = f"© {int(baseScoreGoal * blind.baseScoreMult):,}"
            child[8].value = blind.reward * "$"
            child[8].left = child[9].right + 2

    background = Rect(125, 150, 260, 250, fill=rgb(18, 32, 34), border=rgb(43, 57, 58), borderWidth=4)
    cardsBackground = Rect(201, 165, 169, 70, fill=rgb(43, 57, 58))
    blindsBackground = Rect(140, 250, 230, 100, fill=rgb(43, 57, 58))

    smallBlind = BlindInfoBox(152.5, 260)
    bigBlind = BlindInfoBox(225, 260)
    bossBlind = BlindInfoBox(297.5, 260)
    group = Group(background, cardsBackground, blindsBackground, smallBlind.group, bigBlind.group, bossBlind.group)

    size = 3
    jokersOnSale = []
    rerollPrice = 5

    def Initialize():
        this = Shop
        Buttons.Enable(Buttons.NextRound)
        Buttons.Enable(Buttons.RerollShop)
        this.group.add(Buttons.NextRound.group, Buttons.RerollShop.group)
        this.group.toFront()
        this.group.top = 400
        this.animSpeed = 2 / app.gameSpeed
        this.animPosition = 0
        this.animDir = 1

    def StartAnimation(dir):
        this = Shop
        this.animDir = dir
        Effects.AddEffect(this.Step)
        Buttons.Disable(Buttons.NextRound)
        Buttons.Disable(Buttons.RerollShop)
    def StopAnimation():
        Effects.RemoveEffect(Shop.Step)
        Buttons.Enable(Buttons.NextRound)
        Buttons.Enable(Buttons.RerollShop)
    def Step():
        this = Shop
        t = this.animPosition
        if ((this.animDir==1 and t==1) or (this.animDir==-1 and t==0)):
            this.StopAnimation()
            if (this.animDir == 1):
                this.group.bottom = 400
                this.GenerateInventory()
                return
            elif (this.animDir == -1):
                this.group.top = 400
                return
        animPos = 1 + 2.70158*(t-1)**3 + 1.70158*(t-1)**2
        posY = animPos * 250
        this.group.bottom = 650-posY
        if (this.animDir==-1):
            this.group.toFront()
        this.animPosition = max(0, min(1, t + this.animSpeed * this.animDir * Time.deltaTime))

    def GenerateInventory():
        this = Shop
        oldJokers = this.jokersOnSale.copy()
        for i in range(this.size):
            jokersOfRarity = None
            for j in range(50000):
                key = random.randint(1, 100)
                rarity = None
                if (key <= 5):
                    rarity = Rarity.RARE
                elif (key <= 30):
                    rarity = Rarity.UNCOMMON
                elif (key <= 100):
                    rarity = Rarity.COMMON
                _jokersOfRarity = JManager.GetJokersOfRarity(rarity)
                if (len(_jokersOfRarity) != 0):
                    jokersOfRarity = _jokersOfRarity
                    break
            if (jokersOfRarity is None):
                raise Exception("No jokers seem to be available (shop only drew rarities with empty lists)")
            joker = random.choice(jokersOfRarity)
            JManager.Activate(joker, silent=True)
            this.jokersOnSale.append(joker)
        for joker in oldJokers:
            joker.visual.DeleteVisual()
            this.jokersOnSale.remove(joker)
            JManager.Deactivate(joker, silent=True)
        spreadDistance = 108
        spacing = spreadDistance/(this.size-1)
        left = 285.5 - spreadDistance/2
        centerY = this.group.top + 50
        for i in range(this.size):
            joker = this.jokersOnSale[i]
            if (joker.visual.IsActive()):
                joker.visual.DeleteVisual()
            joker.visual.CreateVisual(285.5, centerY + random.randint(-40, 40))
            joker.visual.MoveVisual(left + i*spacing, centerY, animate=True, timeToMove=app.gameSpeed/5)

    def Reroll():
        this = Shop
        if (Game.money < this.rerollPrice):
            return
        Game.money -= this.rerollPrice
        this.GenerateInventory()
        this.rerollPrice += 1
        Buttons.RerollShop.cost.value = f"${this.rerollPrice}"
        RoundInfo.Update(money=Game.money)

    def CheckForJokersClicked(mx, my):
        this = Shop
        if (Game.jokersDeck.GetSize() == Game.maxJokers):
            return
        for joker in this.jokersOnSale:
            if (Game.money < joker.price or not joker.visual.IsHovered() or joker.visual.group is None):
                continue
            if (joker.visual.group.hits(mx, my)):
                app.jokerTut.visible = False
                Game.money -= joker.price
                JManager.Deactivate(joker, True)
                this.jokersOnSale.remove(joker)
                Game.jokersDeck.AddJoker(joker)
                RoundInfo.Update(money=Game.money)
                Audio.CARD_SELECT.play(restart=True)
                return

    def Open(baseScoreGoal, bossBlind):
        this = Shop
        this.background.border = bossBlind.color
        this.smallBlind.UpdateInfo(baseScoreGoal, Blind.Small)
        this.bigBlind.UpdateInfo(baseScoreGoal, Blind.Big)
        this.bossBlind.UpdateInfo(baseScoreGoal, bossBlind)
        this.rerollPrice = 5
        Buttons.RerollShop.cost.value = f"${this.rerollPrice}"
        if (this.group.top == 400):
            this.StartAnimation(1)
        Buttons.Disable(Buttons.SortRank)
        Buttons.Disable(Buttons.SortSuit)

    def Close():
        this = Shop
        if (this.group.bottom == 400):
            this.StartAnimation(-1)
        for joker in this.jokersOnSale:
            JManager.Deactivate(joker, silent=True)
            joker.visual.DeleteVisual()
        this.jokersOnSale.clear()
        Buttons.Enable(Buttons.SortRank)
        Buttons.Enable(Buttons.SortSuit)

Effects.AddEffect(Effects.OpeningFade.Step)



class GameState(Enum):
    CHOOSING_HAND = 0
    PLAYING_HAND = 1
    SHOPPING = 2
    NONE = 3

class Game:
    fullDeck = FullDeck()
    state = GameState.NONE

    maxHands = 4
    maxDiscards = 4
    money = 4
    ante = 0
    round = 0

    maxHandSize = 8
    maxJokers = 6
    jokersDeck = JokersDeck(maxJokers)

    anteProgress = -1
    baseAnteScores = {
        1: 300,
        2: 800,
        3: 2_800,
        4: 6_000,
        5: 11_000,
        6: 20_000,
        7: 35_000,
        8: 50_000,
        9: 110_000,
        10: 560_000,
        11: 7_200_000,
        12: 300_000_000,
        13: 47_000_000_000,
    }

    def AnteUp():
        Game.ante += 1
        Game.anteProgress = 0
        Game.bossBlind = Blind.GetRandomBossBlind()
        Game.baseScoreGoal = Game.baseAnteScores[Game.ante]
        RoundInfo.Update(ante=Game.ante)
        Audio.ANTE_UP.play(restart=True)
        if (Game.ante == 9):
            kwargs = {'font':app.font, 'fill':rgb(252, 181, 67), 'bold':True, 'size':14}
            Bars.group.add(Label("Nice job! You got past Ante 8 and beat the Game!", 200, 25, **kwargs),Label("Now, continue your run in Endless Mode!", 200, 375, **kwargs))
        
    def EndRound():
        Event.Call(Event.ON_ROUND_END)
        Game.money += Game.blind.reward
        RoundInfo.Update(hands=Game.hands, discards=Game.discards, money=Game.money)
        for card in Game.activeHand.GetCardList():
            card.visual.DeleteVisual()

        if (Game.roundScore < Game.scoreGoal):
            Game.LoseGame()

        Game.roundDeck = None
        Game.activeHand = None
        Game.anteProgress += 1
        if (Game.anteProgress == 3):
            Game.AnteUp()
        match Game.anteProgress:
            case 0: Game.blind = Blind.Small
            case 1: Game.blind = Blind.Big
            case 2: Game.blind = Game.bossBlind
        Game.OpenShop()

    def OpenShop():
        Game.state = GameState.SHOPPING
        Shop.Open(Game.baseScoreGoal, Game.bossBlind)

    def NextRound():
        Shop.Close()
        Game.StartRound(Game.blind)

    def StartRound(blind):
        Game.roundDeck = EffectiveDeck(Game.fullDeck)
        Game.activeHand = Hand(Game.maxHandSize, Game.roundDeck)
        Game.state = GameState.CHOOSING_HAND
        Game.scoreGoal = int(Game.baseScoreGoal * Game.blind.baseScoreMult)
        Game.roundScore = 0
        Game.hands = Game.maxHands
        Game.discards = Game.maxDiscards
        Game.round += 1
        Event.Call(Event.ON_ROUND_START)

        if (blind != BossBlind):
            UI.UpdateThemes(blind)
        else:
            UI.UpdateBossThemes(blind)
        RoundInfo.Update(scoreGoal=Game.scoreGoal, roundScore=Game.roundScore, blind=blind,hands=Game.hands,discards=Game.discards,money=Game.money,ante=Game.ante,round=Game.round,)
        Buttons.Enable(Buttons.SortRank)
        Buttons.Enable(Buttons.SortSuit)

    def LoseGame():
        Rect(0,0,400,400,opacity=60)
        Label("uh oh, you lost.", 200, 200, font=app.font, fill='white', size=32)
        app.stop()

    def DiscardHand(selectedCards):
        Event.Call(Event.ON_DISCARD, args=(Game.currentPokerHand, selectedCards))
        for card in selectedCards:
            Game.activeHand.DeselectCard(card)
            card.visual.DeleteVisual()
            Game.activeHand.RemoveCard(card)
        Game.activeHand.FillHand(Game.activeHand.sourceDeck)    
        Game.discards -= 1
        RoundInfo.Update(discards=Game.discards)

    class PlayHand_Stages:
        HAND_PLAYED = CoroutineStage()
        EFF_CARDS = CoroutineStage()
        CALC_CARDS = CoroutineStage()
        CALC_SCORE = CoroutineStage()
        COUNT_CHIPS = CoroutineStage()
        CLEAR_BOARD = CoroutineStage()
        JOKER_CALCS = CoroutineStage()
        stages = [ HAND_PLAYED, EFF_CARDS, CALC_CARDS, CALC_SCORE, COUNT_CHIPS, CLEAR_BOARD, JOKER_CALCS ]

    ##### This system was a PAIN to make without async
    class PlayHand_CR(Coroutine):
        def resetVars(self):
            s = Game.PlayHand_Stages
            s.CALC_CARDS.indexes.clear()
            s.CALC_CARDS.indexes.insert(0, 0)
            s.JOKER_CALCS.indexes.clear()
            s.JOKER_CALCS.indexes.insert(0, 0)
            self.effectiveCards = None
            self.chips = 0
            self.mult = 0
            self.handScore = 0
            self.eventToCheck = None
            self.targetIndexAfterDone = -1

        def SkipToJokerCalculations(self, event, eventArgs, targetIndex):
            s = Game.PlayHand_Stages
            self.eventToCheck = event
            self.eventToCheckArgs = eventArgs
            self.targetIndexAfterDone = targetIndex
            self.setStage(6)
            s.JOKER_CALCS.indexes[0] = 0

        def nextStep(self, stage, selectedCards, pokerHand):
            s = Game.PlayHand_Stages
            waitTime = app.gameSpeed/2
            match stage:
                case s.HAND_PLAYED:
                    spreadDistance = 165
                    spacing = spreadDistance/max(1, len(selectedCards)-1)
                    left = 255 - spreadDistance/2
                    centerY = 215
                    for i in range(len(selectedCards)):
                        card = selectedCards[i]
                        if (card.visual.IsActive()):
                            card.visual.MoveVisual(left + i*spacing, centerY, animate=True, timeToMove=app.gameSpeed/6)
                            card.visual.idleAnimation.Stop()
                        else:
                            raise Exception("Tried to play a card that didn't have a visual!")
                        Game.activeHand.RemoveCard(card)
                        if (card.visual.IsHovered()):
                            card.visual.Unhover()

                    Game.activeHand.selectedCards.clear()
                    Game.activeHand.OnSelectedCardsChanged()
                    Game.activeHand.DisplayCards()
                    Game.activeHand.canSelectCards = False
                    Game.jokersDeck.canMoveJokers = False

                    Game.state = GameState.PLAYING_HAND
                    Game.hands -= 1
                    RoundInfo.Update(hands=Game.hands)
                    Sidebar.HandInfo.UpdateInfo(pokerHand)

                    self.nextStage()
                    return waitTime

                case s.EFF_CARDS:
                    self.chips = pokerHand.chips
                    self.mult = pokerHand.mult
                    self.effectiveCards = pokerHand.GetEffectiveCards(PokerHand.GetUniqueRanks(selectedCards), selectedCards)

                    for card in self.effectiveCards:
                        card.visual.MoveVisual(None, card.visual.group.centerY-12.5, animate=True, timeToMove=app.gameSpeed/12)

                    if (Event.ON_HAND_PLAY.GetSize() != 0):
                        self.SkipToJokerCalculations(Event.ON_HAND_PLAY, (pokerHand, selectedCards.copy(), self.effectiveCards.copy()), 2)
                        return waitTime

                    self.nextStage()
                    return waitTime

                case s.CALC_CARDS:
                    i = s.CALC_CARDS.indexes[0]

                    if (i < len(self.effectiveCards)):
                        card = self.effectiveCards[i]
                        chips = card.GetChips()
                        self.chips += chips
                        Effects.AddChipsEffect(chips, card.visual.group.centerX, card.visual.group.top-15, -1)
                        RoundInfo.Update(chips=self.chips, mult=self.mult)
                        s.CALC_CARDS.indexes[0] += 1
                        if (Event.ON_CARD_SCORED.GetSize() != 0):
                            self.SkipToJokerCalculations(Event.ON_CARD_SCORED, (card,), 2)
                            return waitTime

                    elif (i == len(self.effectiveCards)):
                        if (Event.ON_HAND_END.GetSize() != 0):
                            self.SkipToJokerCalculations(Event.ON_HAND_END, (pokerHand, selectedCards.copy(), self.effectiveCards.copy()), 3)
                            return self.nextStep(self.stage, selectedCards, pokerHand)
                        self.nextStage()
                    return waitTime

                case s.CALC_SCORE:
                    self.handScore = int(self.chips * self.mult)
                    Game.activeHand.OnSelectedCardsChanged()
                    RoundInfo.Update(handScore=self.handScore)
                    Audio.CHIPS_CALCULATED.play(restart=True)

                    for card in self.effectiveCards:
                        card.visual.MoveVisual(None, card.visual.group.centerY+12.5, animate=True, timeToMove=app.gameSpeed/12)

                    self.nextStage()
                    return waitTime

                case s.COUNT_CHIPS:
                    Audio.TOTAL_CHIPS_ADDED.play(restart=True)
                    Effects.CountUpChipsToScore.Start(self.handScore)
                    Game.roundScore += self.handScore

                    self.nextStage()
                    return waitTime
                
                case s.CLEAR_BOARD:
                    for card in selectedCards:
                        card.visual.DeleteVisual()
                    Game.activeHand.FillHand(Game.roundDeck)
                    Game.activeHand.canSelectCards = True
                    Game.jokersDeck.canMoveJokers = True

                    Game.state = GameState.CHOOSING_HAND
                    if (Game.hands == 0 or Game.roundScore >= Game.scoreGoal or Game.activeHand.GetSize() == 0):
                        Game.EndRound()

                    self.end()
                    return 0

                case s.JOKER_CALCS:
                    i = s.JOKER_CALCS.indexes[0]
                    while True:
                        if (i < self.eventToCheck.GetSize()):
                            if (Event.CallSingle(self.eventToCheck, i, args=self.eventToCheckArgs) == True):
                                if (i == self.eventToCheck.GetSize()-1):
                                    self.setStage(self.targetIndexAfterDone)
                                s.JOKER_CALCS.indexes[0] = i+1
                                return waitTime
                            i += 1
                            continue
                        elif (i == self.eventToCheck.GetSize()):
                            self.setStage(self.targetIndexAfterDone)
                            return self.nextStep(self.stage, selectedCards, pokerHand)

    PlayHand_CR.Instance = PlayHand_CR()
    

    
kwargs = {"size":5, "fill":'white', "bold":True, "italic":True}
app.playTut = Group(
Label("Play your hand", 144, 322, **kwargs),
Label("and draw new cards.", 144, 329, **kwargs),
Label("(any amount 1-5) -->", 144, 336, **kwargs),
)
app.discardTut = Group(
Label("Discard your hand", 366, 322, **kwargs),
Label("and draw new cards.", 366, 329, **kwargs),
Label("<-- (any amount 1-5)", 366, 336, **kwargs),
)
app.scoreTut = Group(
Label("<-- Reach this score to win the round.", 158, 144, **kwargs),
Label("Play hands to earn score", 142, 179, **kwargs),
Label("<------- for this round.", 142, 186, **kwargs),
Label("<----------- This is your hand info.    ", 162, 207, **kwargs),
Label("The blue is 'Chips', the red is 'Mult';", 162, 214, **kwargs),
Label("a hand's score equals Chips TIMES Mult.", 162, 221, **kwargs),
Label("Stronger poker hands have better stats.", 162, 234, **kwargs),
Label("Extra stats come from cards & jokers.", 162, 241, **kwargs),
)
app.jokerTut = Group(
Label("Your jokers will appear here. You can buy jokers in the shop. (Check the gray text under their descriptions).", 255, 78, **kwargs),
Label("Joker abilities will activate automatically. Their ability and when it activates depends on their description.", 255, 85, **kwargs),
Label("Most jokers have round-specific abilities. Others, however, may have lasting traits.", 255, 98, **kwargs),
Label("Jokers with a lasting trait will always have '(Currently ...)' in their description to show the current stat.", 255, 105, **kwargs),
Label("Jokers with a lasting trait will maintain that trait and its stats for the entire game or until sold.", 255, 112, **kwargs),
)



Game.blind = Blind.Small
Shop.Initialize()
Game.AnteUp()
Game.NextRound()

def onMousePress(mx, my):
    if (Game.activeHand is not None):
        Game.activeHand.CheckForSelection(mx, my)
    if (Game.jokersDeck is not None):
        Game.jokersDeck.CheckForJokersClicked(mx, my)
    if (Game.state is GameState.SHOPPING):
        Shop.CheckForJokersClicked(mx, my)
    Buttons.HandleButtonsClick(mx, my)


def onMouseMove(mx, my):
    if (Game.activeHand is not None):
        Game.activeHand.CheckForHover(mx, my)
    Buttons.HandleButtonsHover(mx, my)
    Joker.HandleHovers(mx, my)


app.stepsPerSecond = 240     
def onStep():
    Time.Update()
    Coroutine.HandleCoroutines()
    Card.HandleAnimations()
    Effects.HandleEffects()
    Joker.HandleAnimations()
    Bars.group.toFront()
    Effects.OpeningFade.screenCover.toFront()