#!/bin/bash

# drops in jobs for a single dataset

if [[ $# -ne 4 ]]; then
    echo "Usage: $0 dataset working_dir is_data sample_name"
    exit 1
fi

DATASET=$1
WORKDIR=$2
if [[ $3 -eq 1 ]]; then
    OURDATA="--useData"
else
    OURDATA=""
fi
SAMPLE=$4
# do PBS for now, condor should be simple as well

if [ ! -d $WORKDIR ]; then
    mkdir -p $WORKDIR
fi

if [ -f $WORKDIR/makelock ]; then
    echo "Lockfile already exists $WORKDIR/makelock"
    exit 1
fi

touch $WORKDIR/makelock
./das.py --query="file dataset=$DATASET  instance=cms_dbs_ph_analysis_02" --limit=10000 | grep '/store/' > $WORKDIR/filelist.txt

COUNT=0
while true; do
    FILELIST=$( ./split_file.sh $WORKDIR/filelist.txt 100 $COUNT )
    if [[ "X$FILELIST" = 'X' ]]; then
        break
    fi
    COUNT=$(( $COUNT + 1 ))
    cat << EOF > tempscript.pbs
#!/bin/bash
#PBS -M andrew.m.melo@vanderbilt.edu
#PBS -l nodes=1:ppn=1
#PBS -l mem=1900mb
BS -l walltime=4:00:00
#PBS -j oe
#PBS -W group_list=jswhep
cd ~
. set-analysis.sh
INPUTLIST="\$(mktemp)"
cat << EOINPUT > \$INPUTLIST
$FILELIST
EOINPUT

python2.6 shyft_fwlite.py --inputListFile=$LINE --sampleName=$4 $OURDATA --lepType=0 --outname=$WORKDIR/$COUNT

EOF
    qsub tempscript.pbs
done
