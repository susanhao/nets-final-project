#!/bin/bash
export CROWDFLOWER_API_KEY=8kg2XeBus1yfQGx32Tgt
(( i++ ))
while [[ $i -lt 16 ]] ; do
    echo "ITERATION $i"
    python code_production.py create
    python code_production.py launch
    python code_production.py check
    python code_production.py results
    python code_voting.py create
    python code_voting.py launch
    python code_voting.py check
    python code_voting.py results
    python votes_to_counts.py
    python QC_code.py
    (( i++ ))
done
