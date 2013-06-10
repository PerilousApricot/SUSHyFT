#!/bin/csh

foreach crabfolder ( `ls -d $1` )
echo "=======     merging: $crabfolder/res/*.root     ======="
ls $crabfolder/res/*.root | awk '{print "file:" $0}' >! fileListToMerge.txt
edmCopyPickMerge inputFiles_load=fileListToMerge.txt outputFile=$crabfolder.root maxSize=10000000 >&! copypickmerge_output.txt
end

#unset crabfolder
