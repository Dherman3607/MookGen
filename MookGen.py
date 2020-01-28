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
    NormalStats = ['Body','Agility','Reaction','Strength','Willpower','Logic','Charisma','Intuition']
    advancedStats = ['Magic','Resonance','Edge']
    for stat in advancedStats:
        if(inputStats[stat] == "-"):
            advancedStats.remove(stat)

    while SpendablePoints > 0:
        increaseStat = random.choice(NormalStats)
        if(inputStats[increaseStat]< maxStats[increaseStat]):
            inputStats[increaseStat]+=1
            SpendablePoints -= 1
        else:
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
def determineSpecials(Mook,SkillsInputFile):
    specialtyStats = Mook['specialtyStats']
    Skills = Mook['Skills']
    print(specialtyStats)
    if('Aspected' in Stats['Special']):
        #an aspected mage can only use one of the three mage skills, to be determined randomly.
        ChosenSkillSet = random.choice(list(SkillsInputFile['Specials']['Magic']))
        Skills[ChosenSkillSet] = {}
        Skills[ChosenSkillSet].update(SkillsInputFile['Specials']['Magic'][ChosenSkillSet])
        if('SkillGroup' in specialtyStats):
            for skill in Skills[ChosenSkillSet]:
                Skills[ChosenSkillSet][skill] = specialtyStats['SkillGroup']
        spellSelections = []
        spellOptions = mook['specialtyStats'] * 2
        # spellSelections = selectSpells(spellOptions,"magician")
        # Skills['spells'] = spellSelections

    elif ('Technomancer' in Stats['Special']):
        print('Technomancer')

    elif('Mystic Adept') in Stats['Special']:
        print('Mystic Adept')

    elif('Magician' in Stats['Special']):
        print('Magician')
    elif('Adept' in Stats['Special']):
        print('Adept')

    print(Skills)
    return Skills
def selectSpells(OptionsCount,type):
    #stub for later, this is definitely going to be in a file, but just a proof of concept for the other stats at the moment.
    spells = ['Toxic wave','punch']
    return spells
def addSkills(skillPointsDict,Skills):

    removableSkillgroups = []
    #set up the list of skills that can be increased. When we process skill groups, we'll remove individual skills from this list.
    SkillList = []
    skillGroups = []
    #aspected magicans, adepts, and technomancers all have different rules for Skills
    #before assigning groups and skill points, those need to be configured.
    for skillGroup in Skills:
        skillGroups.append(skillGroup)
        for skill in Skills[skillGroup]:
            SkillList.append(skill)


    while skillPointsDict['groups'] > 0:
        increasedSkills = random.choice(skillGroups)
        if(increasedSkills not in removableSkillgroups):
            removableSkillgroups.append(increasedSkills)
        for skill in Skills[increasedSkills]:
            Skills[increasedSkills][skill] +=1
        skillPointsDict['groups'] -=1


    if(removableSkillgroups):
        for group in removableSkillgroups:
            skillGroups.remove(group)

    while skillPointsDict['points'] > 0:
        randomGroup = random.choice(skillGroups)
        randomSkill = random.choice(list(Skills[randomGroup]))
        print(randomSkill,Skills[randomGroup][randomSkill])
        if (Skills[randomGroup][randomSkill]< 5):
            Skills[randomGroup][randomSkill] +=1
            skillPointsDict['points'] -=1
        else:
            pass
    return Skills

def MakeEasyMook():
    sumToTen = 10
    Priorities = ReadJson('data\\Priorities.json')
    metatypeStats = ReadJson('data\\metatypes.json')
    boughtValues = ReadJson('data\\boughtValues.json')
    #SkillPointAllocations = ReadJson('data\\SkillPoints.json')
    SpecialStaters = ReadJson('data\\SpecialStats.json')
    PointCost = ReadJson('data\\pointCosts.json')
    SkillsInputFile = ReadJson('data\\skills.json')
    Skills = SkillsInputFile['Skills']
    Stats = {}
    specialtyStats = {}
    Mook = {
    "Metatype":"",
    "Priorities":{},
    "specialtyStats":{},
    "Attributes":{},
    "Skills":{},
    "Spells":[],
    "Gear":[]
    }

    for priority in Priorities:
        if sumToTen > 0:
            value =  (random.randrange(0,4))
            sumToTen -= value
            Priorities[priority] = value

    #Creating the actual character - Probably turned into a function? eventually?

    #the poor man's way to do this. Leaving these 2 lines as an example of setting it up
    #and then doing it better, below
    #possibleMeta = boughtValues['metatype'][str(Priorities['metatype'])]
    #metatype = random.choice(list(possibleMeta.keys()))

    metatype = random.choice(list(boughtValues['metatype'][str(Priorities['metatype'])].keys()))
    Mook['Metatype'] = metatype
    print(Priorities)
    Mook['Priorities'].update(Priorities)


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
        Mook['specialtyStats'] = SpecialStaters[str(Priorities['Magic'])][specialty]
        #print(specialtyStats)
        if('Magic' in Mook['specialtyStats']):
            Stats['Magic'] = Mook['specialtyStats']
        else:
            Stats['Resonance'] = specialtyStats['Resonance']
        if(Stats["Special"] =='None'):
            Stats["Special"] = specialty
        else:
             Stats["Special"] +=  " " + specialty


    #set up and calculate attributes
    SpendableSpecialPoints = boughtValues['metatype'][str(Priorities['metatype'])][metatype]['Specials']
    Stats = addAttributes(Stats,maxStats,attributePoints,SpendableSpecialPoints)
    Mook['Attributes'].update(Stats)
    #setup and calculate skill points
    spendableSkillpoints =PointCost['skillpoints'][str(Priorities['Skills'])]

    skills = determineSpecials(Mook,SkillsInputFile)
    skills = addSkills(spendableSkillpoints,Skills)
    Mook['Skills'].update(skills)

    print(Mook)
    # print('at the end of assigning attribute points, the stat array is:')
    # print(Stats)
    # print(Skills)


#main loop
root = Tk()
root.title("MookGen")
root.minsize(300,300)

EasyMook = Button(root, text ="Easy Mook", command = MakeEasyMook)
EasyMook.place(x=50, y=50)

root.mainloop()
