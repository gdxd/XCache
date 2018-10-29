#!/bin/sh

#getting paths from a service.given as a parameter 1 and transferting through xcache given as a parameter 2.

# X509_USER_PROXY, X509_CERT_DIR, X509_VOMS_DIR do not have to be defined/provided
# but then it won't really be useful

export X509_USER_PROXY=/etc/grid-security/x509up
export X509_CERT_DIR=/etc/grid-security/certificates
export X509_VOMS_DIR=/etc/grid-security/vomsdir

echo $X509_USER_PROXY $X509_CERT_DIR $X509_VOMS_DIR

export LD_PRELOAD=/usr/lib64/libtcmalloc.so
export TCMALLOC_RELEASE_RATE=10

export TIMEFORMAT='%3R'

#SERVER="http://localhost"
#SERVER="https://xcache.org"
SERVER=$1

# XCACHE_SERVER='https://fax.mwt2.org//'
XCACHE_SERVER=$2

while true
do

    # get next n files in queue and save them as json file
    curl -s -k -X GET "$SERVER/stress_test/" > res.json

    # parse filenames and paths
    fn=( $(jq -C -r '.filename'  res.json) )
    pth=( $(jq -C -r '.path'  res.json) )
    id=( $(jq -C -r '._id'  res.json) )

    printf "$(date) copying %s\n" "${pth}"
    export XRD_LOGFILE=${id}.LOG
    { time timeout 270 xrdcp -f -d 2 -N $XCACHE_SERVER${pth} /dev/null  2>&1 ; } 2> timing.txt
    # { time timeout 270 sleep 5  2>&1 ; } 2> ${id}.tim

    code=$?
    rate=`cat timing.txt`
    rm timing.txt
    echo "ret code: $code   duration: $rate"

    curl -s -k -X GET "$SERVER/stress_result/$id/$code/$rate"

done
