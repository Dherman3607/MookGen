#imports
from tkinter import *
from tkinter import messagebox
import random
import json


#vars:
stats = {}



maxStats = {}
class Utility:
    def Read_Json(Inputfile):

        with open(Inputfile,'r') as f:
            return json.load(f)
class Character:
    def Add_Skills(skillPointsDict,Skills):

        removableSkillgroups = []
        # set up the list of skills that can be increased. When we process skill
        # groups, we'll remove individual skills from this list.
        SkillList = []
        skillGroups = []
        #aspected magicans, adepts, and technomancers all have different rules for
        # Skills before assigning groups and skill points, those need to be configured.
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

    priorities = Utility.Read_Json('data\\priorities.json')
    metatypeStats = Utility.Read_Json('data\\metatypes.json')
    boughtValues = Utility.Read_Json('data\\boughtValues.json')
    #SkillPointAllocations = Utility.Read_Json('data\\SkillPoints.json')
    SpecialStates = Utility.Read_Json('data\\SpecialStats.json')
    PointCost = Utility.Read_Json('data\\pointCosts.json')
    SkillsInputFile = Utility.Read_Json('data\\skills.json')
    Skills = SkillsInputFile['Skills']

    def __init__(self, priorities=priorities,
    boughtValues = boughtValues,metatypeStats = metatypeStats,
    PointCost = PointCost, SpecialStates = SpecialStates):
        #not all mooks will have adept, spells, or adept powers but for now they
        #can be left here as the first pass in conversion.

        self.stats = {
            'Body':{},
            'Agility':{},
            'Reaction':{},
            'Strength':{},
            'Willpower':{},
            'Logic':{},
            'Intuition':{},
            'Charisma':{},
            }
        self.Mook = {
        "Metatype":"",
        "priorities":{},
        "specialtyStats":{
        'Edge':{}
        },
        "Attributes":{},
        "Limits":{},
        "Adept":{},
        "Skills":{},
        "Spells":[],
        "Adept Powers":{},
        "Gear":[]
        }
        #self.specialtyStats = {}


        self.metatype = random.choice(list(boughtValues['metatype'][str(priorities
                    ['metatype'])].keys()))
        self.Mook['Metatype'] = self.metatype
        self.Mook['priorities'].update(priorities)

        for stat in self.stats:
            if stat != 'Specialty':
                self.stats[stat] = metatypeStats[self.metatype][stat]

        attributePoints = PointCost['attributes'][str(priorities['attributes'])]

#    def add_base_attributes(inputStats,maxStats,spendable_points,spendableSpecialPoints):
    def add_base_attributes(self):
        # Normal states are those that 1) every character has, and 2) are increased
        # with regular attribute points (spendable_points)
        #advanced stats are either not available to all characters (magic/resonance)
        # or use other points to upgrade them (all of them) (spendableSpecialPoints)
        NormalStats = ['Body','Agility','Reaction','Strength','Willpower','Logic',
                        'Charisma','Intuition']
        advancedStats = ['Magic','Resonance','Edge']
        inputStats = {}
        # for stat in advancedStats:
        #     if(inputStats[stat] == "-"):
        #         advancedStats.remove(stat)
        for stat in self.stats:
            inputStats[stat] = stat
            inputStats[stat] = self.stats[stat]['starting']

    # #setup and calculate skill points
    # spendableSkillpoints =PointCost['skillpoints'][str(priorities['Skills'])]
    # skills = determine_specials(Mook,SkillsInputFile)
    # skills = Add_Skills(spendableSkillpoints,Skills)
    # Mook['Skills'].update(skills)

        print("point cost " + str(self.PointCost))
        print(self.priorities)
        spendable_points = self.PointCost['skillpoints'][str(self.priorities['Skills'])]
        # while spendable_points > 0:
        #     increaseStat = random.choice(NormalStats)
        #     if(inputStats[increaseStat]< maxStats[increaseStat]):
        #         inputStats[increaseStat]+=1
        #         spendable_points -= 1
        #     else:
        #         NormalStats.remove(increaseStat)


        inputStats['Initiative'] = inputStats['Reaction'] + inputStats['Intuition']
        return inputStats
    def add_advanced_attributes(self):
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
class Adept(Character):
    '''Define the archetype of an dept, a character that has power points
    and special abilities.'''
    def __init__(self,priorities):
        super().__init__()
        super().add_base_attributes()
        #self.'adept powers' = select_adept_powers()
        #print(Character.__dict__)
        return
    #print(Character.stats.__dict__)

    # elif('Adept' in stats['Special']):
    #     print('Adept')
    #     power_points = Mook['Attributes']['Magic']*2
    #     Mook['Adept Powers'] = select_adept_powers(power_points)
    # return Skills

    def check_pre_req(adept_powers,random_power):
        # this random_power should be the pre-req to the previous one. If it doesn't have a pre-req,
        # we can return that as the the new skill to add
        #print(adept_powers)
        if('none' in adept_powers[random_power]['Prereq']):
            return adept_powers[random_power]['Prereq']
        else:
            random_power = adept_powers[random_power]['Prereq']
            check_pre_req(adept_powers,random_power)
        pass

    def add_power(adept_powers,random_power,power_points,selected_powers,adept_list):
        if(adept_powers[random_power]['Cost'] < power_points):
            if random_power not in selected_powers:
                selected_powers[random_power] = adept_powers[random_power]
                selected_powers[random_power]['Current Rank'] = 1
                power_points -= adept_powers[random_power]['Cost']
                adept_list.extend([random_power]*10)
            elif selected_powers[random_power]['Current Rank'] < (selected_powers
                [random_power]['Max']):
                    selected_powers[random_power]['Current Rank'] +=1
                    power_points -= adept_powers[random_power]['Cost']
            else:
                adept_list.remove(random_power)

        else:
            #print('removing ' + random_power)
            adept_list.remove(random_power)
        return adept_list,selected_powers

    def select_adept_powers(power_points):
        adept_powers = Read_Json('data\\AdeptPowers.json')
        selectedPowersList = []
        adept_list = []
        selected_powers = {}

        for key in adept_powers:
            adept_list.append(key)

        while adept_list:
            if power_points >0:
                random_power = random.choice(list(adept_list))
                #print(adept_powers[random_power]['Prereq'])
                if('none' in adept_powers[random_power]['Prereq']):
                    added_power = add_power(adept_powers,random_power,power_points,
                                            selected_powers,adept_list)
                    adept_list = added_power[0]
                    selected_powers = added_power[1]
                else:
                    random_power = adept_powers[random_power]['Prereq']
                    random_power = check_pre_req(adept_powers,random_power)
                    break
        return selected_powers

class Magician(Character):
    # #elif('Magician' in stats['Special']):
    # print('Magician')
    # SkillCount = Mook['specialtyStats']['SkillCount']
    # for skillGroup in SkillsInputFile['Specials']['Magic']:
    #     print(skillGroup)
    #     Skills[skillGroup] = {}
    #     Skills[skillGroup].update(SkillsInputFile['Specials']['Magic'][skillGroup])
    # while SkillCount > 0:
    #     randomGroup = random.choice(list(SkillsInputFile['Specials']['Magic']))
    #     randomSkill = random.choice(list(SkillsInputFile['Specials']['Magic'][randomGroup]))
    #     Mook['Skills'][randomGroup][randomSkill] = specialtyStats['SkillRating']
    #     print(randomSkill)
    #     SkillCount -=1
    # spellOptions = Mook['specialtyStats']['Spells']
    # if spellOptions != 0:
    #     spellSelections = Select_Spells(spellOptions,"magician")
    #     Mook['Spells'] = spellSelections
    #
    # def Select_Spells(OptionsCount,type):
    #     #stub for later, this is definitely going to be in a file, but just a proof
    #     # of concept for the other stats at the moment.
    #     spells = []
    #     spellList = Read_Json('data\\Spells.json')
    #     while OptionsCount > 0:
    #         spells.append(random.choice(list(spellList[random.choice(list(spellList))])))
    #         OptionsCount -= 1
    #     return spells
    pass
class Mystic_Adept(Character):
    pass
class Technomancer(Character):
    pass
class Aspected_Mage(Character):
    pass

def determine_limits():
    pass
def determine_specials(Mook,SkillsInputFile):
    specialtyStats = Mook['specialtyStats']
    Skills = Mook['Skills']
    stats = Mook['Attributes']
    if('Aspected' in stats['Special']):
        # an aspected mage can only use one of the three mage skills,
        # to be determined randomly.
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

def Make_Easy_Mook():
    priorities = Utility.Read_Json('data\\priorities.json')
    SpecialStates = Utility.Read_Json('data\\SpecialStats.json')
    sumToTen = 10
    for priority in priorities:
        if sumToTen > 0:
            value =  (random.randrange(0,4))
            sumToTen -= value
            priorities[priority] = value
    print(priorities)

    #is this guy magical, or a technomancer?
    if(priorities['Magic'] >0 ):

        specialty = random.choice(list(SpecialStates[str(priorities['Magic'])]))
        if(specialty == 'Technomancer'):
            mook = Technomancer()
        elif(specialty == "Aspected Magician"):
            mook = Aspected_Mage()
        elif(specialty == "Adept"):
            mook = Adept(priorities)
            print(mook.__dict__)
            print('adept')
        elif(specialty == "Magician"):
            mook = Magician()
    else:
        mook = Character()
        print('regular person')
        print(mook.__dict__)
        # Mook['specialtyStats'] = SpecialStates[str(priorities['Magic'])][specialty]
        # if('Magic' in Mook['specialtyStats']):
        #     stats['Magic'] = Mook['specialtyStats']['Magic']
        # else:
        #     stats['Resonance'] =  Mook['specialtyStats']['Resonance']
        # if(stats["Special"] =='None'):
        #     stats["Special"] = specialty
        # else:
        #      stats["Special"] +=  " " + specialty
        #

    #set up and calculate attributes
    # spendableSpecialPoints = boughtValues['metatype'][str(priorities['metatype'])][metatype]['Specials']
    # stats = add_base_attributes(stats,maxStats,attributePoints,spendableSpecialPoints)
    # Mook['Attributes'].update(stats)
    #
    #



    #mook = Character()
    #print(mook.__dict__)

#main loop
root = Tk()
root.title("MookGen")
root.minsize(300,300)

EasyMook = Button(root, text ="Easy Mook", command = Make_Easy_Mook)
EasyMook.place(x=50, y=50)

root.mainloop()
