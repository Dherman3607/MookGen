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
    'Intelligence':0,
    'Charisma':0,
    'Edge':0,
    'Magic' : '-',
    'Resonance' : '-',
    'Initiative': 0

}


    #'Initiative': Stats['Physical']['Reaction'] + Stats['Mental']['Intelligence']
#callback defs
def ReadJson(Inputfile):

    with open(Inputfile,'r') as f:
        return json.load(f)
def  addAttributes(inputStats,SpendablePoints):
    print(inputStats,SpendablePoints)

def MakeEasyMook():
    sumToTen = 10
    Priorities = ReadJson('data\\Priorities.json')
    metatypeStats = ReadJson('data\\metatypes.json')
    boughtValues = ReadJson('data\\boughtValues.json')
    #SkillPointAllocations = ReadJson('data\\SkillPoints.json')
    SpecialStaters = ReadJson('data\\SpecialStats.json')
    PointCost = [ReadJson('data\\pointCosts.json')]
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

    attributePoints = int(PointCost[0]['attributes'][str(Priorities['attributes'])])

    #is this guy magical, or a technomancer?
    if(Priorities['Magic'] >0 ):
        #print (SpecialStaters[str(Priorities['Magic'])])
        specialty = random.choice(list(SpecialStaters[str(Priorities['Magic'])]))
        #specialityStats = SpecialStaters[str(Priorities['Magic'])[specialty]

        specialtyStats = SpecialStaters[str(Priorities['Magic'])][specialty]

        print(type(specialty))
        print(specialtyStats)
        if(specialtyStats['Magic']):
            print('we have a magic user!')
            Stats['Magic'] = specialtyStats['Magic']
        elif(specialtyStats['Resonance']):
            print('We have a technomancer!')

    print(Stats)
    Stats = addAttributes(Stats,attributePoints)



#main loop
root = Tk()
root.title("hello")
root.minsize(300,300)

EasyMook = Button(root, text ="Easy Mook", command = MakeEasyMook)
EasyMook.place(x=50, y=50)

root.mainloop()
