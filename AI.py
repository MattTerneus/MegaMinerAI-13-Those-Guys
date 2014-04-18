#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
from operator import *
import random
import prioritizer
import ASTAR

spawnList={}
restrictedList = {}
forwardList = {}
keyList = []

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Those Guys"

  @staticmethod
  def password():
    return "password"

  CLAW, ARCHER, REPAIRER, HACKER, TURRET, WALL, TERMINATOR, HANGAR = range(8)
  
  def tryToOperate (self, droid, x, y):
    if droid.attacksLeft > 0 and 0<=x<self.mapWidth and 0<=y<self.mapHeight and droid.range >= (abs(x-droid.x)+abs(y-droid.y)) and (x != droid.x or y != droid.y):
      for targetdroid in self.droids:
        if x == targetdroid.x and y == targetdroid.y and targetdroid.healthLeft>0:
          droid.operate(x,y)
          
  def tryToMove (self, droid, x, y):
    if droid.movementLeft > 0 and 0<=x<self.mapWidth and 0<=y<self.mapHeight:
      droid.move(x,y)

  ##This function is called once, before your first turn
  def init(self):
    random.seed()
    global keyList
    ymax = 0
    ymin = 20
    for droid in self.droids:
      if droid.variant == self.HANGAR:
        if droid.y < ymin:
          ymin = droid.y
        if droid.y > ymax:
          ymax = droid.y
    ymax = min(19,ymax+2)
    ymin = max(0,ymin+2)
    #spawnList = {}
    #Generate a dictionary of every tile that does not have a hanger
    for tile in self.tiles:
      string = str(tile.getX()) + '+' + str(tile.getY())
      spawnList[string] = tile   
      if self.playerID == 0 and tile.getX() < 2:
        string = str(tile.getX()) + '+' + str(tile.getY())
        restrictedList[string] = tile
      elif self.playerID == 1 and tile.getX() >=38:
        string = str(tile.getX()) + '+' + str(tile.getY())
        restrictedList[string] = tile
        
      if self.playerID == 0 and 5 < tile.getX() < 15 and ymin < tile.y < ymax:
        string = str(tile.getX()) + '+' + str(tile.getY())
        forwardList[string] = tile
      elif self.playerID == 1 and 25 < tile.getX() < 35 and ymin < tile.y < ymax:
        string = str(tile.getX()) + '+' + str(tile.getY())
        forwardList[string] = tile
        
      for droid in self.droids:
        if droid.getVariant() == self.HANGAR:
          string = str(droid.getX()) + '+' + str(droid.getY())
          if spawnList.has_key(string):
            del spawnList[string]
          if restrictedList.has_key(string):
            del restrictedList[string]
          if forwardList.has_key(string):
            del forwardList[string]

    #randomly select one of those tiles as a spawn
    #print self.playerID
    #print len(spawnList)
    
    #print len(keyList)
    

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    global keyList
    #print len(keyList)
    #Claw drop
    for droid in self.droids:
      if droid.variant == self.TURRET and droid.owner != self.playerID:
        if self.getTile(droid.x, droid.y).turnsUntilAssembled == 0:
          if self.players[self.playerID].scrapAmount >= self.modelVariants[self.CLAW].cost:
            self.players[self.playerID].orbitalDrop(droid.x, droid.y,self.CLAW)
          else:
           break
           
    ####################################################BLITZ
    blitzX = 0
    blitzY = 0
    for droid in self.droids:
      if droid.variant == self.HANGAR and droid.owner != self.playerID:
        blitzX = droid.x
        blitzY = droid.y
        break   
    if self.playerID == 0:
      blitzTime = 2*blitzX
    else:
      blitzTime = 2*(self.mapWidth-blitzX-1)
    
    if self.players[self.playerID].scrapAmount >= 140 and 500-self.turnNumber-blitzTime > 20:
      for i in range(blitzY):
        if self.players[self.playerID].scrapAmount >= 70:
          if str(blitzX)+"+"+str(blitzY-1-i) in spawnList:
            self.players[self.playerID].orbitalDrop(blitzX, blitzY-1-i, self.TERMINATOR)
        else:
            break
          
      for i in range(self.mapWidth-blitzY):
        if self.players[self.playerID].scrapAmount >= 70:
          if str(blitzX)+"+"+str(blitzY+1+i) in spawnList:
            self.players[self.playerID].orbitalDrop(blitzX, blitzY+1+i, self.TERMINATOR)
        else:
            break



    ####################################################################### Others
    outposts = 5
    turretcount = 0
    repaircount = 0
    enemytermcount = 0
    enemyothercount = 0
    clawcount = 0
    archercount = 0
    hackercount = 0
    termcount = 0

    for droid in self.droids:
      if droid.variant == self.TURRET and droid.owner == self.playerID:
        turretcount += 1
      if droid.variant == self.REPAIRER and droid.owner == self.playerID:
        repaircount += 1
      if droid.variant == self.CLAW and droid.owner == self.playerID:
        clawcount += 1
      if droid.variant == self.ARCHER and droid.owner == self.playerID:
        archercount += 1
      if droid.variant == self.TERMINATOR and droid.owner != self.playerID:
        enemytermcount += 1
      if (droid.variant == self.ARCHER or droid.variant == self.CLAW) and droid.owner != self.playerID:
        enemyothercount += 1
      if droid.variant == self.HACKER and droid.owner == self.playerID:
        hackercount += 1
      if droid.variant == self.TERMINATOR and droid.owner == self.playerID:
        termcount += 1        
    newunits = [] 
    
    if turretcount < 3 and self.players[self.playerID].scrapAmount >= self.modelVariants[self.TURRET].cost:
        newunits.append(self.TURRET)
    if termcount < (enemyothercount/3)+1:
        newunits.append(self.TERMINATOR)
    if clawcount < (enemyothercount*2/3)+3:
        newunits.append(self.CLAW)
    if hackercount < 3:
        newunits.append(self.HACKER)    
    if repaircount < 1:
        newunits.append(self.REPAIRER)
    if archercount < enemytermcount:
        newunits.append(self.ARCHER)
        
    for unit in newunits:
      if unit == self.TURRET:
        thislist = forwardList
      else:
        thislist = restrictedList
      keyList = thislist.keys()
      randomIndex = random.randint(0,len(keyList)-1)
      self.spawnX = thislist[keyList[randomIndex]].getX()
      self.spawnY = thislist[keyList[randomIndex]].getY()
      
      if self.players[self.playerID].scrapAmount >= self.modelVariants[unit].cost:
        if self.getTile(self.spawnX, self.spawnY).turnsUntilAssembled == 0:
          self.players[self.playerID].orbitalDrop(self.spawnX, self.spawnY, unit)
      else:
        break

    
    droidList = sorted(self.droids,key=lambda droids: droids.x)
    if self.playerID == 0:
      droidList.reverse()
    
    #for droid in self.droids:
    for droid in droidList:
      #print "Droid Start"
      if (droid.owner == self.playerID and droid.hackedTurnsLeft <= 0) or (droid.owner != self.playerID and droid.hackedTurnsLeft > 0):
        target = None
        #print "Target Start"
        if droid.variant == self.ARCHER:
          target = prioritizer.pickTargetArcher(droid,self)
        elif droid.variant == self.CLAW:
          target = prioritizer.pickTargetClaw(droid,self)
        elif droid.variant == self.TERMINATOR:
          target = prioritizer.pickTargetTerminator(droid,self)
        elif droid.variant == self.TURRET:
          target = prioritizer.pickTargetTurret(droid,self)
        elif droid.variant == self.HACKER:
          target = prioritizer.pickTargetHacker(droid,self)
        elif droid.variant == self.REPAIRER:
          target = prioritizer.pickTargetRepair(droid,self)
        #print "Target End"        
        
        if target != None and target != (-1,-1):
          #if (abs(target[0]-droid.x)+abs(target[1]-droid.y) > 20):
          #  target = (round((target[0]+droid.x)/2.0),round((target[1]+droid.y)/2.0))
          #print "Astar Start"
          path = ASTAR.aStar(ASTAR.makeGraph(self),(droid.x,droid.y),target,self.playerID)
          #print "Astar End"
          pathindex = 0
          self.tryToOperate(droid,target[0],target[1])
          self.tryToOperate(droid,target[0],target[1])
          #print "Move Start"
          while (droid.movementLeft > 0 and droid.attacksLeft > 0 and pathindex+1 < len(path)):
            pathindex += 1
            self.tryToMove(droid,path[pathindex][0],path[pathindex][1])
            self.tryToOperate(droid,target[0],target[1])

          seq = []
          seq.append(-1)
          seq.append(1)
          if self.playerID == 0:
            self.tryToMove(droid,droid.getX()+1,droid.getY())
            self.tryToMove(droid,droid.getX(),droid.getY() + random.choice(seq))
          else:
            self.tryToMove(droid,droid.getX()-1,droid.getY())
            self.tryToMove(droid,droid.getX(),droid.getY() + random.choice(seq))
          #print "Move End"
      #print "Droid End"                              
    return 1

  #returns a tile, or None if no tile
  def getTile(self, x ,y):
    for tile in self.tiles:
      if tile.x == x and tile.y == y:
        return tile
    return None

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
