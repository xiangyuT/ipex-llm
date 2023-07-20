#!/bin/bash

# Set PCCS conf
if [ "$PCCS_URL" != "" ] ; then
    echo 'PCCS_URL='${PCCS_URL}'/sgx/certification/v4/' > /etc/sgx_default_qcnl.conf
    echo 'USE_SECURE_CERT=FALSE' >> /etc/sgx_default_qcnl.conf
fi

cd /ppml/bigdl-aa
echo "bigdl-aa start" > ./bigdl-aa.log
python3 ./bigdl-aa.py >> ./bigdl-aa.log 2>&1
