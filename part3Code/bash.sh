#!/bin/bash
export CROWDFLOWER_API_KEY=8kg2XeBus1yfQGx32Tgt
(( i++ ))
while [[ $i -lt 10 ]] ; do
    echo "ITERATION $i"
    python code_production.py create
    python code_production.py launch
    COUNTER=$((python code_production.py ping) 2>&1)
        until [[ $COUNTER -lt 1 ]]
        do
            echo Production judgments remaining are $COUNTER
            COUNTER=$((python code_production.py ping) 2>&1)
        done
    python code_production.py results
    python code_production.py delete
    python code_voting.py create
    python code_voting.py launch
    COUNTER=$((python code_voting.py ping) 2>&1)
        until [[ $COUNTER -lt 1 ]]
        do
            echo Voting judgments remaining are $COUNTER
            COUNTER=$((python code_voting.py ping) 2>&1)
        done
    python code_voting.py results
    python code_voting.py delete
    python votes_to_counts.py
    python QC_code.py
    (( i++ ))
done

