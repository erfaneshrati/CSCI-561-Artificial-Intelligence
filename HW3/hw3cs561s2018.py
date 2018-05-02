import numpy as np
import copy
import time

t1 = time.time()
f = open('input.txt')
content = [x.strip() for x in f.readlines()]
f.close()

neg_inf = -99999999999

i = 0
N_rows, N_columns = [int(j) for j in content[i].split(',')]
i += 1
wall_cells_number = int(content[i])
i += 1
wall_cells = {}
for j in range(wall_cells_number):
	wall_cells[str(int(content[i].split(',')[0])-1) + ',' + str(int(content[i].split(',')[1])-1)] = 1
	i += 1
	
terminal_states_number = int(content[i])
i += 1
terminal_states = {} #'x,y' -> reward
for j in range(terminal_states_number):
	terminal_states[str(int(content[i].split(',')[0])-1) + ',' + str(int(content[i].split(',')[1])-1)] = float(content[i].split(',')[2])
	i += 1
p_walk = float(content[i].split(',')[0])
p_run = float(content[i].split(',')[1])
i += 1
r_walk = float(content[i].split(',')[0])
r_run = float(content[i].split(',')[1])
i += 1
discount_factor = float(content[i])
U = np.zeros((N_rows,N_columns))

def utility(r,c):
	if r>= N_rows-1 or str(r+1)+','+str(c) in wall_cells:
		up_walk_util = U[r,c]
	else:
		up_walk_util = U[r+1,c]
	if r <= 0 or str(r-1)+','+str(c) in wall_cells:
		down_walk_util = U[r,c]
	else:
		down_walk_util = U[r-1,c]
	if c >= N_columns-1 or str(r)+','+str(c+1) in wall_cells:
		right_walk_util = U[r,c]
	else:
		right_walk_util = U[r,c+1]
	if c <= 0 or str(r)+','+str(c-1) in wall_cells:
		left_walk_util = U[r,c]
	else:
		left_walk_util = U[r,c-1]
	#######RUNNING#######
	if r >= N_rows-2 or str(r+2)+','+str(c) in wall_cells or str(r+1)+','+str(c) in wall_cells:
		up_run_util = U[r,c]
	else:
		up_run_util = U[r+2,c]
	if r <= 1 or str(r-2)+','+str(c) in wall_cells or str(r-1)+','+str(c) in wall_cells:
		down_run_util = U[r,c]
	else:
		down_run_util = U[r-2,c]
	if c >= N_columns-2 or str(r)+','+str(c+2) in wall_cells or str(r)+','+str(c+1) in wall_cells:
		right_run_util = U[r,c]
	else:
		right_run_util = U[r,c+2]
	if c <= 1 or str(r)+','+str(c-2) in wall_cells or str(r)+','+str(c-1) in wall_cells:
		left_run_util = U[r,c]
	else:
		left_run_util = U[r,c-2]
	return up_walk_util, down_walk_util, right_walk_util, left_walk_util, up_run_util, down_run_util, right_run_util, left_run_util
delta = 999999999
eps = 1e-18

for r in range(N_rows):
	for c in range(N_columns):
		if str(r)+','+str(c) in terminal_states:
			U[r,c] = terminal_states[str(r)+','+str(c)]
U_next = np.zeros((N_rows,N_columns))
U_next = copy.deepcopy(U)

point_values = {}
for r in range(N_rows):
	for c in range(N_columns):
		value = 0
		if str(r)+','+str(c) in terminal_states:
			continue
		elif str(r)+','+str(c) in wall_cells:
			continue
		for target in terminal_states:
			r_t, c_t = [int(j) for j in target.split(',')]
			terminal_reward = terminal_states[target]
			value += terminal_reward*(abs(r_t-r)+abs(c_t-c))
		point_values[c+r*N_columns] = value
sorted_points = sorted(point_values.iteritems(), key=lambda (k,v): (v,k))
iteration_no = 1
while delta > eps * (1-discount_factor)/discount_factor:
	iteration_no+=1
	delta = 0
	for key, _ in sorted_points:
		r = key/N_columns
		c = key%N_columns
		if str(r)+','+str(c) in terminal_states:
			continue
		elif str(r)+','+str(c) in wall_cells:
			continue
		else:
			up_walk_util, down_walk_util, right_walk_util, left_walk_util, up_run_util, down_run_util, right_run_util, left_run_util = utility(r,c)
			walk_up = r_walk + discount_factor*(p_walk*up_walk_util+0.5*(1-p_walk)*right_walk_util+0.5*(1-p_walk)*left_walk_util)
			walk_down = r_walk + discount_factor*(p_walk*down_walk_util+0.5*(1-p_walk)*right_walk_util+0.5*(1-p_walk)*left_walk_util)
			walk_right = r_walk + discount_factor*(p_walk*right_walk_util+0.5*(1-p_walk)*up_walk_util+0.5*(1-p_walk)*down_walk_util)
			walk_left = r_walk + discount_factor*(p_walk*left_walk_util+0.5*(1-p_walk)*up_walk_util+0.5*(1-p_walk)*down_walk_util)
			
			run_up = r_run + discount_factor*(p_run*up_run_util+0.5*(1-p_run)*right_run_util+0.5*(1-p_run)*left_run_util)
			run_down = r_run + discount_factor*(p_run*down_run_util+0.5*(1-p_run)*right_run_util+0.5*(1-p_run)*left_run_util)
			run_right = r_run + discount_factor*(p_run*right_run_util+0.5*(1-p_run)*up_run_util+0.5*(1-p_run)*down_run_util)
			run_left = r_run + discount_factor*(p_run*left_run_util+0.5*(1-p_run)*up_run_util+0.5*(1-p_run)*down_run_util)
			U_new = max([walk_up,walk_down,walk_left,walk_right,run_up,run_down,run_left,run_right])
			if abs(U_new - U[r,c]) > delta:
				delta = abs(U_new - U[r,c])
			U[r,c] = U_new
	print ("delta: " + str(delta))
f = open('output.txt','w')
for r in range(N_rows-1,-1,-1):
	for c in range(N_columns):
		up_walk_util, down_walk_util, right_walk_util, left_walk_util, up_run_util, down_run_util, right_run_util, left_run_util = utility(r,c)
		walk_up = r_walk + discount_factor*(p_walk*up_walk_util+0.5*(1-p_walk)*right_walk_util+0.5*(1-p_walk)*left_walk_util)
		walk_down = r_walk + discount_factor*(p_walk*down_walk_util+0.5*(1-p_walk)*right_walk_util+0.5*(1-p_walk)*left_walk_util)
		walk_right = r_walk + discount_factor*(p_walk*right_walk_util+0.5*(1-p_walk)*up_walk_util+0.5*(1-p_walk)*down_walk_util)
		walk_left = r_walk + discount_factor*(p_walk*left_walk_util+0.5*(1-p_walk)*up_walk_util+0.5*(1-p_walk)*down_walk_util)
		run_up = r_run + discount_factor*(p_run*up_run_util+0.5*(1-p_run)*right_run_util+0.5*(1-p_run)*left_run_util)
		run_down = r_run + discount_factor*(p_run*down_run_util+0.5*(1-p_run)*right_run_util+0.5*(1-p_run)*left_run_util)
		run_right = r_run + discount_factor*(p_run*right_run_util+0.5*(1-p_run)*up_run_util+0.5*(1-p_run)*down_run_util)
		run_left = r_run + discount_factor*(p_run*left_run_util+0.5*(1-p_run)*up_run_util+0.5*(1-p_run)*down_run_util)
		argsort = np.argsort([run_right,run_left,run_down,run_up,walk_right,walk_left,walk_down,walk_up])
		#print ([run_right,run_left,run_down,run_up,walk_right,walk_left,walk_down,walk_up])
		#if sorted([run_right,run_left,run_down,run_up,walk_right,walk_left,walk_down,walk_up])[-1] == sorted([run_right,run_left,run_down,run_up,walk_right,walk_left,walk_down,walk_up])[-2]:
		#	print (str(r)+'_'+str(c))
		action = argsort[-1]
		if str(r)+','+str(c) in wall_cells:
			f.write('None')
		elif str(r)+','+str(c) in terminal_states:
			f.write('Exit')
		elif action == 0:
			f.write('Run Right')
		elif action == 1:
			f.write('Run Left')
		elif action == 2:
			f.write('Run Down')
		elif action == 3:
			f.write('Run Up')
		elif action == 4:
			f.write('Walk Right')
		elif action == 5:
			f.write('Walk Left')
		elif action == 6:
			f.write('Walk Down')
		elif action == 7:
			f.write('Walk Up')
		if c < N_columns - 1:
			f.write(',')
		else:
			f.write('\n')
#print (U)
f.close()
print ("Elapsed time: " + str(time.time()-t1))
