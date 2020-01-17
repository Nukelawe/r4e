import random
import math

players = [
    "Nukelawe",
    "MajorBongo",
    "DiIusion",
    "_Mystery_Man",
    "Oreolamp"
]
teamsize = 2
teamcount = len(players) / teamsize + 1

def buildTeams():
    teams = [[]] * teamcount
    for i in range(teamcount):
        teams[i] = random.sample(players, min(teamsize, len(players)))
        for player in teams[i]:
            players.remove(player)
    return teams

def generateSpawnpoints():
    r1 = 1000
    r2 = .2 * r1
    angle = random.uniform(0, 360 / teamcount)
    angles = [angle + i * 360 / teamcount for i in range(teamcount)]
    xs = [math.cos(deg * math.pi / 180) * r1 for deg in angles]
    zs = [math.sin(deg * math.pi / 180) * r1 for deg in angles]
    coords = [
        [int(xs[i]) + random.randint(-r2, r2),
         int(zs[i]) + random.randint(-r2, r2)
        ] for i in range(teamcount)
    ]
    return coords

def commandTeams(teams):
    string = ""
    for i in range(len(teams)):
        teamname = str(i)
        string += "team add " + teamname + "\n"
        for player in teams[i]:
            string += "team join " + teamname + " " + player + "\n" 
    return string

def commandSpread(coords):
    string = ""
    for i in range(teamcount):
        x = coords[i][0]
        z = coords[i][1]
        string += "forceload add " + str(x) + " " + str(z) + "\n"
        string += 'summon armor_stand ' + str(x) + ' 256 ' + str(z) + ' {Tags:["' + str(i) + '"],Invisible:1,Motion:[0d,-10d,0d]}\n'
    return string

def generateInitFunction():
    template = open("template/data/minecraft/functions/init.mcfunction", "r")
    output = open("r4e/data/minecraft/functions/init.mcfunction", "w")
    teams = buildTeams()
    coords = generateSpawnpoints()
    for line in template:
        string = line
        if '<command_teams>' in line:
            string = commandTeams(teams)
        if '<command_spreads>' in line:
            string = commandSpread(coords)
        output.write(string)
    template.close()
    output.close()

def generateRespawnFunction():
    output = open("r4e/data/minecraft/functions/respawn.mcfunction", "w")
    string = ""
    for i in range(teamcount):
        teamname = str(i)
        string += "tp @a[team=" + teamname + ",x=0,y=0,z=0,dx=0,dy=255,dz=0] @e[type=armor_stand,limit=1,tag=" + teamname + "]\n"
    output.write(string)

generateInitFunction()
generateRespawnFunction()
