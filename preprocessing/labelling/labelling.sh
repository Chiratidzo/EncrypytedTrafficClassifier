#!/bin/bash

# For testing the script on 5 flow pcaps:
# FLOW_FILES=../data/SampleFlowsSmall/*.pcap

TCP_FLOW_FILES=../data/SampleFlows/tcp_syn/*.pcap
UDP_FLOW_FILES=../data/SampleFlows/udp/*.pcap

# Write the header row to the labels.csv file
echo "FlowFilePath,LabelDetails" > labels.csv
echo "Created labels.csv with header row"

###############################
####### Label TCP Flows #######
###############################

echo "Labelling TCP flows..."

# Loop through TCP_SYN flows folder, label each flow file using nDPI 
# and append the filename-label pair to labels.csv
tcp_file_counter=0
for f in $TCP_FLOW_FILES
do
     # Every 1000th file processed, print to console to track of progress
     ((tcp_file_counter=tcp_file_counter+1))
     remainder=$(( tcp_file_counter % 1000 ))
     if [ $remainder -eq 0 ]
     then
          echo Processing file \#$tcp_file_counter
     fi

     # 1) Run nDPI on the file, $f, with output stored temporarily in nDPI_output.txt
     ./nDPI/example/ndpiReader -i $f > nDPI_output.txt

     # 2) Extract the label and flow stats from the nDPI output

     # i) Find the line number and line for the line containing "Detected protocols"
     line_num=`grep -n "Detected protocols" "nDPI_output.txt"`

     # ii) Extract just the line number
     line_num=`echo $line_num | cut -f1 -d":"`

     # iii) Increment the line number - since nDPI label and flow statistics found on the next line
     line_num=`expr $line_num + 1`

     # iv) Extract the contents on the line containing the label and flow statistics
     flow_stats=`sed "${line_num}q;d" "nDPI_output.txt"`

     # 3) Append filename-label_stats pair to labels.csv
     echo "${f}, ${flow_stats}" >> labels.csv 
done


# ###############################
# ####### Label UDP Flows #######
# ###############################

echo "Labelling UDP flows..."

# Loop through UDP flows folder, label each flow file using nDPI 
# and append the filename-label pair to labels.csv
udp_file_counter=0
for f in $UDP_FLOW_FILES
do
     # Every 1000th file processed, print to console to track of progress
     ((udp_file_counter=udp_file_counter+1))
     remainder=$(( udp_file_counter % 1000 ))
     if [ $remainder -eq 0 ]
     then
          echo Processing file \#$udp_file_counter
     fi

     # 1) Run nDPI on the file, $f, with output stored temporarily in nDPI_output.txt
     ./nDPI/example/ndpiReader -i $f > nDPI_output.txt

     # 2) Extract the label and flow stats from the nDPI output

     # i) Find the line number and line for the line containing "Detected protocols"
     line_num=`grep -n "Detected protocols" "nDPI_output.txt"`

     # ii) Extract just the line number
     line_num=`echo $line_num | cut -f1 -d":"`

     # iii) Increment the line number - since nDPI label and flow statistics found on the next line
     line_num=`expr $line_num + 1`

     # iv) Extract the contents on the line containing the label and flow statistics
     flow_stats=`sed "${line_num}q;d" "nDPI_output.txt"`

     # 3) Append filename-label_stats pair to labels.csv
     echo "${f}, ${flow_stats}" >> labels.csv 
done

# Remove temporary nDPI_output.txt file
rm nDPI_output.txt

# Clean up labels.csv 
python3 labels_csv_cleaning.py


