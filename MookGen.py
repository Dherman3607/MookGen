#imports
from tkinter import *
from tkinter import messagebox
import random
import json


#vars:
Stats = {}
Stats = {

    'Body':0,
    'Agility':0,
    'Reaction':0,
    'Strength':0,
    'Willpower':0,
    'Logic':0,
    'Intuition':0,
    'Charisma':0,
    'Edge':0,
    'Magic' : '-',
    'Resonance' : '-',
    'Initiative': 0

}
maxStats = {}


def ReadJson(Inputfile):

    with open(Inputfile,'r') as f:
        return json.load(f)

def  addAttributes(inputStats,maxStats,SpendablePoints,SpendableSpecialPoints):
    print('inside')
    print(inputStats,SpendablePoints,SpendableSpecialPoints)
    NormalStats = ['Body','Agility','Reaction','Strength','Willpower','Logic','Charisma','Intuition']
    advancedStats = ['Magic','Resonance','Edge']
    for stat in advancedStats:
        print(stat)
        if(inputStats[stat] == "-"):
            print("character doesn't have this stat, remove")
            advancedStats.remove(stat)

    while SpendablePoints > 0:
        increaseStat = random.choice(NormalStats)
        if(inputStats[increaseStat]< maxStats[increaseStat]):
            print('increasing stat?')
            inputStats[increaseStat]+=1
            SpendablePoints -= 1
        else:
            print("this stat is at it's max?")
            NormalStats.remove(increaseStat)

    while SpendableSpecialPoints > 0:
        if(advancedStats):
            increaseStat = random.choice(advancedStats)
            if(inputStats[increaseStat] == "-"):
                #this attribute can't be bought on this chracter, remove it
                advancedStats.remove(increaseStat)
            else:
                if(inputStats[increaseStat] < maxStats[increaseStat]):
                    inputStats[increaseStat] += 1
                    SpendableSpecialPoints -= 1
                else:
                    advancedStats.remove(increaseStat)
        else:
            break
    inputStats['Initiative'] = inputStats['Reaction'] + inputStats['Intuition']
    return inputStats

def addSkills(skillPointsDict,Skills):
    removableSkillgroups = []
    #set up the list of skills that can be increased. When we process skill groups, we'll remove individual skills from this list.
    SkillList = []
    skillGroups = []
    for skillGroup in Skills['Skills']:
        skillGroups.append(skillGroup)
        for skill in Skills['Skills'][skillGroup]:
            SkillList.append(skill)


    while skillPointsDict['groups'] > 0:
        increasedSkills = random.choice(skillGroups)
        print(increasedSkills)
        if(increasedSkills not in removableSkillgroups):
            removableSkillgroups.append(increasedSkills)
        for skill in Skills['Skills'][increasedSkills]:
            Skills['Skills'][increasedSkills][skill] +=1
        skillPointsDict['groups'] -=1


    if(removableSkillgroups):
        for group in removableSkillgroups:
            skillGroups.remove(group)

    while skillPointsDict['points'] > 0:
        print("choosing skills")
        randomGroup = random.choice(skillGroups)
        #print(Skills['Skills'][randomGroup])
        randomSkill = random.choice(list(Skills['Skills'][randomGroup]))
        if (Skills['Skills'][randomGroup][randomSkill]< 5):
            Skills['Skills'][randomGroup][randomSkill] +=1
            skillPointsDict['points'] -=1
        else:
            pass

    print(Skills)
    return Skills

def MakeEasyMook():
    sumToTen = 10
    Priorities = ReadJson('data\\Priorities.json')
    metatypeStats = ReadJson('data\\metatypes.json')
    boughtValues = ReadJson('data\\boughtValues.json')
    #SkillPointAllocations = ReadJson('data\\SkillPoints.json')
    SpecialStaters = ReadJson('data\\SpecialStats.json')
    PointCost = ReadJson('data\\pointCosts.json')
    Skills = ReadJson('data\\skills.json')
    Stats = {}

    for priority in Priorities:
        if sumToTen > 0:
            value =  (random.randrange(0,4))
            sumToTen -= value
            Priorities[priority] = value


    print("the priorities are " + str(Priorities))

    #Creating the actual character - Probably turned into a function? eventually?

    #the poor man's way to do this. Leaving these 2 lines as an example of setting it up
    #and then doing it better, below
    #possibleMeta = boughtValues['metatype'][str(Priorities['metatype'])]
    #metatype = random.choice(list(possibleMeta.keys()))

    metatype = random.choice(list(boughtValues['metatype'][str(Priorities['metatype'])].keys()))


    for stat in metatypeStats[metatype]:

        if stat == 'Special':
            Stats[stat] = metatypeStats[metatype][stat]
        else:
            Stats[stat] = metatypeStats[metatype][stat]['starting']
            maxStats[stat] = metatypeStats[metatype][stat]['max']


    attributePoints = PointCost['attributes'][str(Priorities['attributes'])]
    #is this guy magical, or a technomancer?
    if(Priorities['Magic'] >0 ):

        specialty = random.choice(list(SpecialStaters[str(Priorities['Magic'])]))
        specialtyStats = SpecialStaters[str(Priorities['Magic'])][specialty]

        if('Magic' in specialtyStats):
            Stats['Magic'] = specialtyStats['Magic']
        else:
            Stats['Resonance'] = specialtyStats['Resonance']
        if(Stats["Special"] =='None'):
            Stats["Special"] = specialty
        else:
             Stats["Special"] +=  " " + specialty


    #set up and calculate attributes
    SpendableSpecialPoints = boughtValues['metatype'][str(Priorities['metatype'])][metatype]['Specials']
    Stats = addAttributes(Stats,maxStats,attributePoints,SpendableSpecialPoints)
    #setup and calculate skill points
    spendableSkillpoints =PointCost['skillpoints'][str(Priorities['Skills'])]
    if(Stats['Magic'] == "-"):
        Skills['Skills'].pop('Sorcery')
        Skills['Skills'].pop('Conjuring')
        Skills['Skills'].pop('Enchanting')
    if(Stats['Resonance'] == '-'):
        Skills['Skills'].pop('Tasking')

    skills = addSkills(spendableSkillpoints,Skills)


    print('at the end of assigning attribute points, the stat array is:')
    print(Stats)

    print()


#main loop
root = Tk()
root.title("hello")
root.minsize(300,300)

EasyMook = Button(root, text ="Easy Mook", command = MakeEasyMook)
EasyMook.place(x=50, y=50)

root.mainloop()
