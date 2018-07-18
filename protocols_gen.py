#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess

def symbcut(string):
	if len(string) == 1:
		return string
	else:
		return string[1:]

''' make complete procotol '''
def print_protocol(table_id, team_one, team_two, room, judges, pf):
	pf.write('\\begin{center}\n')
	pf.write('{\\Huge \\bf ' + str(tour_idx) + ' тур ФМТ}\n')
	pf.write('\\end{center}\n')
	pf.write('\\begin{minipage}{.30\\textwidth}\n')
	pf.write('\\begin{center}\n')
	pf.write('\\includegraphics[width=0.48\\textwidth]{klshlogo.pdf}\n')
	pf.write('\\end{center}\n')
	pf.write('\\end{minipage}\n')
	pf.write('\\begin{minipage}{.65\\textwidth}\n')
	pf.write('\\begin{flushleft}\n')
	pf.write('{\\bf Старший судья}: ' + judges[0][0] + ' ' + judges[0][1] + '\\\\ \n')
	
	pf.write('{\\bf Судьи}: ')
	for index in range(1, len(judges)):
		judge = judges[index]
		pf.write(judge[0] + ' ' + judge[1])
		if index + 1 != len(judges):
			pf.write(', ')
	pf.write('\\\\ \n')

	pf.write('{\\bf Команды}: ' + '$' + symbcut(team_one) + '$ --- $' + symbcut(team_two) + '$\\\\ \n')
	pf.write('{\\bf Аудитория}: ' + room + '\\\\ \n')
	pf.write('\\end{flushleft}\n')
	pf.write('\\end{minipage}\n')
	pf.write('\\begin{center}')
	pf.write('{\\bf Протокол основного времени: } \\\\ \n')

	pf.write('\\begin{tabular}{|p{3.3cm}|p{1.5cm}|p{2cm}|p{1.5cm}|p{1.5cm}|p{2cm}|p{1.5cm}|}\n')
	pf.write('\\hline Время начала: & \\multicolumn{3}{c|}{Команда $' + symbcut(team_one) + '$} & \\multicolumn{3}{c|}{Команда $' + symbcut(team_two) + '$ }\\\\\\cline{2-7} {} & Время & Баллы $' + symbcut(team_one) + '$ & Ответ & Время & Баллы $' + symbcut(team_two) + '$ & Ответ \\\\\\hline \\hline \\center Задача 1 &{}&{}&{}&{}&{}&{}\\\\[20mm]\\hline \\hline \\center Задача 2 &{}&{}&{}&{}&{}&{}\\\\[20mm]\\hline \\hline \\center Задача 3 &{}&{}&{}&{}&{}&{}\\\\[20mm]\\hline \\hline \\center Задача 4 &{}&{}&{}&{}&{}&{}\\\\[20mm]\\hline \\hline \\center Стрелки &{}&{}&{}&{}&{}&{}\\\\[20mm]\\hline\n')
	pf.write('\\end{tabular}\n')

	pf.write('$ $\\\\\n')
	pf.write('$ $\\\\\n')
	pf.write('{\\bf Протокол второго тура: } \\\\ \n')
	pf.write('\\begin{tabular}{ | p{7cm} | p{1cm} | p{1cm} |}\n')
	pf.write('\\hline\n')
	pf.write('$ $ & \\centering $' + symbcut(team_one) + '$ & $\;$ $' + symbcut(team_two) + '$ \\\\ \\hline')
#	pf.write('\\raggedleft Вольные стрелки: & & \\\\ \\hline')	
	pf.write('\\raggedleft Первый тур: & & \\\\ \\hline')
	pf.write('\\raggedleft Решение задачи соперника: & & \\\\ \\hline')
	pf.write('\\raggedleft Штраф за незнание: & & \\\\ \\hline')
	pf.write('\\raggedleft Дисциплинарный штраф: & & \\\\ \\hline')
	pf.write('\\raggedleft \\bf Итоговый счёт: & & \\\\ \\hline \hline')
	pf.write('\\raggedleft Красота обменной задачи: & & \\\\ \\hline')
	pf.write('\\raggedleft Согласие команд: & & \\\\ \\hline')
	pf.write('\\end{tabular}')
	pf.write('\\end{center}\n')
	pf.write('$ $\\\\\n')
	pf.write('$ $\\\\\n')
	pf.write('$ $\\\\\n')
	pf.write('$ $\\\\\n')
	pf.write('{\\bf Подписи судей: }................................................................................................................')
	pf.write('\\newpage\n')	
tour_idx = int(sys.argv[1])
jf = open('judges_file_' + sys.argv[1] + '.dat', 'r')
pf = open('protocol_' + str(tour_idx) + '.tex', 'w')
table_id = None
team_one = None
team_two = None
room = None
judges = []

''' print head of the document '''
pf.write('\\documentclass[12pt]{article}\n')
pf.write('\\usepackage[utf8]{inputenc}\n')
pf.write('\\usepackage[russian]{babel}\n')
pf.write('\\usepackage{wrapfig}\n')
pf.write('\\usepackage{amsmath}\n')
pf.write('\\usepackage{amssymb}\n')
pf.write('\\usepackage{geometry}\n')
pf.write('\\usepackage{graphicx}\n')
pf.write('\\geometry{top=0.5cm}\n')
pf.write('\\geometry{bottom=0.5cm}\n')
pf.write('\\geometry{left=1.5cm}\n')
pf.write('\\geometry{right=1.5cm}\n')
pf.write('\\pagestyle{empty}\n')
pf.write('\n')
pf.write('\\begin{document}\n')

''' document body '''
for line in jf:
	line_split = [x for x in line.split()]
	if line_split[0] == 'table':
		if table_id != None:
			print_protocol(table_id, team_one, team_two, room, judges, pf)
			judges = []
		table_id = int(line_split[1])
	elif line_split[0] == 'teams':
		team_one = line_split[1]
		team_two = line_split[2]
	elif line_split[0] == 'room':
		room = line_split[1]
	elif len(line_split) > 0:
		judges.append((line_split[0], line_split[1]))
print_protocol(table_id, team_one, team_two, room, judges, pf)
pf.write('\\end{document}\n')

subprocess.Popen(['texmaker', 'protocol_' + str(tour_idx) + '.tex'], stdout=subprocess.PIPE)
