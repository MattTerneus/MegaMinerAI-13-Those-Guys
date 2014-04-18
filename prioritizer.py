import AI
import random

CLAW, ARCHER, REPAIRER, HACKER, TURRET, WALL, TERMINATOR, HANGAR = range(8)

def findDroids(x,y,radius,team,droids):
    found = []
    for droid in droids:
        if ((droid.owner == team and droid.hackedTurnsLeft <= 0) or (droid.owner != team and droid.hackedTurnsLeft > 0)) and (radius >= (abs(x-droid.x)+abs(y-droid.y)))and droid.healthLeft > 0:
            found.append(((abs(x-droid.x)+abs(y-droid.y)),droid))
    found.sort()
    retlist = []
    for _,i in found:
        retlist.append(i)        
    return retlist
    

def pickTargetClaw(droid,AI):
    targetDroids = findDroids(droid.x,droid.y,5,1-AI.playerID,AI.droids)
    if (len(targetDroids) > 0):
        for targetDroid in targetDroids:
            if targetDroid.variant == ARCHER:
                return targetDroid.x,targetDroid.y
        return targetDroids[0].x,targetDroids[0].y
    else:
        targetDroids = findDroids(droid.x,droid.y,AI.getMapHeight()+AI.getMapWidth(),1-AI.playerID,AI.droids)
        if (len(targetDroids) > 0):
            return targetDroids[0].x,targetDroids[0].y
        else:
            #return droid.x+ 4*(-2*AI.playerID+1),droid.y
            return AI.getMapWidth()/2, AI.getMapHeight()/2
    
def pickTargetArcher(droid,AI):
    targetDroids = findDroids(droid.x,droid.y,5,1-AI.playerID,AI.droids)
    if (len(targetDroids) > 0):
        for targetDroid in targetDroids:
            if targetDroid.variant == HACKER:
                return targetDroid.x,targetDroid.y
        lowest = targetDroids[0]
        lowestrating = targetDroids[0].armor*targetDroids[0].healthLeft
        for targetDroid in targetDroids:
            if lowestrating > targetDroid.armor*targetDroid.healthLeft:
                lowest = targetDroid
                lowestrating = targetDroid.armor*targetDroid.healthLeft
        return lowest.x,lowest.y
    else:
        targetDroids = findDroids(droid.x,droid.y,AI.getMapHeight()+AI.getMapWidth(),1-AI.playerID,AI.droids)
        # if (len(targetDroids) > 0):
            # for targetDroid in targetDroids:
                # if (targetDroid.variant == TERMINATOR) and ((droid.owner == 0 and  targetDroid.x > droid.x) or (droid.owner == 1 and  targetDroid.x < droid.x)):
                    # return targetDroid.x + 2*(2*AI.playerID-1),targetDroid.y
            # return AI.getMapWidth()/2, AI.getMapHeight()/2
        if (len(targetDroids) > 0):
            return targetDroids[0].x,targetDroids[0].y
        else:
            return AI.getMapWidth()/2, AI.getMapHeight()/2

def pickTargetTerminator(droid,AI):
    targetDroids = findDroids(droid.x,droid.y,2,1-AI.playerID,AI.droids)
    if (len(targetDroids) > 0):
        for targetDroid in targetDroids:
            if targetDroid.variant == TURRET:
                return targetDroid.x,targetDroid.y
        for targetDroid in targetDroids:
            if targetDroid.variant == HANGAR:
                return targetDroid.x,targetDroid.y
        for targetDroid in targetDroids:
            if targetDroid.variant == HACKER:
                return targetDroid.x,targetDroid.y
        lowest = targetDroids[0]
        lowestrating = targetDroids[0].armor*targetDroids[0].healthLeft
        for targetDroid in targetDroids:
            if lowestrating > targetDroid.armor*targetDroid.healthLeft:
                lowest = targetDroid
                lowestrating = targetDroid.armor*targetDroid.healthLeft
        return lowest.x,lowest.y
    else:
        targetDroids = findDroids(droid.x,droid.y,AI.getMapHeight()+AI.getMapWidth(),1-AI.playerID,AI.droids)
        if (len(targetDroids) > 0):
            for targetDroid in targetDroids:
                if targetDroid.variant == HANGAR:
                    return targetDroid.x,targetDroid.y
            
            return targetDroids[0].x,targetDroids[0].y
        else:
            #return droid.x+ 4*(-2*AI.playerID+1),droid.y
            return AI.getMapWidth()/2, AI.getMapHeight()/2

def pickTargetRepair(droid,AI):
  possibleDroids = findDroids(droid.x,droid.y,4,AI.playerID,AI.droids)
  for targetDroid in possibleDroids:
    if targetDroid.armor != targetDroid.maxArmor and targetDroid.variant == TURRET:
      return targetDroid.x,targetDroid.y
  for targetDroid in possibleDroids:
    if targetDroid.armor != targetDroid.maxArmor and targetDroid.variant == TERMINATOR:
      return targetDroid.x,targetDroid.y  
  #for targetDroid in possibleDroids:
   # if targetDroid.armor != targetDroid.maxArmor:
    #  return targetDroid.x,targetDroid.y
  possibleDroids = findDroids(droid.x,droid.y,AI.getMapHeight()+AI.getMapWidth(),AI.playerID,AI.droids)
  for targetDroid in possibleDroids:
    if targetDroid.armor != targetDroid.maxArmor and targetDroid.variant == TURRET:
      return targetDroid.x,targetDroid.y
  for targetDroid in possibleDroids:
    if targetDroid.armor != targetDroid.maxArmor and targetDroid.variant == TERMINATOR:
      return targetDroid.x,targetDroid.y
  #for targetDroid in possibleDroids:
  #  if targetDroid.armor != targetDroid.maxArmor:
  #    return targetDroid.x,targetDroid.y
  for targetDroid in possibleDroids:
    if targetDroid.armor != targetDroid.maxArmor:
      return targetDroid.x,targetDroid.y
  return -1,-1    

def pickTargetHacker(droid,AI):
  possibleDroids = findDroids(droid.x,droid.y,4,1-AI.playerID,AI.droids)
  for targetDroid in possibleDroids:
    if targetDroid.hackedTurnsLeft == 0 and targetDroid.variant == CLAW:
      return targetDroid.x,targetDroid.y  
  for targetDroid in possibleDroids:
    if targetDroid.hackedTurnsLeft == 0 and targetDroid.variant == TERMINATOR:
      return targetDroid.x,targetDroid.y
  for targetDroid in possibleDroids:
    if targetDroid.hackedTurnsLeft == 0 and (targetDroid.variant != HANGAR and targetDroid.variant != WALL and targetDroid.variant != TURRET):
      return targetDroid.x,targetDroid.y      
  possibleDroids = findDroids(droid.x,droid.y,AI.getMapHeight()+AI.getMapWidth(),1-AI.playerID,AI.droids)
  for targetDroid in possibleDroids:
    if targetDroid.hackedTurnsLeft == 0 and targetDroid.variant == CLAW:
      return targetDroid.x,targetDroid.y  
  for targetDroid in possibleDroids:
    if targetDroid.hackedTurnsLeft == 0 and targetDroid.variant == TERMINATOR:
      return targetDroid.x,targetDroid.y
  for targetDroid in possibleDroids:
    if targetDroid.hackedTurnsLeft == 0 and (targetDroid.variant != HANGAR and targetDroid.variant != WALL and targetDroid.variant != TURRET):
      return targetDroid.x,targetDroid.y
  return -1,-1
def pickTargetTurret(droid,AI):
  highestAttack = -1
  x = -1
  y = -1
  for targetDroid in findDroids(droid.x,droid.y,3,1-AI.playerID,AI.droids):
    if targetDroid.attack > highestAttack:
      highestAttack = targetDroid.attack
      x = targetDroid.x
      y = targetDroid.y
  return x,y
