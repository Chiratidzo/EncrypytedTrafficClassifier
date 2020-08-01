import os
from scapy.all import *
import time

def main():
    # packets per label = 10 000

    # set the file path 
    cwd = os.getcwd()
    directory_path = '/'.join(cwd.split('/')[:-1]) + '/data/SampleFlows/'

    start_time = time.time()

    # get the path to the sample_labels.csv
    sample_labels_file_path = '/'.join(cwd.split('/')[:-1]) + '/data/labels.csv'

    # open the file for writing
    f_write = open('/'.join(cwd.split('/')[:-1]) + '/data/data.csv', 'w')

    # write the headers
    header = ['label']
    for i in range(1, 1501):
        header.append('byte'+str(i))
    f_write.write(','.join(header)+'\n')

    count = 0
    if os.path.exists(sample_labels_file_path):
        with open(sample_labels_file_path) as f_read:
            for line in f_read:
                split_line = line.split(',')

                # get the file path, labels and num packets from csv
                file_path = split_line[0]
                label = split_line[1]
                num_packets = split_line[2]
                file_path = directory_path + file_path

                # process the pcap file
                label_packets(file_path, label, f_write)

                print('{} {} has been processed'.format(count, file_path))
                count += 1
    else:
        print('Could not find sample_labels.csv')
                    
    end_time = time.time()
    print('Total time to run: {}'.format(end_time-start_time)) 

    # close file for reading
    f_read.close()        

    # close file for writing
    f_write.close()

def label_packets(file_path, label, f_write):
    '''
    param file_path (String): Path to the pcap file
    param label(String): Label for each packet in the flow 
    '''

    # This value will determine how many packets per flow(with payload) to sample
    # set to ALL to sample all packets in a flow
    packets = 0
    packets_per_flow = 10000
    count_packets_per_flow = 0
    if os.path.exists(file_path):
        data = rdpcap(file_path)
        #print('Read {}'.format(file_path))
        sessions = data.sessions()
        for session in sessions:
            for pkt in sessions[session]:
                if count_packets_per_flow <= packets_per_flow:
                    if pkt.haslayer(IP) and pkt.haslayer(Raw):
                        hex_data = linehexdump(pkt[IP].payload, onlyhex=1, dump=True).split(" ")
                        decimal_data = list(map(hex_to_dec, hex_data))
                        #print(decimal_data)
                        f_write.write(label+','+','.join(decimal_data))
                        f_write.write('\n')
                    else:
                        continue
                else:
                    break
                count_packets_per_flow += 1

    else:
        print('Could not find {}'.format(file_path))

def hex_to_dec(hex):
    return str(int(hex, base = 16))

if __name__ == '__main__':
    main()
