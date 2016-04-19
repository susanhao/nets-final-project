Code_production.py is the first piece of code in our project. It takes in a rap theme (that we generated) and posts a HIT to CrowdFlower. This HIT requests each contributor to write the next (or first) line of the rap based on the title, description, and current lines that are provided to them. After CrowdFlower has aggregated responses, the results come in a CSV that contains worker information as well as the lines they submitted. 

The next piece of code, code_voting.py, takes this CSV as the input and parses it for the rap lyrics that were submitted. It then creates a CSV that has four columns: rap theme, description, previous line(s), and possible line(s). That CSV file is then uploaded to CrowdFlower to create a HIT in which users vote on whether a lyric should be added to the rap. 

This HIT then outputs a TSV file with 5 columns: rap theme, description, previous line(s), possible line(s), and “should this line be added to the above rap?”.  The third piece of code, votes_to_counts.py, then takes in this TSV file and tallies the number of “yes” votes each line received. It then outputs a CSV file with 5 columns: rap theme, description, previous line(s), possible line(s), and “vote numbers”, with vote numbers being the total number of “yes” votes for each line. 

QC_code.py then takes this CSV containing vote numbers as an input, and determines the line with the greatest number of “yes” votes. The code then permanently appends that line to the previous lines of the rap containing that title and description. The resulting file/output is a TSV with the title, description, and updated current/previous lines. This output is then fed back into code_production.py and the process repeats. 

Bash.yaml is a bash file that automates the process of running our commands on the terminal.

