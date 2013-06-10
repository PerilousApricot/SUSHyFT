#!/bin/bash

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 input_list lines_per_group group_id"
    exit 1
fi

INPUT_FILE=$1
FILES_PER_JOB=$2
GROUP_ID=$3
TOTAL_LINES=`wc -l $INPUT_FILE | awk '{print $1}'`
X=$(($FILES_PER_JOB * ($GROUP_ID + 1)))
HEAD_AMOUNT=$X
TAIL_AMOUNT=$FILES_PER_JOB
if (( ($X - $FILES_PER_JOB) > $TOTAL_LINES )); then
    # we're past the list
    exit 0
fi
if (( $X > $TOTAL_LINES )); then
    HEAD_AMOUNT=$(($X - $FILES_PER_JOB + ($TOTAL_LINES % $FILES_PER_JOB) ))
    TAIL_AMOUNT=$(($TOTAL_LINES % $FILES_PER_JOB))
fi
head -n $HEAD_AMOUNT $INPUT_FILE | tail -n $TAIL_AMOUNT
