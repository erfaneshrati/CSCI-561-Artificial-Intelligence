from sets import Set
f = open('input1.txt')
content = [x.strip() for x in f.readlines()]
f.close()

group_count = int(content[0])
pot_count = int(content[1])
pots = {}
for i in range(2,2+pot_count):
    pots[i-2] = content[i].split(',')
group_assignments = {}
continentals = {'AFC':[],'CAF':[],'OFC':[],'CONCACAF':[],'CONMEBOL':[],'UEFA':[]}

for i in range(i+1, len(content)):
    continentals[content[i].split(':')[0]] = content[i].replace(content[i].split(':')[0]+':','').split(',')
    
team_assignments = {}
for i in range(group_count):
    team_assignments[i] = []
    
team_regions = {}

for region in continentals.keys():
    if continentals[region] != ['None']:
        for team in continentals[region]:
            group_assignments[team] = -1
            team_regions[team] = region
#print (team_regions)
pots_constraints = {}      
team_pots = {}
for pot in pots:
    for i in range(len(pots[pot])):
        for j in range(len(pots[pot])):
            if i != j:
                pots_constraints[pots[pot][i]+'-'+pots[pot][j]] = 1
        team_pots[pots[pot][i]] = pot
#print (team_pots)
continent_constraints = {}
for continent in continentals:
    if continent != 'UEFA':
        for i in range(len(continentals[continent])):
            for j in range(len(continentals[continent])):
                if i != j:
                    continent_constraints[continentals[continent][i]+'-'+continentals[continent][j]] = 1
                    
UEFA_constraints = {}
for continent in continentals:
    if continent == 'UEFA':
        for i in range(len(continentals[continent])):
            for j in range(len(continentals[continent])):
                for k in range(len(continentals[continent])):
                    if i != j and j != k and i != k:
                        UEFA_constraints[continentals[continent][i]+'-'+continentals[continent][j]+'-'+continentals[continent][k]] = 1
        break

team_names = continentals['UEFA'] + continentals['AFC'] + continentals['CAF'] + continentals['OFC'] + continentals['CONMEBOL'] + continentals['CONCACAF']
team_names = [i for i in team_names if i != 'None']

def crange(start, modulo):
    result = []
    index = start
    i = 0
    while i < modulo:
        result.append(index)
        index = (index + 1) % modulo
        i += 1
    return result
import time
time1 = time.time()
failure_past = Set()
def backtrack(team_id,start, modulo):
    if (time.time()-time1) > 150:
        return False
    global failure_past
    if team_id == len(team_names):
        return True
    set_of_grps = Set()
    for g_id in range(group_count):
        g_teams = team_assignments[g_id]
        current_g = Set([team_regions[t]+str(team_pots[t]) for t in g_teams])
        set_of_grps.add(current_g)
    if set_of_grps in failure_past:
        #print ("hereee")
        return False
    region_pot_patterns = Set()
    for group_id in range(group_count):
    #for group_id in crange(start,group_count):
        group_teams = team_assignments[group_id]
        current_grp = Set([team_regions[t]+str(team_pots[t]) for t in group_teams])
        #if (current_grp in region_pot_patterns):
        #    print (current_grp in region_pot_patterns)
        if (not current_grp in region_pot_patterns) or (len(region_pot_patterns) == 0) or len(current_grp) == 0:
            consistent = True
            for t1 in team_assignments[group_id]:
                if consistent == False:
                    break
                for t2 in team_assignments[group_id]:
                    if team_names[team_id]+'-'+t1+'-'+t2 in UEFA_constraints:
                        consistent = False
                        break
                if team_names[team_id]+'-'+t1 in pots_constraints or team_names[team_id]+'-'+t1 in continent_constraints:
                    consistent = False
                    break
            if consistent == True:
                group_assignments[team_names[team_id]] = group_id
                team_assignments[group_id].append(team_names[team_id])
                result = backtrack(team_id+1,(start + 1)%modulo,modulo)
                if result == False:
                    set_of_grps = Set()
                    for g_id in range(group_count):
                        g_teams = team_assignments[g_id]
                        current_g = Set([team_regions[t]+str(team_pots[t]) for t in g_teams])
                        set_of_grps.add(current_g)
                    if len(failure_past) < 30000:
                        failure_past.add(set_of_grps)
                    #print (len(failure_past))
                    team_assignments[group_assignments[team_names[team_id]]].pop()
                    group_assignments[team_names[team_id]] = -1
                    region_pot_patterns.add(Set([team_regions[team_names[team_id]]+str(team_pots[team_names[team_id]]) for t in group_teams]))
                    #print (region_pot_patterns)
                    #print (team_assignments)
                else:
                    return True
    return False
        
#print (continentals)
#print (group_assignments)
f = open('output.txt','w')
if backtrack(0,0,group_count):
    f.write('Yes\n')
    for i in range(group_count):
        if len(team_assignments[i])==0:
            f.write('None')
        for j,team in enumerate(team_assignments[i]):
            f.write(team)
            if j < len (team_assignments[i]) - 1:
                f.write(',')
        f.write('\n')
else:
    f.write('No')
    #print ("No Solution Found!!!")
f.close()
#print (pots_constraints)
#print (continent_constraints)
#print (UEFA_constraints)
