run="v2"
SHORTLINE=$(date +%Y%m%d%k%M)
while read LINE; do
    echo $LINE
    SHORTNAME=$(echo ${LINE} | tr '/' '_'  | tr '_' ' ' | awk '{print $5 "_" $6}')
    CFGFILE="stage_edntuple/config_${SHORTNAME}.cfg"
    sed "s!DATASETPATH!${LINE}!" crab_edtuple.cfg > $CFGFILE
    sed -i "s!WORKDIR!crab_${run}_${SHORTNAME}!" $CFGFILE
    sed -i "s!OUTPUTDATA!melo_${run}_${SHORTNAME}_${SHORTLINE}!" $CFGFILE
    sed -i "s!pycfg.*!pycfg_params= useData=1!" $CFGFILE
done < data_pat.txt
rm stage_edntuple/config*

while read LINE; do
    echo $LINE
    SHORTNAME=$(echo ${LINE} | tr '/' '_') 
    CFGFILE="stage_edntuple/config_${SHORTNAME}.cfg"
    sed "s!DATASETPATH!${LINE}!" crab_edtuple.cfg > $CFGFILE
    echo "Looking at shortline ${SHORTLINE}"
    sed -i "s!WORKDIR!crab_${run}_${SHORTNAME}!" $CFGFILE
    sed -i "s!OUTPUTDATA!melo_${run}_${SHORTNAME}_${SHORLINE}!" $CFGFILE
    sed -i "s!pycfg.*!pycfg_params= useData=0!" $CFGFILE
    if [[ $LINE =~ StoreResults ]]; then
        sed -i "s!dbs_url.*!!" $CFGFILE
    fi
done < mc_pat.txt
