#!/bin/bash

# For testing the script on 5 flow pcaps:
# FLOW_FILES=../data/SampleFlowsSmall/*.pcap

FLOW_FILES=../data/SampleFlows/tcp_syn/*.pcap

# Header row of the labels csv file
echo "FlowName,LabelDetails" > labels.csv

# Loop through TCP_SYN flows folder, label each flow file using nDPI 
# and append the filename-label pair to labels.csv
for f in $FLOW_FILES
do
     echo "Processing $f"

     # 1) Run nDPI on the file, $f
     ./nDPI/example/ndpiReader -i $f > nDPI_output.txt

     # 2) Extract the label and flow stats from the nDPI output
     line_num=`grep -n "Detected protocols" "nDPI_output.txt"`
     line_num=`echo $line_num | cut -f1 -d":"`
     line_num=`expr $line_num + 1`
     flow_stats=`sed "${line_num}q;d" "nDPI_output.txt"`

     # 3) Append filename-label_stats pair to labels.csv
     echo "${f}, ${flow_stats}" >> labels.csv 
done
