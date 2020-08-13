#!/bin/bash

RAW_PCAP_FILES=./data/raw_pcaps/*.pcap
OUTPUT_DIR=./data/flows/

mkdir $OUTPUT_DIR # create flows directory

num_files=`ls $RAW_PCAP_FILES | wc -l | tr -d '[:space:]'` # for keeping track of progress
i=1
for f in $RAW_PCAP_FILES
do
     echo "Processing $f ($i/$num_files)"
     ((i=i+1))
     flow-splitting/pkt2flow/pkt2flow -u -o $OUTPUT_DIR $f
done
