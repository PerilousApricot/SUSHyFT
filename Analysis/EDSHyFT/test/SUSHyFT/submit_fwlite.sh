run="v1"
while read LINE; do
    echo $LINE
    SHORTLINE=$(echo ${LINE} | tr '/' '_') 
    CFGFILE="config_${SHORTLINE}.cfg"
    sed "s!DATASETPATH!${LINE}!" crab_fwlite.cfg > $CFGFILE
    sed -i "s!WORKDIR!crab_${run}_${SHORTLINE}!" $CFGFILE
    sed -i "s!OUTPUTDATA!melo_${run}_${SHORTLINE}!" $CFGFILE
    sed -i "s!pycfg.*!pycfg_params= useData=1!" $CFGFILE
done < data_pat.txt

while read LINE; do
    echo $LINE
    SHORTLINE=$(echo ${LINE} | tr '/' '_') 
    CFGFILE="config_${SHORTLINE}.cfg"
    sed "s!DATASETPATH!${LINE}!" crab_fwlite.cfg > $CFGFILE
    sed -i "s!WORKDIR!crab_${run}_${SHORTLINE}!" $CFGFILE
    sed -i "s!OUTPUTDATA!melo_${run}_${SHORTLINE}!" $CFGFILE
    sed -i "s!pycfg.*!pycfg_params= useData=0!" $CFGFILE
done < mc_pat.txt
