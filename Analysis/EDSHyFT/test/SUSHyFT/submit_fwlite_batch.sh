#!/bin/bash

# Submits a list of datasets to be processed

# data sample: sed 's!/\(.*\)/.*\(Run.*_v[0-9]*\).*!\1_\2!'
# mc sample: sed 's!/\(.*\)/.*/.*!\1!'

if [[ $# -ne 3 ]]; then
    echo "Usage: $1 input_list is_data workdir"
    exit 1
fi

INPUTLIST=$1
WORKDIR=$3

if [[ ! -e $WORKDIR ]]; then
    mkdir -p $WORKDIR
fi

while read LINE; do
    if [[ $2 -eq 1 ]]; then
        DIRNAME=$( echo $LINE | sed 's!/\(.*\)/.*\(Run.*_v[0-9]*\).*!\1_\2!' )
        SAMPLENAME='data'
    else
        DIRNAME=$( echo $LINE | sed 's!/\(.*\)/.*/.*!\1!' )
        case $DIRNAME in
            ZJet*)
                SAMPLENAME='zjets'
                ;;
            TTJet*)
                SAMPLENAME='ttjets'
                ;;
            WJet*)
                SAMPLENAME='wjets'
                ;;
            Tbar*)
                SAMPLENAME='singletop'
                ;;
            T_*)
                SAMPLENAME='singletop'
                ;;
            *)
                echo "Error, unknown samplename $DIRNAME"
                exit 1
        esac
    fi
    echo "$SAMPLENAME $DIRNAME"
    ./submit_fwlite_dataset.sh $LINE $WORKDIR/$DIRNAME "$2" $SAMPLENAME
done < "$INPUTLIST"
