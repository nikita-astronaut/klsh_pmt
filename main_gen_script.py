import numpy as np
import sys
import copy
import random

number_of_tables = 11
zonders = 0
min_judges = None

def read_judges_data(judges_datafile):
	global zonders
	judges = []
	for judge_line in judges_datafile:
		if judge_line[0] == '#':
			continue

		judge_line_split = [element for element in judge_line.split()]
		name = judge_line_split[0]
		surname = judge_line_split[1]
		skill = int(judge_line_split[2])
		if skill == 0:
			zonders += 1
		physician = (int(judge_line_split[3]) == 1)
		senior = (int(judge_line_split[4]) == 1)

		forbidden_teams = []
		for index in range(5, len(judge_line_split)):
			forbidden_teams.append(judge_line_split[index])

		judge = (name, surname, skill, physician, senior, forbidden_teams)
		judges.append(judge)
	return judges

def read_min_skills(min_skills_file):
	min_skills_per_matches = []
	for line in min_skills_file:
		min_skills_per_matches.append(int(line))
	return min_skills_per_matches

def get_all_rooms(rooms_file):
	rooms = []
	for line in rooms_file:
		rooms.append(line)
	return rooms

def get_all_matches(matches_file):
	matches = []
	for line in matches_file:
		first, second = [x for x in line.split()]
		match = (first, second)
		matches.append(match)
	return matches	

def no_conflicts(judge, match_pair):
	return match_pair[0] not in judge[5] and match_pair[1] not in judge[5]

judges = read_judges_data(open('judges.dat', 'r'))
min_skills_per_matches = read_min_skills(open('min_skills.dat', 'r'))
rooms_names_list = get_all_rooms(open('rooms.dat', 'r'))
tour_idx = int(sys.argv[1])
match_pairs_list = get_all_matches(open('matches_' + sys.argv[1] + '.dat', 'r'))

judges_min = len(judges) / number_of_tables

found = False

tables_with_max_judges = len(judges) - judges_min * number_of_tables

while not found:
	tables_judges = [[] for i in range(number_of_tables)]
	judges_temp = copy.deepcopy(judges)
	
	''' first set a senior judge to every table '''
	for table_id in range(number_of_tables):
		success = False
		while not success:
			senior_id = random.randint(0, len(judges_temp) - 1)
			if judges_temp[senior_id][4] and no_conflicts(judges_temp[senior_id], match_pairs_list[table_id]):
				success = True
				tables_judges[table_id].append(judges_temp[senior_id])
				del judges_temp[senior_id]
	print 'seniors set'
	''' now add physicist to all the tables '''
	for table_id in range(number_of_tables):
		success = tables_judges[table_id][0][3] # if the senior judge is a physician, we are done
		while not success:
			physician_id = random.randint(0, len(judges_temp) - 1)
			if judges_temp[physician_id][3] and no_conflicts(judges_temp[physician_id], match_pairs_list[table_id]):
				success = True
				tables_judges[table_id].append(judges_temp[physician_id])
				del judges_temp[physician_id]
	print 'physicists set'
	''' now add zonder to first nZ tables (zonder has zero skill)'''
	for table_id in range(zonders):
		success = False
		while not success:
			zonder_id = random.randint(0, len(judges_temp) - 1)
			if judges_temp[zonder_id][2] == 0 and no_conflicts(judges_temp[zonder_id], match_pairs_list[table_id]):
				success = True
				tables_judges[table_id].append(judges_temp[zonder_id])
				del judges_temp[zonder_id]
	print 'zonders set'
	''' now distribute the other judges in the way that there are from 3 to 4 judges per table (4 on top, 3 on bottom) '''
	for table_id in range(number_of_tables):
		more_needed = judges_min - len(tables_judges[table_id])
		
		if table_id in range(tables_with_max_judges):
			more_needed += 1

		for new_judge in range(more_needed):	
			success = False
			while not success:
				new_id = random.randint(0, len(judges_temp) - 1)
				if no_conflicts(judges_temp[new_id], match_pairs_list[table_id]):
					success = True
					tables_judges[table_id].append(judges_temp[new_id])
					del judges_temp[new_id]

	''' now check that all the requirements are met '''
	found = True
	for table_id in range(number_of_tables):
		skill = 0
		for judge in tables_judges[table_id]:
			skill += judge[2]
		if skill < min_skills_per_matches[table_id]:
			print 'skill fail'
			found = False

''' write judges, pairs and everything required for the protocols and notification to file '''
jf = open('judges_file_' + str(tour_idx) + '.dat', 'w')

for table_id in range(number_of_tables):
	jf.write('table ' + str(table_id) + '\n')
	jf.write('teams ' + match_pairs_list[table_id][0] + ' ' + match_pairs_list[table_id][1] + '\n')
	jf.write('room ' + rooms_names_list[table_id])
	for judge in tables_judges[table_id]:
		jf.write(judge[0] + ' ' + judge[1] + '\n')
