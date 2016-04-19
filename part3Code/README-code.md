# README-code

"Make-A-Rap” will effectively crowd-source raps based on any theme a requester decides to post. We will determine if it is possible for a random group of individuals to cooperatively create an effective and aesthetically pleasing rap.

### Flow of information
- Ran via **bash. sh**, a bash file that automates the process of running our commands on the terminal. 
- **code_production.py** is the first piece of code in our project. It takes in a rap theme (that we generated, in **_proto_in.tsv_**) and posts a HIT to CrowdFlower called **"Write a line for a rap!"**. This HIT requests each contributor to write the next (or first) line of the rap based on the title, description, and current lines that are provided to them. After CrowdFlower has aggregated responses, the results come in a TSV called _produce_line_output.tsv_ that contains worker information as well as the lines they submitted. 
- **code_voting.py**, takes _produce_line_output.tsv_ as the input and parses it for the rap lyrics that were submitted. It then uploads this TSV that has four columns: rap theme, description, previous line(s), and possible line(s). This is uploaded to CrowdFlower to create a HIT called **"Pick the best line for a rap!"** in which users vote on whether a lyric should be added to the rap. This HIT then outputs a CSV file called _produce_vote_output.csv_ with 5 columns: rap theme, description, previous line(s), possible line(s), and “should this line be added to the above rap?”.  
- **votes_to_counts.py** then takes _produce_vote_output.csv_ and tallies the number of “yes” votes each line received. It then outputs a CSV file called _QC_input.csv_ with 5 columns: rap theme, description, previous line(s), possible line(s), and “vote numbers”, with vote numbers being the total number of “yes” votes for each line.
- **QC_code.py** then takes  _QC_input.csv_, containing vote numbers as an input, and determines the line with the greatest number of “yes” votes. The code then permanently appends that line to the previous lines of the rap containing that title and description. The resulting file/output is an updated **_proto_in.tsv_** with the title, description, and updated current/previous lines. This output is then fed back into **code_production.py** and the process repeats for the number of lines in the rap, which we have designated as 10.

### Instructions to run
  - Log on to a server that will be uninterrupted for a while (a few hours or days)
  - type into the terminal:
```bash
easy_install crowdflower
```
  - Make sure that **proto_in.tsv** and the **crowdflower** (the crowdflower API folder) is in the same directory as **bash.sh**, **code_production.py**, **code_voting.py**, **votes_to_counts.py**, and **QC_code.py**.
  - Inspect **proto_in.tsv** to ensure it is 3 columns, with a header row and a data row, containing a title, description, and N/A. **_It must be N/A for the code to work!_**
  - After ensuring the above four points, type into the terminal
```bash
bash bash.sh
```
  - This will begin the automated process. Because it is set to internal workers (a.k.a. 'sandbox mode'), you will need to re-collect the link to access the current HIT. There will be on the order of 20 HITs. Please discuss with Arjun Sastry and Thomas Peterson a plan for distributing these links. 
  - ALTERNATIVELY, we can turn off sandbox mode and open the HITs to the public in addition to the students. This will remove the need to redistribute the link for the crowdflower HITs every time the task updates itself.
  - The tasks are titled: **"Write a line for a rap!"** and **"Pick the best line for a rap!"**. Please search for these tasks when completing them.

