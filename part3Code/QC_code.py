'''
QC_code.py


input headers from QC_input.csv:
rap_theme
description
previous_lines
possible_lines
vote_numbers
'''

import csv

if __name__ == '__main__' : 
    # Create lists for desired objects
    worker_ids = [];
    gold_answers = [];
    answers = [];
    urls = [];

    with open('QC_input.csv', 'rb') as full:
        # Create reader object for the quality control input
        reader = csv.reader(full)
        
        # Vote count default is 0
        votes = 0
        rap = ''

        # Load into lists the desired information
        for row in reader:
            try:
                current_vote = int(row[4])
                if current_vote > votes:
                    # Tracks winning rap and the vote count of winning rap
                    votes = current_vote
                    rap = row[3]
            except:
                continue
    
    with open('proto_in.tsv', 'r') as old:
        old_reader = csv.reader(old, delimiter='\t')
        next(old_reader)
        for line in old_reader:
            theme = line[0]
            description = line[1]
            previous_lines = line[2]
        
    # Update the lines
    if (previous_lines.strip() == 'N/A'):
        previous_lines = rap
    else:
        previous_lines = previous_lines + '; ' + rap
        
    # Update the new input file for the next iteration
    with open('proto_in.tsv', 'wb') as f:
        output = csv.writer(f, delimiter='\t')
        headers = ['rap_theme', 'description', 'previous_lines']
        output.writerow(headers)
        row=[theme, description, previous_lines]
        output.writerow(row)
    print rap
