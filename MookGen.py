#imports
from tkinter import *
from tkinter import messagebox
import random
import json


#vars:
stats = {}
stats = {

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


def Read_Json(Inputfile):

    with open(Inputfile,'r') as f:
        return json.load(f)

def Add_Attributes(inputStats,maxStats,SpendablePoints,spendableSpecialPoints):
    #Normal states are those that 1) every character has, and 2) are increased with regular attribute points (SpendablePoints)
    #advanced stats are either not available to all characters (magic/resonance) or use other points to upgrade them (all of them) (spendableSpecialPoints)
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

    while spendableSpecialPoints > 0:
        if(advancedStats):
            increaseStat = random.choice(advancedStats)
            if(inputStats[increaseStat] == "-"):
                #this attribute can't be bought on this chracter, remove it
                advancedStats.remove(increaseStat)
            else:
                if(inputStats[increaseStat] < maxStats[increaseStat]):
                    inputStats[increaseStat] += 1
                    spendableSpecialPoints -= 1
                else:
                    advancedStats.remove(increaseStat)
        else:
            break
    inputStats['Initiative'] = inputStats['Reaction'] + inputStats['Intuition']
    return inputStats

def Determine_Specials(Mook,SkillsInputFile):
    specialtyStats = Mook['specialtyStats']
    Skills = Mook['Skills']
    stats = Mook['Attributes']
    if('Aspected' in stats['Special']):
        #an aspected mage can only use one of the three mage skills, to be determined randomly.
        ChosenSkillSet = random.choice(list(SkillsInputFile['Specials']['Magic']))
        Skills[ChosenSkillSet] = {}
        Skills[ChosenSkillSet].update(SkillsInputFile['Specials']['Magic'][ChosenSkillSet])
        if('SkillGroup' in specialtyStats):
            for skill in Skills[ChosenSkillSet]:
                Skills[ChosenSkillSet][skill] = specialtyStats['SkillGroup']
        spellSelections = []
        spellOptions = Mook['specialtyStats']['Magic'] * 2
        spellSelections = Select_Spells(spellOptions,"magician")
        Mook['Spells'] = spellSelections

    elif('Technomancer' in stats['Special']):
        print('Technomancer')

    elif('Mystic Adept') in stats['Special']:
        print('Mystic Adept')

    elif('Magician' in stats['Special']):
        print('Magician')
        SkillCount = Mook['specialtyStats']['SkillCount']
        for skillGroup in SkillsInputFile['Specials']['Magic']:
            print(skillGroup)
            Skills[skillGroup] = {}
            Skills[skillGroup].update(SkillsInputFile['Specials']['Magic'][skillGroup])
        while SkillCount > 0:
            randomGroup = random.choice(list(SkillsInputFile['Specials']['Magic']))
            randomSkill = random.choice(list(SkillsInputFile['Specials']['Magic'][randomGroup]))
            Mook['Skills'][randomGroup][randomSkill] = specialtyStats['SkillRating']
            print(randomSkill)
            SkillCount -=1
        spellOptions = Mook['specialtyStats']['Spells']
        if spellOptions != 0:
            spellSelections = Select_Spells(spellOptions,"magician")
            Mook['Spells'] = spellSelections


    elif('Adept' in stats['Special']):
        print('Adept')
        powerPoints = Mook['Attributes']['Magic']*2
        Select_Adept_Powers(powerPoints)
    return Skills

def Select_Adept_Powers(powerPoints):
    adeptPowers = Read_Json('data\\AdeptPowers.json')
    selectedPowersList = []
    adeptList = []
    selectedPowers = {}

    for key in adeptPowers:
        adeptList.append(key)

    while adeptList:
        if powerPoints >0:
            randomPower = random.choice(list(adeptList))


            if(adeptPowers[randomPower]['Cost'] < powerPoints):
                if randomPower not in selectedPowers:
                    selectedPowers[randomPower] = adeptPowers[randomPower]
                    selectedPowers[randomPower]['Current Rank'] = 1
                    powerPoints -= adeptPowers[randomPower]['Cost']
                    adeptList.extend([randomPower]*10)
                elif selectedPowers[randomPower]['Current Rank'] < selectedPowers[randomPower]['Max']:
                        selectedPowers[randomPower]['Current Rank'] +=1
                        powerPoints -= adeptPowers[randomPower]['Cost']
                else:
                    adeptList.remove(randomPower)

            else:
                #print('removing ' + randomPower)
                adeptList.remove(randomPower)

    print(selectedPowersList)


    print(selectedPowers)


def Select_Spells(OptionsCount,type):
    #stub for later, this is definitely going to be in a file, but just a proof of concept for the other stats at the moment.
    spells = []
    spellList = Read_Json('data\\Spells.json')
    while OptionsCount > 0:
        spells.append(random.choice(list(spellList[random.choice(list(spellList))])))
        OptionsCount -= 1
    return spells

def Add_Skills(skillPointsDict,Skills):

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
        if (Skills[randomGroup][randomSkill]< 5):
            Skills[randomGroup][randomSkill] +=1
            skillPointsDict['points'] -=1
        else:
            pass
    return Skills

def Make_Easy_Mook():
    sumToTen = 10
    priorities = Read_Json('data\\priorities.json')
    metatypeStats = Read_Json('data\\metatypes.json')
    boughtValues = Read_Json('data\\boughtValues.json')
    #SkillPointAllocations = Read_Json('data\\SkillPoints.json')
    SpecialStates = Read_Json('data\\SpecialStats.json')
    PointCost = Read_Json('data\\pointCosts.json')
    SkillsInputFile = Read_Json('data\\skills.json')
    Skills = SkillsInputFile['Skills']
    stats = {}
    specialtyStats = {}
    Mook = {
    "Metatype":"",
    "priorities":{},
    "specialtyStats":{},
    "Attributes":{},
    "Adept":{},
    "Skills":{},
    "Spells":[],
    "Gear":[]
    }

    for priority in priorities:
        if sumToTen > 0:
            value =  (random.randrange(0,4))
            sumToTen -= value
            priorities[priority] = value

    #Creating the actual character - Probably turned into a function? eventually?

    #the poor man's way to do this. Leaving these 2 lines as an example of setting it up
    #and then doing it better, below
    #possibleMeta = boughtValues['metatype'][str(priorities['metatype'])]
    #metatype = random.choice(list(possibleMeta.keys()))

    metatype = random.choice(list(boughtValues['metatype'][str(priorities['metatype'])].keys()))
    Mook['Metatype'] = metatype
    Mook['priorities'].update(priorities)


    for stat in metatypeStats[metatype]:

        if stat == 'Special':
            stats[stat] = metatypeStats[metatype][stat]
        else:
            stats[stat] = metatypeStats[metatype][stat]['starting']
            maxStats[stat] = metatypeStats[metatype][stat]['max']


    attributePoints = PointCost['attributes'][str(priorities['attributes'])]
    #is this guy magical, or a technomancer?
    if(priorities['Magic'] >0 ):

        specialty = random.choice(list(SpecialStates[str(priorities['Magic'])]))
        Mook['specialtyStats'] = SpecialStates[str(priorities['Magic'])][specialty]
        if('Magic' in Mook['specialtyStats']):
            stats['Magic'] = Mook['specialtyStats']['Magic']
        else:
            stats['Resonance'] =  Mook['specialtyStats']['Resonance']
        if(stats["Special"] =='None'):
            stats["Special"] = specialty
        else:
             stats["Special"] +=  " " + specialty


    #set up and calculate attributes
    spendableSpecialPoints = boughtValues['metatype'][str(priorities['metatype'])][metatype]['Specials']
    stats = Add_Attributes(stats,maxStats,attributePoints,spendableSpecialPoints)
    Mook['Attributes'].update(stats)


    #setup and calculate skill points
    spendableSkillpoints =PointCost['skillpoints'][str(priorities['Skills'])]
    skills = Determine_Specials(Mook,SkillsInputFile)
    skills = Add_Skills(spendableSkillpoints,Skills)
    Mook['Skills'].update(skills)


    print('The mook is ')
    print(Mook)



#main loop
root = Tk()
root.title("MookGen")
root.minsize(300,300)

EasyMook = Button(root, text ="Easy Mook", command = Make_Easy_Mook)
EasyMook.place(x=50, y=50)

root.mainloop()
