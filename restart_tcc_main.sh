#!/bin/bash
# Start tcc environment
#conda activate tcc

process_id=$(ps -ef | grep 'python /home/jvsn/tcc/tcc_main.py' | grep -v 'grep' | awk '{ printf $2 }')

if [[ ! $process_id ]]
then
    cd ~/tcc
    conda activate tcc
    python ~/tcc/tcc_main.py >/dev/null
    conda deactivate
fi

#conda deactivate
