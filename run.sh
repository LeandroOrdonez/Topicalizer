#!/bin/bash

function timer()
{
    if [[ $# -eq 0 ]]; then
        echo $(date '+%s')
    else
        local  stime=$1
        etime=$(date '+%s')

        if [[ -z "$stime" ]]; then stime=$etime; fi

        dt=$((etime - stime))
        ds=$((dt % 60))
        dm=$(((dt / 60) % 60))
        dh=$((dt / 3600))
        printf '%d:%02d:%02d' $dh $dm $ds
    fi
}

EXPECTED_ARGS=1
E_BADARGS=65

if [ $# -ne $EXPECTED_ARGS ]
then
  echo
  echo "(!) Usage: $0 /path/to/<list_uris_file>.txt"
  echo
  exit $E_BADARGS
fi

clear

#echo "The script starts now."
#echo
SERVICE_URIS_PATH=$1
echo "The whole 'topicalization' process is performed in two steps: "
echo "	* Step 1: Retrieving and processing the service descriptors."
echo "	* Step 2: Running Online LDA over the information regarding service operations."
echo
read -p "Press [Enter] key to start ..."
echo
echo "--> Starting Step 1: Retrieving and processing the service descriptors."
echo
t=$(timer)
# without proxy:
java -jar WebAPIDocProcessing.jar $SERVICE_URIS_PATH .doc/
#
# with proxy:
#java -Dhttp.useProxy=true -Dhttp.proxyHost='proxy.unicauca.edu.co' -Dhttp.proxyPort=3128 -Dhttp.nonProxyHosts='127.0.0.1|localhost' -jar WebAPIDocProcessing.jar $SERVICE_URIS_PATH .doc/

echo
echo
echo "Documentation Processing Done!"
echo
cd onlinelda
#echo "I will now fetch you a list of connected users:"
echo "--> Starting Step 2: Running Online LDA over the information regarding service operations."
echo
python online_lda_wsdl.py ../.doc/
python printtopics.py dictnostops.txt parameters/lambda-all.dat 15
python printtopicdistributions.py parameters/gamma-all.dat 5

# generating JSON output
python ./json_handler/jsonify.py ../outcome/per-document-topics.csv
cp ../outcome/per-document-topics.json /home/leandro/NetBeansProjects/TopicalizerBrowser/web/datasources
cp ../outcome/per-document-topics.csv /home/leandro/NetBeansProjects/TopicalizerBrowser/web/datasources
cp ../outcome/topics.csv /home/leandro/NetBeansProjects/TopicalizerBrowser/web/datasources
#w
echo "Topic Model Done..."
echo
printf 'Elapsed time: %s\n' $(timer $t)
echo
echo "That's it! now explore the operation categorization at: http://localhost:8080/openrdf-workbench/repositories/WebAPIModel"
echo
