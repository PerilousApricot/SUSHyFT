#!/bin/bash

echo "input parameters: cluster, process, run path, input path, output path, data?, leptype " $1 $2 $3 $4 $5 $6

CLUSTER=$1
PROCESS=$2
RUNPATH=$3
INPATH=$4
OUTPATH=$5 
DATA=$6


echo ""
echo "CMSSW on Condor"
echo ""

START_TIME=`/bin/date`
echo "started at $START_TIME"

echo ""
echo "parameter set:"
echo "CLUSTER: $CLUSTER"
echo "PROCESS: $PROCESS"
echo "RUNPATH: $RUNPATH"
echo "INPATH: $INPATH"
echo "OUTPATH: $OUTPATH"
echo "DATA: $DATA"

cd $RUNPATH
source /uscmst1/prod/sw/cms/shrc uaf
eval `scramv1 runtime -sh`

# setup certificate to copy files to dCache
#export X509_USER_PROXY=/uscms/home/skhalil/x509up_u44569

counter=0

for txt in `ls $INPATH`; do
    echo "going here: "$txt
    if test -f $INPATH/$txt; then
        echo "file   $INPATH/$txt   exists"
        name=`basename $txt .txt`
        echo "output file name: $name "
        if test $DATA -eq 0; then
        if test $counter -eq $PROCESS; then
            echo "python ntupleMaker.py --JES nominal --onDcache --txtfiles $INPATH/$txt --sample $OUTPATH/${name}"
            python ntupleMaker.py --JES nominal --onDcache --txtfiles $INPATH/$txt --sample $OUTPATH/${name}
        fi
            let "counter+=1"
        else
            let "counter+=1"
        fi

    fi
done

exitcode=$?

echo ""
END_TIME=`/bin/date`
echo "finished at ${END_TIME}"
exit $exitcode
