import copy
f = open('input.txt')
content = [x.strip() for x in f.readlines()]
f.close()
player_name = content[0]
algorithm = content[1]
depth = int(content[2])-1
initial_state = []
for i in range(8):
    initial_state.append(content[3+i].split(','))
row_values = [int(x) for x in content[11].split(',')]
#print (row_values)
inf=9999999999
neg_inf=-9999999999

visited_nodes = 0
best_action = 'pass'
root_utility = neg_inf
one_step_utility = neg_inf

if player_name == 'Star':
    opponent = 'C'
    player = 'S'
else:
    opponent = 'S'
    player = 'C'
            
def utility(state):
    u = 0
    for i in range (8):
        for j in range(8):
            if player_name == 'Star':
                if 'S' in state[i][j]:
                    u += row_values[7-i]*int(state[i][j][1:])
                if 'C' in state[i][j]:
                    u -= row_values[i]*int(state[i][j][1:])
            if player_name == 'Circle':
                if 'C' in state[i][j]:
                    u += row_values[i]*int(state[i][j][1:])
                if 'S' in state[i][j]:
                    u -= row_values[7-i]*int(state[i][j][1:])
    return u
def maxValue(state,alpha,beta,d,passed):
    global root_utility, best_action, one_step_utility, visited_nodes
    #print ("maxValue")
    visited_nodes += 1
    if d==depth:
        return utility(state)
    v = neg_inf
    actions = []
    found_pieces = 0
    for i in range (8):
        for j in range(8):
            if player in state[i][j]:
                found_pieces = 1
                if player == 'S':
                    if j > 0 and ((i > 1 and state[i-1][j-1] == '0') or (i == 1 and (opponent not in state[i-1][j-1]))):
                        actions.append(str(i)+str(j)+'-'+str(i-1)+str(j-1))
                    if j < 7 and ((i > 1 and state[i-1][j+1] == '0') or (i == 1 and (opponent not in state[i-1][j+1]))):
                        actions.append(str(i)+str(j)+'-'+str(i-1)+str(j+1))
                    if j > 1 and ((i > 2 and state[i-2][j-2] == '0' and opponent in state[i-1][j-1]) or (i == 2 and (opponent not in state[i-2][j-2]) and opponent in state[i-1][j-1])):
                        actions.append(str(i)+str(j)+'-'+str(i-2)+str(j-2))
                    if j < 6 and ((i > 2 and state[i-2][j+2] == '0' and opponent in state[i-1][j+1]) or (i == 2 and (opponent not in state[i-2][j+2]) and opponent in state[i-1][j+1])):
                        actions.append(str(i)+str(j)+'-'+str(i-2)+str(j+2))
                else:
                    if (j > 0 and ((i < 6 and state[i+1][j-1] == '0') or (i == 6 and (opponent not in state[i+1][j-1])))):
                        actions.append(str(i)+str(j)+'-'+str(i+1)+str(j-1))
                    if j < 7 and ((i < 6 and state[i+1][j+1] == '0') or (i == 6 and (opponent not in state[i+1][j+1]))):
                        actions.append(str(i)+str(j)+'-'+str(i+1)+str(j+1))
                    if j > 1 and ((i < 5 and state[i+2][j-2] == '0' and opponent in state[i+1][j-1]) or (i == 5 and (opponent not in state[i+2][j-2]) and opponent in state[i+1][j-1])):
                        actions.append(str(i)+str(j)+'-'+str(i+2)+str(j-2))
                    if j < 6 and ((i < 5 and state[i+2][j+2] == '0' and opponent in state[i+1][j+1]) or (i == 5 and (opponent not in state[i+2][j+2]) and opponent in state[i+1][j+1])):
                        actions.append(str(i)+str(j)+'-'+str(i+2)+str(j+2))
    actions = sorted(actions)
    #print (actions)
    for action in actions:
        source, destination = action.split('-')
        new_state = copy.deepcopy(state)
        s1 = int(source[0])
        s2 = int(source[1])
        d1 = int(destination[0])
        d2 = int(destination[1])
        new_state[s1][s2] = '0'
        if player == 'S':
            if d1 == 0 and new_state[d1][d2] != '0':
                new_state[d1][d2] = player + str(int(new_state[d1][d2][1:]) + 1)
            else:
                new_state[d1][d2] = player + '1'
            if s1-d1 == 2: #remove opponent
                new_state[s1-1][(s2+d2)/2] = '0'
        else:
            if d1 == 7 and new_state[d1][d2] != '0':
                new_state[d1][d2] = player + str(int(new_state[d1][d2][1:]) + 1)
            else:
                new_state[d1][d2] = player + '1'
            if d1-s1 == 2: #remove opponent
                new_state[s1+1][(s2+d2)/2] = '0'
        #print (new_state)
        minValueTemp = minValue(new_state,alpha,beta,d+1,0)
        if d==-1 and minValueTemp > v:
            best_action = action
            #print (new_state)
            one_step_utility = utility(new_state)
        v = max(v,minValueTemp)
        if algorithm == 'ALPHABETA':
            if v >= beta:
                return v
        alpha = max(alpha, v)
    if found_pieces == 0:
        #visited_nodes -= 1
        return utility(state)
    if len(actions)==0:
        if d==-1:
            one_step_utility = utility(state)
        if passed == 1:
            #print ("double_passed")
            visited_nodes += 1
            return utility(state)
        v = max(v, minValue(copy.deepcopy(state),alpha,beta,d+1,1))
    root_utility = v
    return v
    
def minValue(state,alpha,beta,d,passed):
    #print ("minValue")
    global visited_nodes
    visited_nodes += 1
    if d==depth:
        return utility(state)
    v = inf
    actions = []
    found_pieces = 0
    for i in range (8):
        for j in range(8):
            if opponent in state[i][j]:
                found_pieces = 1
                if opponent == 'S':
                    if j > 0 and ((i > 1 and state[i-1][j-1] == '0') or (i == 1 and (player not in state[i-1][j-1]))):
                        actions.append(str(i)+str(j)+'-'+str(i-1)+str(j-1))
                    if j < 7 and ((i > 1 and state[i-1][j+1] == '0') or (i == 1 and (player not in state[i-1][j+1]))):
                        actions.append(str(i)+str(j)+'-'+str(i-1)+str(j+1))
                    if j > 1 and ((i > 2 and state[i-2][j-2] == '0' and player in state[i-1][j-1]) or (i == 2 and (player not in state[i-2][j-2]) and player in state[i-1][j-1])):
                        actions.append(str(i)+str(j)+'-'+str(i-2)+str(j-2))
                    if j < 6 and ((i > 2 and state[i-2][j+2] == '0' and player in state[i-1][j+1]) or (i == 2 and (player not in state[i-2][j+2]) and player in state[i-1][j+1])):
                        actions.append(str(i)+str(j)+'-'+str(i-2)+str(j+2))
                else:
                    if (j > 0 and ((i < 6 and state[i+1][j-1] == '0') or (i == 6 and (player not in state[i+1][j-1])))):
                        actions.append(str(i)+str(j)+'-'+str(i+1)+str(j-1))
                    if j < 7 and ((i < 6 and state[i+1][j+1] == '0') or (i == 6 and (player not in state[i+1][j+1]))):
                        actions.append(str(i)+str(j)+'-'+str(i+1)+str(j+1))
                    if j > 1 and ((i < 5 and state[i+2][j-2] == '0' and player in state[i+1][j-1]) or (i == 5 and (player not in state[i+2][j-2]) and player in state[i+1][j-1])):
                        actions.append(str(i)+str(j)+'-'+str(i+2)+str(j-2))
                    if j < 6 and ((i < 5 and state[i+2][j+2] == '0' and player in state[i+1][j+1]) or (i == 5 and (player not in state[i+2][j+2]) and player in state[i+1][j+1])):
                        actions.append(str(i)+str(j)+'-'+str(i+2)+str(j+2))
    actions = sorted(actions)
    #print (actions)
    for action in actions:
        source, destination = action.split('-')
        new_state = copy.deepcopy(state)
        s1 = int(source[0])
        s2 = int(source[1])
        d1 = int(destination[0])
        d2 = int(destination[1])
        new_state[s1][s2] = '0'
        if opponent == 'S':
            if d1 == 0 and new_state[d1][d2] != '0':
                new_state[d1][d2] = opponent + str(int(new_state[d1][d2][1:]) + 1)
            else:
                new_state[d1][d2] = opponent + '1'
            if s1-d1 == 2: #remove opponent
                new_state[s1-1][(s2+d2)/2] = '0'
        else:
            if d1 == 7 and new_state[d1][d2] != '0':
                new_state[d1][d2] = opponent + str(int(new_state[d1][d2][1:]) + 1)
            else:
                new_state[d1][d2] = opponent + '1'
            if d1-s1 == 2: #remove opponent
                new_state[s1+1][(s2+d2)/2] = '0'
        #print ('here')
        v = min(v, maxValue(new_state,alpha,beta,d+1,0))
        if algorithm == 'ALPHABETA':
            if v <= alpha:
                return v
        beta = min(beta, v)
    if found_pieces == 0:
        #visited_nodes -= 1
        return utility(state)
    if len(actions)==0: #handling pass action
        if passed == 1:
            #print ("double_passed")
            visited_nodes += 1
            return utility(state)
        v = min(v, maxValue(copy.deepcopy(state),alpha,beta,d+1,1))
    return v

chess_translate = {'0':'H','1':'G','2':'F','3':'E','4':'D','5':'C','6':'B','7':'A'}
maxValue(initial_state,neg_inf,inf,-1,0)
if best_action != 'pass':
    source,destination = best_action.split('-')
    source = chess_translate[source[0]] + str(int(source[1])+1)
    destination = chess_translate[destination[0]] + str(int(destination[1])+1)
    best_action = source + '-' + destination
print (best_action)
print (one_step_utility)
print (root_utility)
print (visited_nodes)

f = open('output.txt','w')
f.write(best_action + '\n')
f.write(str(one_step_utility) + '\n')
f.write(str(root_utility) + '\n')
f.write(str(visited_nodes))

