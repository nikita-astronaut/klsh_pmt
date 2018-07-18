#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
def symbcut(string):
	if len(string) == 1:
		return string
	else:
		return string[1:]	

''' adds line to a table '''
def print_game(table_id, team_one, team_two, room, judges, nf):
	outstring = '$' + symbcut(team_one) + '$ --- $' + symbcut(team_two) + '$' + ' & ' + room + ' & '
	for idx in range(len(judges)):
		judge = judges[idx]
		outstring += judge[0] + ' ' + judge[1]
		if idx + 1 != len(judges):
			outstring += ', '
	outstring += ' \\\\ \hline\n'
	nf.write(outstring)		


tour_idx = int(sys.argv[1])
jf = open('judges_file_' + sys.argv[1] + '.dat', 'r')
nf = open('notification_' + str(tour_idx) + '.tex', 'w')
table_id = None
team_one = None
team_two = None
room = None
judges = []

''' print head of the document '''
nf.write('\\documentclass[12pt]{article}\n')
nf.write('\\usepackage[utf8]{inputenc}\n')
nf.write('\\usepackage[russian]{babel}\n')
nf.write('\\usepackage{amsmath}\n')
nf.write('\\usepackage{amssymb}\n')
nf.write('\\usepackage{geometry}\n')
nf.write('\\usepackage{graphicx}\n')
nf.write('\\geometry{top=0.5cm}\n')
nf.write('\\geometry{bottom=0.5cm}\n')
nf.write('\\geometry{left=1.5cm}\n')
nf.write('\\geometry{right=1.5cm}\n')
nf.write('\\pagestyle{empty}\n')
nf.write('\n')
nf.write('\\begin{document}\n')
nf.write('\\begin{center}\n')
nf.write('{\\Large ' + str(tour_idx) + ' тур ФМТ: судьи}\n')
nf.write('\\begin{tabular}{| c | c | c |}\n')
nf.write('\\hline\n')
nf.write('Команды & Аудитория & Судьи \\\\ \\hline\n')

for line in jf:
	line_split = [x for x in line.split()]
	if line_split[0] == 'table':
		if table_id != None:
			print_game(table_id, team_one, team_two, room, judges, nf)
			judges = []
		table_id = int(line_split[1])
	elif line_split[0] == 'teams':
		team_one = line_split[1]
		team_two = line_split[2]
	elif line_split[0] == 'room':
		room = line_split[1]
	elif len(line_split) > 0:
		judges.append((line_split[0], line_split[1]))
print_game(table_id, team_one, team_two, room, judges, nf)		

''' finish document '''
nf.write('\\end{tabular}\n')
nf.write('\\end{center}\n')
nf.write('\\end{document}\n')

''' open .tex file in texmaker '''
subprocess.Popen(['texmaker', 'notification_' + str(tour_idx) + '.tex'], stdout=subprocess.PIPE)
