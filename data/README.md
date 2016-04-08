Data

Aggregation Input
The input for our aggregation module is comprised of a rap theme and a description of that theme. For our 
example data, we came up with our own theme, Chicago, and description, "I'm looking for a rap about Chicago. 
Chicago has a lot of things like the Willis Tower, the tallest building in the united states, the chicago cubs, 
a baseball team who hasn't won the world series in over 100 years. It is known as the Windy City. Idk, I 
just need something I can rap about to my friends." Additionally, there is a header called previous lines, which, 
if this were not the first line in the rap, would contain the other lines in the verse. This column would be 
useful to ensure that no lines are repeated and to give inspiration to the people writing the next lines.

Aggregation Output
The main output that would come from our aggregation module would be the lines of rap that each crowd worker wrote.
Our format is reflective of crowdflower because we used this platform to quickly test our concept and its 
viability.

Aggregation Input 2
The next thing we need to aggregate is votes for each line that was submitted. We input each line with the theme 
and the description of the theme.

Aggregation Output 2
We aggregated the votes by having each worker select their favorite line from the list of options. Each option 
would be summed using a python script to determine which line got the most votes.


Quality Control Input
The input for the Quality Control Module would be each line that was submitted along with the number of votes that 
each line recieved

Quality Control Output
The quality control module, which can be a python script can take all of the lines and how many votes each gets and 
outpust the line with the most votes. This output would then be added to the previous lines collumn in the first 
aggregation module.
