'''
code_production.py

Provides a user with a rap theme and previously finalized rap lines, and then asks a user to enter in the lines.

CHANGE # OF JUDGEMENTS FOR FUTURE

LAUNCHED INTERNALLY

'''

import os
import sys
import json
import random
import crowdflower
import csv
import time
from crowdflower.exception import CrowdFlowerError

# expects api key to be available in your environment variables; does not use cache
conn = crowdflower.Connection()
job_tag = 'produce some lines'


def _find_job():
    for job in conn.jobs():
        if job_tag in job.tags:
            return job


def create():
    #filename = os.path.join(crowdflower.root, 'examples', 'spam.txt')
    #filename = '/Users/TDPeterson/Dropbox/nets213/FINAL/proto_in.tsv'

    def iter_data():
        for i, line in enumerate(open('proto_in.tsv'), 1):
            if i != 1:
                title, description, previous = line.strip().split('\t')
                yield {'title': title, 'description': description, 'previous': previous}

    # Format of inputing title, description, and previous lines
    input_theme = list(iter_data())
    
    job = conn.upload(input_theme)
    print >> sys.stderr, 'Uploaded data' 

    job.update({
        'title': 'Write a line for a rap!',
        'max_judgments_per_worker': 1,
        'units_per_assignment': 1,
        'judgments_per_unit': 10,
        'payment_cents': 5,
        'instructions': '''
<h1>Overview: &nbsp;</h1>

<ul>
	<li>A rap is "spoken or chanted rhyming lyrics"</li>
	<li>Your task is to write the next line to an original rap!</li>
</ul>
<hr>

<h1>Steps:&nbsp;</h1>

<ol>
	<li>Read the "Rap Title" , "Description", and "Current Lines"</li>
	<li>Think about a creative next line for this rap that relates to the topic, description, and lines already written.</li>
	<li>Write it down and submit your response!</li>
</ol>
<hr>

<h1>Rules &amp; Tips:</h1>

<ol>
	<br>
	<li>Keep in mind: THIS IS ONLY A SINGLE LINE to a rap, not the whole rap, so keep your response short. :)</li>
	<li>If there is no "Description", or it does not make sense with the Rap Title, then just write your line based on the "Rap Title".</li>
	<li>If "Current Lines" says N/A, then just write your line based on the "Rap Title"</li>
	<li>Feel free to be as creative and original as you like! (<u>Your response might be part of a class presentation!</u>)</li>
	<li>MOST IMPORTANTLY:

		<ol>
			<li>Keep your response it short</li>
			<li>Keep your response (somewhat) relevant to the topic and/or description</li>
			<li>Use the current lines to inspire your new rap line.</li>
			<li><u>Please do not copy any of the current lines. We want this rap to be good!!!</u></li>            
		</ol>
	</li>
</ol>

<p>THANKS EVERYONE!! :D :D :D</p>
<hr>

<h1>Examples: (DO NOT USE THESE EXAMPLES)</h1>

<ul>
	<li>&nbsp;Rap Title: "California Girls". Description: "I'm looking for a rap about girls in California"

		<ul>
			<li>EXAMPLE RESPONSE: Toned, tan, fit and ready. Turn it up 'cause it's gettin' heavy. Wild Wild West Coast. These are the girls I love the most.</li>
			<li>This response is good because it is short and relevant to the topic.</li>
		</ul>
	</li>
</ul>

<p>
	<br>
</p>

<ul>
	<li>Rap Title: "My name is Carl". Description: "No Data Available"

		<ul>
			<li>EXAMPLE RESPONSE: Carl is a man, just an ordinary man, he's got no money, but he's got a plan.</li>
			<li>This response is also good because it is short and relevant to the topic, even though there is no description.</li>
		</ul>
	</li>
</ul>

<p>
	<br>
</p>

<ul>
	<li>Rap Title: "Ozone depletion". Description: "I don't know anything about this"

		<ul>
			<li>RESPONSE: "Tree and deers are full of life, I just wanna see them true"</li>
			<li>This response is good because even though it doesn't make sense it might be related to Ozone Depletion in some way.</li>
		</ul>
	</li>
</ul>
<hr>

        ''',
        'cml': '''
<div class="html-element-wrapper">
  <span>
    <strong>
      <font size = "5">Rap Title: {{title}}</font>
    </strong>
  </span>
  <br/>
  <br/>
  <span>Description: {{description}}</span>
  <br/>
  <br/>
  <span>Current Lines: <ul><font size = "4"><strong>{{previous}}</strong></font></ul></span>
</div>
<br/>
<br/>
<cml:text label="Write the next line for this rap based on the title, description, and current lines! Be as creative and original as you like!" name="next_line" validates="required clean:['multipleWhitespace']" gold="true" />

        ''',
        'options': {
            'front_load': 0, # quiz mode = 1; turn off with 0
        }
    })
    print >> sys.stderr, 'Updated job'

    # add the 'produce line' tag so that we can easily find this job later
    job.tags = [job_tag]
    print >> sys.stderr, 'Tagged job as %r' % job_tag


def launch():
    job = _find_job()
    job.launch(1)#, channels=['cf_internal'])
    print 'Temporary Sleep for Production Task to Launch'
    time.sleep(2)
    print >> sys.stderr, 'Launched Job[%d]' % job.id

def check():
    job = _find_job()
    complete = job.properties["completed"]
    while complete == False:
        print 'Production: Incomplete'
        print 'Judgments remaining: %d' % job.ping()["needed_judgments"]
        time.sleep(300)
        job = _find_job()
        complete = job.properties["completed"]
    print "Production: complete!"

def ping():
    job = _find_job()
    print "Five Minute Ping Pause: production"
    #time.sleep(300)
    #print job.ping()["needed_judgments"]
    print job.properties["completed"]
    #print job.id
    #print pinged["needed_judgments"]
    #print >> sys.stderr, 'Needed Judgements Remaining: %d' % pinged["needed_judgments"]


def results():
    job = _find_job()
    time.sleep(30)
    try:
        with open('produce_line_output.tsv', 'wb') as f:
            output = csv.writer(f, delimiter='\t')
            headers = ['rap_theme', 'description', 'previous_lines', 'possible_lines']
            output.writerow(headers)
            for judgment in job.judgments:
                try:
                    row=[judgment['title'], judgment['description'], judgment['previous'], judgment['next_line']]    
                    output.writerow(row)
                except:
                    continue
    except CrowdFlowerError, exc:
        # explain HTTP 202 Accepted response
        if exc.response.status_code == 202:
            print >> sys.stderr, 'Try again in a moment', exc


def download():
    job = _find_job()
    for judgment in job.judgments:
        print json.dumps(judgment)


def delete():
    job = _find_job()
    print >> sys.stderr, 'Cancelling Job[%d]' % job.id
    job.cancel()
    print 'Temporary Sleep for Voting Task Cancellation'
    time.sleep(5)
    print >> sys.stderr, 'Deleting Job[%d]' % job.id
    job.delete()

if __name__ == '__main__':
    methods = locals()
    for arg in sys.argv[1:]:
        if arg != 'ping':
            print >> sys.stderr, arg, '...'
        methods[arg]()
