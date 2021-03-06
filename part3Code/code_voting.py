'''
code_voting.py

Provides a user with a rap theme and previously finalized rap lines, and then asks a user to vote on the lines

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
job_tag = 'vote for lines'


def _find_job():
    for job in conn.jobs():
        if job_tag in job.tags:
            return job


def create():
    #filename = os.path.join(crowdflower.root, 'examples', 'spam.txt')
    #filename = '/Users/TDPeterson/Dropbox/nets213/FINAL/produce_line_output.tsv'

    def iter_data():
        for i, line in enumerate(open('produce_line_output.tsv'), 1):
            if i != 1:
                title, description, previous_lines, possible_lines = line.strip().split('\t')
                yield {'rap_theme': title, 'description': description, 'previous_lines':previous_lines, 'possible_lines': possible_lines}

    # Format of inputing title, description, and candidate lines
    input_voting = list(iter_data())
    
    job = conn.upload(input_voting)
    print >> sys.stderr, 'Uploaded data' 

    job.update({
        'title': 'Pick the best line for a rap!',
        'max_judgments_per_worker': 10,
        'units_per_assignment': 10,
        'judgments_per_unit': 13,
        'payment_cents': 5,
        'instructions': '''
<h1>Overview: &nbsp;</h1>

<ul>
	<li>Your task is to vote for your favorite line that should be added to this rap!</li>
	<li>A rap is "spoken or chanted rhyming lyrics"</li>
</ul>
<hr>

<h1>Steps:&nbsp;</h1>

<ol>
	<li>Read the "Rap Title" , "Description", &nbsp;and "Current Lines"</li>
	<li>Think about a creative next line for this rap that relates to the title, description, and lines already written.</li>
	<li>For each possible line, indicate if it should be added or not to the Current Lines.</li>
</ol>
<hr>

<h1>Rules &amp; Tips:</h1>

<ol>
	<br>
	<li>Think about what makes a good rap. Vote for the line that 'flows' the best <u>with the current lines</u>, but is also your favorite...<u>the best line might be part of a class presentation!</u></li>
	<li>If "Current Lines" says N/A, then just pick your favorite line that is based on the "Rap Title" and/or "Description"</li>
	<li><u>Vote no if the line is already in the current lines</u></li>    
</ol>

<p>THANKS EVERYONE!! :D :D :D</p>
<hr>

        ''',
        'cml': '''
<div class="html-element-wrapper"></div>
  <span>
    <strong>
      <font size = "5">Rap Title: {{rap_theme}}</font>
    </strong>
  </span>
  <br/>
  <br/>
  <span>Description: {{description}}</span>
  <br/>
  <br/>
  <span>Current Lines: <ul><font size = "3"><strong>{{previous_lines}}</strong></font></ul></span>
<br/>
    <font size = "4">Possible Line:</font> <ul><font size = "6"><strong><u>{{possible_lines}}</u></strong></font></ul>
<br/>
<br/>
<cml:radios label="Should the Possible line be added to the above Current Lines of the rap?" validates="required" gold="true">
  <cml:radio label="yes" value="yes" />
  <cml:radio label="no" value="no" />
</cml:radios>
        ''',
        'options': {
            'front_load': 0, # quiz mode = 1; turn off with 0
        }
    })
    print >> sys.stderr, 'Updated job'

    # add the 'vote for line' tag so that we can easily find this job later
    job.tags = [job_tag]
    print >> sys.stderr, 'Tagged job as %r' % job_tag

def launch():
    job = _find_job()
    job.launch(10)
    print 'Temporary Sleep for Voting Task to Launch'
    time.sleep(2)
    print >> sys.stderr, 'Launched Job[%d]' % job.id

def ping():
    job = _find_job()
    time.sleep(300)
    print job.properties["completed"]
    #print >> sys.stderr, 'Needed Judgements Remaining: %d' % pinged["needed_judgments"]
    
def check():
    job = _find_job()
    complete = job.properties["completed"]
    while complete == False:
        print 'Voting: Incomplete'
        print 'Judgments remaining: %d' % job.ping()["needed_judgments"]
        time.sleep(300)
        job = _find_job()
        complete = job.properties["completed"]
    print "Voting: complete!"
    

def results():
    job = _find_job()
    time.sleep(30)
    try:
        with open('produce_vote_output.csv', 'wb') as f:   # formerly tsv
            output = csv.writer(f) # CHANGE, used to have the delimiter = '\t'
            headers = ['rap_theme','description', 'previous_lines', 'possible_lines', 'should_this_line_be_added_to_the_above_rap']
            output.writerow(headers)
            for judgment in job.judgments:
                row=[judgment['rap_theme'], judgment['description'], judgment['previous_lines'], judgment['possible_lines'], judgment['should_the_possible_line_be_added_to_the_above_current_lines_of_the_rap']]
                output.writerow(row)
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
