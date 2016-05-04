import sys
import csv
import json

with open('produce_vote_output.csv', 'r') as infile:
	reader = csv.DictReader(infile)
	data = {}
	for row in reader:
		rap_theme = row['rap_theme']
		description = row['description']
		previous_lines = row['previous_lines']
		line = row['possible_lines']
		for header in row:
			if header == 'should_this_line_be_added_to_the_above_rap':
				if line not in data:
					data[line] = 0
				if row[header] == 'yes':
					data[line] += 1


output = csv.writer(open('QC_input.csv', 'w'))
headers = ['rap_theme', 'description', 'previous_lines', 'possible_lines', 'vote_numbers']
output.writerow(headers)

for line in data:
	row = [rap_theme, description, previous_lines, line, data[line]]
	output.writerow(row)
	
