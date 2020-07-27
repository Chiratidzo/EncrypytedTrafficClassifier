#!/bin/bash
FILES=data/SamplePcaps/*.pcap

output_dir=$1

for f in $FILES
do
     echo "Processing $f"
     pkt2flow/pkt2flow -uvx -o $output_dir $f
done
